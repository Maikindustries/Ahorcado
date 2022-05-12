import random
from tabnanny import check
import requests
from flask import Flask, render_template, session, redirect, request

app = Flask(__name__)
app.secret_key = "Esto no deberíair aquí."

@app.route("/")
def index():
  return render_template("busqueda.html")

@app.route("/busqueda",methods=["POST"])
def busqueda():
  nombre = request.form.get("nombre", None)
  checkbox = request.form.get("checkbox",None)
  checkbox = True if checkbox == "on" else False

  page_countries = requests.get(f"https://api.nationalize.io/?name={nombre}")
  page_age = requests.get(f"https://api.agify.io/?name={nombre}")
  page_gender = requests.get(f"https://api.genderize.io/?name={nombre}")
  page_joke = requests.get("https://geek-jokes.sameerkumar.website/api?format=json")

  if page_countries.status_code == 200 and page_countries.status_code == page_countries.status_code and page_gender.status_code == page_countries.status_code == page_joke.status_code:
    contenido_pais = page_countries.json()
    contenido_edad = page_age.json()
    contenido_genero = page_gender.json()
    contenido_joke = page_joke.json()

    lista_pais = []
    for pais in contenido_pais["country"]:
      paiss = pais["country_id"]
      print(paiss)
      page_country_info = requests.get(f"https://restcountries.com/v3.1/name/{paiss}")
      if page_country_info.status_code == 200:
        contenido_pais = page_country_info.json()
        nombre_pais = contenido_pais[0]["name"]["common"]
        link_imagen = contenido_pais[0]["flags"]["png"]
        lista_pais.append([nombre_pais,paiss,pais["probability"],link_imagen])


    return render_template("resultado.html",nombre=nombre,edad =contenido_edad["age"],genero=contenido_genero["gender"],probabilidad=contenido_genero["probability"],datos=lista_pais,show_joke=checkbox,chiste=contenido_joke["joke"])
  

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
