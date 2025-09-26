# 📰 Agente News Editor con LangGraph

## 📌 Resumen Ejecutivo
Aplicación fullstack multi-agente que valida y expande rumores de traspasos en fútbol para generar artículos publicables.  
La orquestación se realiza con **LangGraph**, que permite decidir dinámicamente qué agente ejecutar según el estado del flujo.

El sistema incluye:
- **Backend** en FastAPI con API REST y persistencia en PostgreSQL mediante *checkpoints* de LangGraph.
- **Frontend** de ejemplo en Angular.
- **Base de datos** incluida en Docker Compose.
- **Orquestación multi-agente** con LangGraph.

---

## 🚀 Problema que resuelve
Los rumores de traspasos deportivos suelen estar incompletos o mal redactados.  
Este sistema:
- Valida si la noticia es relevante.
- Completa campos faltantes (club actual, club destino, valor de mercado).
- Expande el contenido a un mínimo de 100 palabras con estilo pulido.
- Genera un artículo final listo para publicación.

---

## ⚙️ Arquitectura y Orquestación
### Workflows principales
- **NewsWorkflow**:  
  - `news_chef (grader)`: evalúa relevancia y faltantes.  
  - `market_value_researcher`: añade valor de mercado.  
  - `current_club_researcher`: añade club actual.  
  - `word_count_rewriter`: expande y pule estilo.  

- **HumanWorkflow**:  
  - Envuelve el flujo principal.  
  - Añade confirmación final.  
  - Conecta el *checkpointer* para persistencia por `thread_id`.

### Backend
- FastAPI expone endpoints REST.  
- PostgreSQL guarda el estado de ejecución con *checkpoints*.  
- Contenedor Docker para backend + base de datos.

### Frontend
- Angular como ejemplo de UI.  
- Permite probar consultas y visualizar artículos generados.

---

## 📂 Estructura del Proyecto
```
news-editor/
│── backend/          # FastAPI + lógica LangGraph
│── frontend/         # Angular de ejemplo
│── workflows/        # Definición de agentes y flujos LangGraph
│── docker-compose.yml
│── README.md
```

---

## 🔧 Requisitos
- Python 3.10+
- Node.js 18+
- PostgreSQL
- Docker y Docker Compose
- Claves API de OpenAI (u otro LLM)

---

## ▶️ Ejecución
1. Clonar el repositorio:
   ```bash
   git clone https://github.com/tu-usuario/news-editor.git
   cd news-editor
   ```

2. Crear y configurar el archivo `.env` en la raíz:
   ```env
   OPENAI_API_KEY=tu_api_key
   DATABASE_URL=postgresql://user:password@db:5432/newsdb
   ```

3. Levantar con Docker Compose:
   ```bash
   docker-compose up --build
   ```

4. Acceder al backend:
   - API Docs: `http://localhost:8000/docs`
   - Frontend Angular: `http://localhost:4200`

---

## 📊 Ejemplo de uso
### Entrada
```
Rumor: Messi podría pasar del PSG al Inter Miami.
```

### Salida
```
Artículo expandido (≥100 palabras), con validación de fuente, club actual, club destino y valor de mercado.
```

---

## 👨‍💻 Autor
Francisco Moyano Escalera  
Especialista en Data, AI y Automatización  
📧 frannmmm419@gmail.com  
🌐 GitHub: [frannmmm](https://github.com/frannmmm)

