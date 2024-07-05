from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from keras.models import load_model
from keras.preprocessing.sequence import pad_sequences
from pydantic import BaseModel
import pickle

app = FastAPI()

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*"
    ],  # Permitir todas las orígenes, puedes especificar dominios específicos aquí
    allow_credentials=True,
    allow_methods=["*"],  # PerDOmitir todos los métodos
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


# Cargar el modelo y el tokenizador
modelNN = load_model("modelNN.h5")
with open("tokenizerNN.pkl", "rb") as handle:
    tokenizerNN = pickle.load(handle)


@app.post("/verify")
def send_message(payload: Payload):
    text = payload.text
    try:
        maxlen = 1000
        # Preprocesar la entrada
        sequences = tokenizerNN.texts_to_sequences([text])
        padded_sequences = pad_sequences(sequences, padding="post", maxlen=maxlen)

        # Hacer predicción
        prediction = modelNN.predict(padded_sequences)
        predicted_label = int(round(prediction[0][0]))
        result = False if predicted_label == 0 else True
        return {"text": text, "correct": result}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8080)
