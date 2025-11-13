from flask import Flask, render_template, request
import os

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


if __name__ == "__main__":
    app.run(debug=True)
