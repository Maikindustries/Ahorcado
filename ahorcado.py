import random
import requests
from flask import Flask, render_template, session, redirect, request

words = ["perro","gato","pants","raton","amazon"]

def new_word_state():
    w = random.choice(words)
    state = [False for i in range(len(w))]
    return [w, state]


def current_string():
    res = ""
    i = 0
    for c in session['word']:
        if session["word_state"][i]:
            res += c + " "
        else:
            res += "_ "  
        i += 1
    return res


app = Flask(__name__)
app.secret_key = "Esto no debería ir  aquí."


@app.route("/elegir_letra", methods=["POST"])
def elegir_letra():
    letra = request.form.get("Input", None)
    if letra in session["word"]:
        state = session["word_state"]
        i = 0
        for c in session["word"]:
            if letra == c:
                state[i] = True
            i += 1
        session["word_state"] = state
    else:
        session["fails"] += 1

    #Verificar si ganó o perdió
    cont = 0
    for i,c in enumerate(session['word']):
        if session["word_state"][i]:
            cont += 1        
    #Verificar que si perdió    
    if session["fails"] >= 6:
        return render_template("fin.html",resultado="Perdedor")
    #Verificar si ganó
    if cont == len(session["word"]):
        return render_template("fin.html",resultado="Ganador") 
    return redirect("/")


@app.route("/")
def index():
    if "word" not in session:
        return redirect("/nuevo_juego")
    return render_template("ahorcado.html",state=current_string(),fails=session['fails'])


@app.route("/nuevo_juego")
def nuevo_juego():
    w, s = new_word_state()
    session["word"] = w
    session["word_state"] = s
    session["fails"] = 0
    return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)