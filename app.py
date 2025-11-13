from flask import Flask, render_template, request
import os
import json

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/scan", methods=["POST"])
def scan():
    url = request.form.get("url")

    if not url:
        is_safe_result = False
        return render_template("results.html", scanned_url="URL no proporcionada", is_safe=is_safe_result)

    dangerous_urls = set()
    base_dir = os.path.dirname(os.path.abspath(__file__))
    txt_path = os.path.join(base_dir, 'url_peligrosas.txt') 

    try:
        with open(txt_path, "r") as f:
            dangerous_urls = {line.strip() for line in f if line.strip()}
    except FileNotFoundError:
        pass 
        
    
    is_safe_result = True
    
    if not url.lower().startswith("https://"):
        is_safe_result = False
    
    if url in dangerous_urls:
        is_safe_result = False

    return render_template("results.html", scanned_url=url, is_safe=is_safe_result)


@app.route("/reportar/<path:scanned_url>")
def reportar(scanned_url):
    return render_template("reportar.html", url_a_reportar=scanned_url )

@app.route("/enviar-reporte", methods=["POST"])
def enviar_reporte():
    url_reportada = request.form.get("url_reportada")
    nombre = request.form.get("nombre")
    correo = request.form.get("correo")
    motivo = request.form.get("motivo")

    base_dir = os.path.dirname(os.path.abspath(__file__))
    txt_path = os.path.join(base_dir, 'url_peligrosas.txt') 

    with open(txt_path, "a") as f:
        f.write(f"{url_reportada} \n")

   
    nuevo_reporte = {
        "url": url_reportada,
        "nombre": nombre,
        "correo": correo,
        "motivo": motivo
    }
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(base_dir, 'reportes.json')
    
    datos_actuales = {"reportes": []}

    if os.path.exists(json_path) and os.path.getsize(json_path) > 0:
        try:
            with open(json_path, 'r') as f:
                datos_actuales = json.load(f)
        except json.JSONDecodeError:
            pass
            
    datos_actuales["reportes"].append(nuevo_reporte)
    
    try:
        with open(json_path, 'w') as f:
            json.dump(datos_actuales, f, indent=4)
    except IOError:
        pass
   
    return render_template("index.html", reporte=True)


if __name__ == "__main__":
    app.run(debug=True)
