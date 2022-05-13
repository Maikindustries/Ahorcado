import random
import requests
from html.parser import HTMLParser
from flask import Flask, render_template, session, redirect, request

app = Flask(__name__)
app.secret_key = "Esto no debería ir  aquí."

@app.route("/generar_trivia", methods=["POST"])
def generar_trivia():
    categoria = request.form.get("categoria",None)
    dificultad = request.form.get("dificultad", None)
    trivia = requests.get(f"https://opentdb.com/api.php?amount=1&category={categoria}&difficulty={dificultad}&type=multiple")
    body = trivia.json()
    print(body)
    h = HTMLParser()
    preguntaV = body["results"][0]["question"]
    # preguntaV = h.unescape(body["results"][0]["question"])
    respuestasl = []
    correcta = body["results"][0]["correct_answer"]
    session["correcta"] = correcta
    respuestasl.append(correcta)
    respuestasl.append(body["results"][0]["incorrect_answers"][0])
    respuestasl.append(body["results"][0]["incorrect_answers"][1])
    respuestasl.append(body["results"][0]["incorrect_answers"][2])
    random.shuffle(respuestasl)
    return render_template("trivia.html",respuestas=respuestasl,pregunta=preguntaV)

@app.route("/responder", methods=["POST"])
def responder():
    respuesta = request.form.get("respuesta",None)
    dog_image = requests.get("https://dog.ceo/api/breeds/image/random").json()["message"]
    kanye = requests.get("https://api.kanye.rest/").json()["quote"]

    if respuesta == session["correcta"]:
        return render_template("resultado.html",resultado="¡Ganaste!",imagen=dog_image,frase=kanye)
    else:
        return render_template("resultado.html",resultado="¡Perdiste!",imagen=dog_image,frase=kanye)

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)