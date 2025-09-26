from typing import TypedDict

from langgraph.graph import END, StateGraph

from .news_workflow import NewsWorkflow


class InputState(TypedDict):
    # El workflow recibe "article" (no "question")
    article: str


class IntermediateState(InputState):
    answer: str
    error: bool
    off_or_ontopic: str


class FinalState(IntermediateState):
    confirmed: str


class HumanWorkflow:
    def __init__(self):
        self.app = NewsWorkflow()
        self.checkpointer = None
        self.workflow = None

    def set_checkpointer(self, checkpointer):
        self.checkpointer = checkpointer
        self.workflow = self._create_workflow()

    def _create_workflow(self):
        workflow = StateGraph(FinalState, input=InputState, output=FinalState)
        workflow.add_node("newsagent_node", self.newsagent_node)
        workflow.add_node("confirm_node", self.confirm_node)
        workflow.set_entry_point("newsagent_node")
        workflow.add_edge("newsagent_node", "confirm_node")
        workflow.add_edge("confirm_node", END)
        return workflow.compile(
            checkpointer=self.checkpointer,
            interrupt_after=["newsagent_node"],
        )

    async def newsagent_node(self, state: IntermediateState) -> IntermediateState:
        try:
            # Usamos el campo "article" para invocar el NewsWorkflow
            response = await self.app.ainvoke({"article": state["article"]})
            state["answer"] = response.get(
                "final_article", "No se pudo generar respuesta"
            )
            state["off_or_ontopic"] = response.get("off_or_ontopic", "unknown")
            state["error"] = False
        except Exception as e:
            state["answer"] = f"Error on newsagent_node: {str(e)}"
            state["error"] = True
            print(f"Error invoking newsagent_node: {e}")
        return state

    def confirm_node(self, state: FinalState) -> FinalState:
        state["confirmed"] = "true"
        return state

    async def ainvoke(self, *args, **kwargs):
        if not self.workflow:
            raise RuntimeError("HumanWorkflow has no checkpointer set.")
        return await self.workflow.ainvoke(*args, **kwargs)
