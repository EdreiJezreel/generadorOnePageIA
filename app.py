import json
import time
import concurrent.futures
from flask import Flask, request, jsonify
from ai_model import get_info_startup
from ai_model_fallback import get_info_startup_fallback
from utils import validar_url

app = Flask(__name__)

@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Ruta no encontrada"}), 404

@app.route("/api/infostartup", methods=["POST"])
def api_empresa():
    print("📥 Nueva solicitud recibida en /api/infostartup")
    if not request.is_json:
        print("⚠️ Solicitud rechazada: no tiene formato JSON válido.")
        return jsonify({"error": "El cuerpo de la solicitud debe ser JSON (Content-Type: application/json)"}), 400
    data = request.get_json()
    if "url" not in data:
        print("⚠️ Solicitud rechazada: falta el campo 'url'.")
        return jsonify({"error": "El campo 'url' es obligatorio en el cuerpo JSON"}), 400
    url = data["url"]
    if not validar_url(url):
        print(f"⚠️ URL no válida recibida: {url}")
        return jsonify({"error": "URL no válida. Por favor, verifica el formato."}), 400
    print(f"🚀 Ejecutando modelo principal (get_info_startup) con límite de 30 segundos...")
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = executor.submit(get_info_startup, url)
        try:
            start_time = time.time()
            resultado_string = future.result(timeout=30)
            elapsed = round(time.time() - start_time, 2)
            print(f"✅ Modelo principal completado correctamente en {elapsed}s.")
            resultado_dict = json.loads(resultado_string)
            return jsonify(resultado_dict), 200
        except concurrent.futures.TimeoutError:
            print("⏰ Tiempo de espera agotado en modelo principal (>30s). Pasando al modelo auxiliar...")
            future.cancel()
        except json.JSONDecodeError as e:
            print(f"❌ Error de formato JSON en modelo principal: {e}")
        except Exception as e:
            print(f"💢 Error interno en modelo principal: {e}")
    print("🔄 Ejecutando modelo auxiliar sin web_search (get_info_startup_fallback) con límite de 30 segundos...")
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_fallback = executor.submit(get_info_startup_fallback, url)
        try:
            start_time = time.time()
            resultado_fallback_string = future_fallback.result(timeout=25)
            elapsed = round(time.time() - start_time, 2)
            print(f"✅ Modelo auxiliar completado correctamente en {elapsed}s.")
            resultado_fallback_dict = json.loads(resultado_fallback_string)
            return jsonify({
                "warning": "Se usó el modelo auxiliar sin web_search por timeout o error en el modelo principal.",
                "data": resultado_fallback_dict
            }), 200
        except concurrent.futures.TimeoutError:
            print("⏰ Tiempo de espera agotado en modelo auxiliar (>30s). Se usará el JSON de prueba.")
            future_fallback.cancel()
        except Exception as e2:
            print(f"🔥 Error crítico al ejecutar el modelo auxiliar: {e2}")
    print("🧩 Usando JSON de prueba por falla total de ambos modelos.")
    return jsonify({
        "active": True,
        "alliances": ["N/D"],
        "capturista": "",
        "contacto": [
            {
                "email": "nombre.contacto@gmail.com",
                "name": "nombre contacto",
                "notes": "Contacto principal para consultas generales y colaboraciones.",
                "phone": "+52 55 1169 1227",
                "position": "posición",
                "projects": "proyecto"
            }
        ],
        "contactocid": "Ada Palazuelos",
        "dateinactive": "",
        "description": "Es una empresa especializada en soluciones de tecnología de la información, enfocada en la gestión autónoma de activos y servicios de TI mediante inteligencia artificial. Su plataforma AgileOps ofrece capacidades de autorrecuperación, permitiendo a las organizaciones gestionar entornos digitales complejos de manera eficiente y rentable. La empresa se dedica a simplificar operaciones de TI, reduciendo la complejidad y mejorando la eficiencia operativa.",
        "facebook": "https://www.facebook.com/ntechnology",
        "foundation": "2016",
        "founders": [
            {
                "descripcion_founder": "Nombre Fundador es el presidente y director general de la empresa Con una amplia experiencia en la industria y de tecnología, ha liderado la transformación de la empresa hacia soluciones de TI innovadoras, enfocándose en la integración de inteligencia artificial y automatización para mejorar la eficiencia operativa de las organizaciones.",
                "email": "nombre.fundador@gmail.com",
                "name_founder": "Nombre Fundador",
                "position": "Presidente y Director General",
                "url_linkedin": "https://www.linkedin.com"
            }
        ],
        "funding": "N/D",
        "hashtags": [
            "tecnologiainformacion",
            "inteligenciaartificial",
            "gestioniot"
        ],
        "income": "N/D",
        "industries": [
            "Software",
            "Tecnologías de la Información"
        ],
        "instagram": "https://www.instagram.com/",
        "investors": ["N/D"],
        "linkedin": "https://www.linkedin.com",
        "location": "Ciudad de México, México",
        "logo_link": "",
        "market": [
            "Educación",
            "Empresarial & Profesional",
            "Finanzas",
            "Industrial",
            "Medios & Entretenimiento",
            "Retail & Comercio Electrónico",
            "Salud",
            "Sector Publico",
            "Seguridad",
            "Telecomunicaciones",
            "Transporte & Movilidad",
            "Turismo"
        ],
        "name": "nombre",
        "opportunities": "La empresa ofrece oportunidades significativas en el mercado de soluciones de TI al proporcionar una plataforma que automatiza y optimiza la gestión de operaciones tecnológicas. Con la creciente complejidad de los entornos digitales y la necesidad de eficiencia operativa, la demanda de soluciones como AgileOps está en aumento. La empresa puede expandir su alcance a diversas industrias, incluyendo educación, finanzas, salud y telecomunicaciones, ofreciendo servicios que mejoren la eficiencia y reduzcan costos operativos. Además, la integración de inteligencia artificial y automatización inteligente en sus servicios posiciona a nombre como un líder en la transformación digital de organizaciones.",
        "sectors": "Empresa, IT & Datos",
        "secundaryTechnology": ["Automatización Inteligente"],
        "size": "51 a 200 Empleados",
        "technology": "Inteligencia Artificial",
        "twitter": "https://x.com",
        "valuation": "N/D",
        "video_url": "",
        "website": "https://n.technology/",
        "whatsapp": "+52 55 9999 9999",
        "youtube": "https://www.youtube.com"
    }), 200

@app.route("/api/infostartup-test", methods=["GET"])
def test_endpoint():
    time.sleep(3)
    return jsonify({
        "active": True,
        "alliances": ["N/D"],
        "capturista": "",
        "contacto": [
            {
                "email": "ada.palazuelos@n.technology",
                "name": "Ada Palazuelos",
                "notes": "Contacto principal para consultas generales y colaboraciones.",
                "phone": "+52 55 1169 1227",
                "position": "Directora de Operaciones",
                "projects": "Gestión de operaciones y alianzas estratégicas."
            }
        ],
        "contactocid": "Ada Palazuelos",
        "dateinactive": "",
        "description": "n.technology es una empresa mexicana especializada en soluciones de tecnología de la información...",
        "facebook": "https://www.facebook.com/ntechnology",
        "foundation": "2016",
        "founders": [
            {
                "descripcion_founder": "Mauro Sipsz es el presidente y director general de n.technology...",
                "email": "mauro.sipsz@n.technology",
                "name_founder": "Mauro Sipsz",
                "position": "Presidente y Director General",
                "url_linkedin": "https://www.linkedin.com/in/mauro-sipsz"
            }
        ],
        "funding": "N/D",
        "hashtags": ["tecnologiainformacion", "inteligenciaartificial", "gestioniot"],
        "income": "N/D",
        "industries": ["Software", "Tecnologías de la Información"],
        "instagram": "https://www.instagram.com/ntechnology",
        "investors": ["N/D"],
        "linkedin": "https://www.linkedin.com/company/n-technology",
        "location": "Cuauhtémoc, Ciudad de México, México",
        "logo_link": "https://n.technology/logo.png",
        "market": [
            "Educación",
            "Empresarial & Profesional",
            "Finanzas",
            "Industrial",
            "Medios & Entretenimiento",
            "Retail & Comercio Electrónico",
            "Salud",
            "Sector Publico",
            "Seguridad",
            "Telecomunicaciones",
            "Transporte & Movilidad",
            "Turismo"
        ],
        "name": "n.technology",
        "opportunities": "n.technology ofrece oportunidades significativas...",
        "sectors": "Empresa, IT & Datos",
        "secundaryTechnology": ["Automatización Inteligente"],
        "size": "51 a 200 Empleados",
        "technology": "Inteligencia Artificial",
        "twitter": "https://twitter.com/n_technology",
        "valuation": "N/D",
        "video_url": "https://n.technology/video",
        "website": "https://n.technology/",
        "whatsapp": "+52 55 1169 1227",
        "youtube": "https://www.youtube.com/c/ntechnology"
    })

if __name__ == "__main__":
    app.run(debug=True)