import json
from flask import Flask, request, jsonify
from ai_model import get_info_startup
from utils import validar_url

app = Flask(__name__)

@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Ruta no encontrada"}), 404

@app.route("/api/infostartup", methods=["POST"])
def api_empresa():
    if not request.is_json:
        return jsonify({"error": "El cuerpo de la solicitud debe ser JSON (Content-Type: application/json)"}), 400
    data = request.get_json()
    if "url" not in data:
        return jsonify({"error": "El campo 'url' es obligatorio en el cuerpo JSON"}), 400
    url = data["url"]
    if not validar_url(url):
        return jsonify({"error": "URL no válida. Por favor, verifica el formato."}), 400
    try:
        resultado_string = get_info_startup(url)
        resultado_dict = json.loads(resultado_string)
        return jsonify(resultado_dict), 200
    except json.JSONDecodeError:
        return jsonify({"error": "Error de formato. La información recibida no es un JSON válido."}), 500
    except Exception as e:
        return jsonify({"error": "Error interno al procesar la solicitud", "detalle": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)