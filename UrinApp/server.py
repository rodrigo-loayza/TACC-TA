import time
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pickle

app = FastAPI()

# Cargar el modelo de clasificación
# with open("model.pkl", "rb") as f:
#     model = pickle.load(f)

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*"
    ],  # Permitir todas las orígenes, puedes especificar dominios específicos aquí
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos
    allow_headers=["*"],  # Permitir todos los headers
)

# Montar la carpeta 'static' para servir archivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")


# Clase para recibir el payload de las solicitudes
class Payload(BaseModel):
    text: str


@app.get("/")
async def read_index():
    return FileResponse("index.html")


@app.post("/verify")
def send_message(payload: Payload):
    time.sleep(1.5)

    # count_vectorizer = pickle.load(open("count_vectorizer.pickle", "rb"))
    # decision_tree_classifier = pickle.load(
    #     open("decision_tree_classifier.pickle", "rb")
    # )
    # rules = pickle.load(open("rules.pickle", "rb"))
    # utterances_examples = pickle.load(open("utterances_examples.pickle", "rb"))

    text = payload.text
    if text != "Contraseña":
        result = False
    else:
        result = True

    return {"text": text, "correct": result}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8080)
