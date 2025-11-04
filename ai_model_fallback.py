import os
import json
from openai import OpenAI

def get_info_startup_fallback(input_text: str):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {
                "role": "system",
                "content": [
                    {
                        "type": "input_text",
                        "text": (
                            "ERES UN ANALISTA DE EMPRESAS Y MERCADOTECNIA. "
                            "DADA UNA URL, GENERA UN OBJETO JSON COMPLETO CON LA INFORMACIÓN CORPORATIVA "
                            "DE ESA EMPRESA BASADO EN EL SCHEMA ESTABLECIDO. "
                            "NO REALICES BÚSQUEDAS EXTERNAS. BASA LA INFORMACIÓN EN EL NOMBRE Y DOMINIO "
                            "DE LA EMPRESA, Y EN SUPOSICIONES COHERENTES Y PLAUSIBLES. "
                            "SI FALTAN DATOS, COMPLETA CON 'N/D'. "
                            "LA ESTRUCTURA Y CAMPOS DEBEN SEGUIR EXACTAMENTE EL SCHEMA DEFINIDO A CONTINUACIÓN. "
                            "EL JSON DEBE SER VÁLIDO Y ESTRICTAMENTE CUMPLIR EL FORMATO."
                        )
                    }
                ]
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": input_text
                    }
                ]
            }
        ],
        text={
            "format": {
                "type": "json_schema",
                "name": "company_info",
                "strict": True,
                "schema": {
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "Nombre completo de la empresa",
                        },
                        "logo_link": {
                            "type": "string",
                            "description": "URL del logo de la empresa"
                        },
                        "website": {
                            "type": "string",
                            "description": "URL del sitio web oficial de la empresa"
                        },
                        "description": {
                            "type": "string",
                            "minLength": 120,
                            "description": "Descripción detallada de la empresa a modo de resumen ejecutivo, debe tener al menos 120 palabras describiendo su negocio, misión y valores"
                        },
                        "hashtags": {
                            "type": "array",
                            "items": {
                                "type": "string"
                            },
                            "minItems": 3,
                            "description": "Hashtags relacionados con la empresa. Debe incluir al menos DOS hashtags relevantes, solo usa minpusculas, sin acentos y sin espacios, no uses caractres especiales, NO COLOQUES EL # AL INICIO"
                        },
                        "foundation": {
                            "type": "string",
                            "description": "Año de fundación de la empresa"
                        },
                        "location": {
                            "type": "string",
                            "description": "Ubicación de la sede principal de la empresa"
                        },
                        "size": {
                            "type": "string",
                            "enum": [
                                "0 a 10 Empleados",
                                "11 a 50 Empleados",
                                "51 a 200 Empleados",
                                "201 a 500 Empleados",
                                "501 a 1,000 Empleados",
                                "1,000 a 5,000 Empleados",
                                "5,000 a 10,000 Empleados",
                                "+10,000 Empleados"
                            ],
                            "description": "Tamaño de la empresa en número de empleados. Debe seleccionar UNO de los siguientes valores: 0 a 10 Empleados, 11 a 50 Empleados, 51 a 200 Empleados, 201 a 500 Empleados, 501 a 1,000 Empleados, 1,000 a 5,000 Empleados, 5,000 a 10,000 Empleados, +10,000 Empleados"
                        },
                        "sectors": {
                            "type": "string",
                            "enum": [
                                "Contenido y Medios",
                                "Empresa, IT & Datos",
                                "Energía",
                                "FinTech",
                                "Retail & Mercadotecnia",
                                "Salud",
                                "Sustentabilidad",
                                "Tecnología Industrial",
                                "Tecnologías de Seguridad",
                                "Transporte & Logística"
                            ],
                            "description": "Sector principal de la empresa. Identifica corretamente el sector al que pertenece Solo se puede seleccionar UNO de estos sectores. IMPORTANTE: Las industrias seleccionadas deben corresponder exclusivamente a este sector."
                        },
                        "industries": {
                            "type": "array",
                            "items": {
                                "type": "string",
                                "enum": [
                                    "Cultura",
                                    "Educación",
                                    "Entretenimiento",
                                    "Eventos",
                                    "Producción Audiovisual",
                                    "Administración de Empresas",
                                    "Datos",
                                    "Software",
                                    "Tecnologías de la Información",
                                    "Telecomunicaciones",
                                    "Energías no Renovables",
                                    "Energías Renovables",
                                    "Administración de Bienes",
                                    "Administración Financiera",
                                    "Análisis y Puntaje Crediticio",
                                    "Banca Digital",
                                    "Billeteras Móviles y Remesas",
                                    "Core Bancario e Infraestructura",
                                    "Criptomonedas",
                                    "Financiamiento e Inversión",
                                    "Financiamiento y Préstamos Empresariales",
                                    "Finanzas Personales",
                                    "Inmobiliaria e Hipoteca",
                                    "Mercado de Capital",
                                    "Nómina y Prestaciones",
                                    "Normativa y Cumplimiento",
                                    "Préstamo al Consumo",
                                    "Préstamos en General",
                                    "Procesamiento de Pagos",
                                    "Punto de Venta",
                                    "Seguros",
                                    "Servicios Financieros y Automatización",
                                    "Transferencias Electrónicas",
                                    "Análisis de Mercadotecnia",
                                    "Comercio Electrónico",
                                    "Gestión de Mercadotecnia",
                                    "Retail",
                                    "Bienestar",
                                    "Biomedicina",
                                    "Gestión Médica",
                                    "Tecnología Sanitaria",
                                    "Desarrollo Sustentable",
                                    "Optimización de Empresas",
                                    "Tecnologías Sustentables",
                                    "Renta de Espacios",
                                    "Tecnologías de la Construcción",
                                    "Ciberseguridad",
                                    "Privacidad y Seguridad Digital",
                                    "Protección de datos",
                                    "Sistemas de Monitoreo",
                                    "Logística",
                                    "Tecnologías de Movilidad",
                                    "Transporte"
                                ]
                            },
                            "minItems": 2,
                            "description": "Industrias dentro del sector seleccionado. Debe seleccionar al menos UNA industria que corresponda EXCLUSIVAMENTE al sector elegido en 'sectors'. NO mezclar industrias de diferentes sectores. NO SOLO SELECCIONES CIBERSEGURIDAD, DETERMINA LA O LAS CORRECTAS CATÁLOGOS POR SECTOR: Contenido y Medios->Cultura,Educación,Entretenimiento,Eventos,Producción Audiovisual | Empresa, IT & Datos->Administración de Empresas,Datos,Software,Tecnologías de la Información,Telecomunicaciones | Energía->Energías no Renovables,Energías Renovables | FinTech->Administración de Bienes,Administración Financiera,Análisis y Puntaje Crediticio,Banca Digital,Billeteras Móviles y Remesas,Core Bancario e Infraestructura,Criptomonedas,Financiamiento e Inversión,Financiamiento y Préstamos Empresariales,Finanzas Personales,Inmobiliaria e Hipoteca,Mercado de Capital,Nómina y Prestaciones,Normativa y Cumplimiento,Préstamo al Consumo,Préstamos en General,Procesamiento de Pagos,Punto de Venta,Seguros,Servicios Financieros y Automatización,Transferencias Electrónicas | Retail & Mercadotecnia->Análisis de Mercadotecnia,Comercio Electrónico,Gestión de Mercadotecnia,Retail | Salud->Bienestar,Biomedicina,Gestión Médica,Tecnología Sanitaria | Sustentabilidad->Desarrollo Sustentable,Optimización de Empresas,Tecnologías Sustentables | Tecnología Industrial->Renta de Espacios,Tecnologías de la Construcción | Tecnologías de Seguridad->Ciberseguridad,Privacidad y Seguridad Digital,Protección de datos,Sistemas de Monitoreo | Transporte & Logística->Logística,Tecnologías de Movilidad,Transporte"
                        },
                        "technology": {
                            "type": "string",
                                "enum": [
                                    "Almacenamiento de Datos",
                                    "Biotecnología",
                                    "Computación Cuántica",
                                    "Comunicación",
                                    "Criptografía",
                                    "Inteligencia Artificial",
                                    "Maquinaria y Robótica",
                                    "Plataformas & Interfaces",
                                    "Semiconductores & Electricidad",
                                    "Sensores",
                                    "Simulación & Imagen",
                                    "Tecnología de Infraestructura"
                                ],
                            "description": "Tecnología primaria de la empresa. Solo se puede seleccionar UNA tecnología principal. IMPORTANTE: Las tecnologías secundarias seleccionadas deben corresponder exclusivamente a esta tecnología primaria."
                        },
                        "secundaryTechnology": {
                            "type": "array",
                            "items": {
                                "type": "string",
                                "enum": [
                                    "Blockchain",
                                    "Nube",
                                    "Celular",
                                    "Genética",
                                    "Microorganismos",
                                    "Molecular",
                                    "Ocular",
                                    "Computación Cuántica",
                                    "5G",
                                    "Drones",
                                    "Fibra Óptica",
                                    "Identificación por Radiofrecuencia",
                                    "Inalámbrico",
                                    "Internet de las Cosas",
                                    "Móvil",
                                    "Operador Móvil Virtual",
                                    "Satelital",
                                    "Sistemas de Localización en Tiempo Real",
                                    "Criptomoneda",
                                    "Encriptación",
                                    "Análisis de Matices Digitales",
                                    "Análisis del Discurso",
                                    "Análisis Predictivo",
                                    "Aprendizaje Automático",
                                    "Aprendizaje Profundo",
                                    "Automatización Inteligente",
                                    "Diseño Conversacional",
                                    "Personalización de Procesos",
                                    "Plataforma de Inteligencia Artificial",
                                    "Procesamiento de Lenguajes Naturales",
                                    "Reconocimiento de Imagen",
                                    "Automatización Robótica de Procesos",
                                    "Dispositivos Usables",
                                    "Impresión 3D",
                                    "Robot de Asistencia",
                                    "Robótica Industrial",
                                    "Interfaz de Programación de Aplicaciones",
                                    "Motor de Búsqueda",
                                    "Plataformas Web",
                                    "Plugin",
                                    "Software",
                                    "Chiplets",
                                    "Acústico",
                                    "Detección por Luz y Distancia",
                                    "Inalámbricos",
                                    "Movimiento",
                                    "Radares Análogos",
                                    "Sensores Faciales",
                                    "Diseño Asistido por Computadora",
                                    "Efectos Visuales",
                                    "Imágenes Generadas por Computadora",
                                    "Ingeniería Asistida por Computadora",
                                    "Realidad Aumentada",
                                    "Realidad Extendida",
                                    "Realidad Virtual",
                                    "Simulación 3D",
                                    "Renderización Personalizable",
                                    "Infraestructura Petrolera"
                                ]
                            },
                            "minItems": 1,
                            "description": "Tecnologías secundarias relacionadas con la tecnología primaria seleccionada. Debe seleccionar al menos UNA tecnología secundaria que corresponda EXCLUSIVAMENTE a la tecnología primaria elegida. NO mezclar tecnologías de diferentes categorías primarias. CATÁLOGOS POR TECNOLOGÍA PRIMARIA: Almacenamiento de Datos->Blockchain,Nube | Biotecnología->Celular,Genética,Microorganismos,Molecular,Ocular | Computación Cuántica->Computación Cuántica | Comunicación->5G,Drones,Fibra Óptica,Identificación por Radiofrecuencia,Inalámbrico,Internet de las Cosas,Móvil,Operador Móvil Virtual,Satelital,Sistemas de Localización en Tiempo Real | Criptografía->Criptomoneda,Encriptación | Inteligencia Artificial->Análisis de Matices Digitales,Análisis del Discurso,Análisis Predictivo,Aprendizaje Automático,Aprendizaje Profundo,Automatización Inteligente,Diseño Conversacional,Personalización de Procesos,Plataforma de Inteligencia Artificial,Procesamiento de Lenguajes Naturales,Reconocimiento de Imagen | Maquinaria y Robótica->Automatización Robótica de Procesos,Dispositivos Usables,Impresión 3D,Robot de Asistencia,Robótica Industrial | Plataformas & Interfaces->Interfaz de Programación de Aplicaciones,Motor de Búsqueda,Plataformas Web,Plugin,Software | Semiconductores & Electricidad->Chiplets | Sensores->Acústico,Detección por Luz y Distancia,Inalámbricos,Movimiento,Radares Análogos,Sensores Faciales | Simulación & Imagen->Diseño Asistido por Computadora,Efectos Visuales,Imágenes Generadas por Computadora,Ingeniería Asistida por Computadora,Realidad Aumentada,Realidad Extendida,Realidad Virtual,Simulación 3D,Renderización Personalizable | Tecnología de Infraestructura->Infraestructura Petrolera"
                        },
                        "market": {
                            "type": "array",
                            "items": {
                                "type": "string",
                                "enum": [
                                    "Aeroespacial",
                                    "Conectividad de Energía",
                                    "Consumo",
                                    "Educación",
                                    "Emprendimiento",
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
                                ]
                            },
                            "minItems": 1,
                            "description": "Mercados objetivo de la empresa. Puede seleccionar UNO o MÚLTIPLES mercados"
                        },
                        "income": {
                            "type": "string",
                            "description": "Ingresos anuales de la empresa,si no está disponible coloca N/D. Formato de ejemplo: 150M USD"
                        },
                        "funding": {
                            "type": "string",
                            "description": "Fondos recaudados por la empresa, si no está disponible coloca N/D. Formato de ejemplo: 150M USD"
                        },
                        "valuation": {
                            "type": "string",
                            "description": "Valoración de la empresa, si no está disponible coloca N/D. Formato de ejemplo: 150M USD"
                        },
                        "opportunities": {
                            "type": "string",
                            "minLength": 150,
                            "description": "Oportunidades de negocio y crecimiento, debe tener al menos 150 palabras describiendo las oportunidades del mercado"
                        },
                        "investors": {
                            "type": "array",
                                "items": {
                                    "type": "string"
                                },
                                "minItems": 1,
                                "description": "Lista de inversionistas de la empresa. Debe incluir al menos UN inversionista"
                        },
                        "video_url": {
                            "type": "string",
                            "description": "URL de video corporativo o promocional"
                        },
                        "linkedin": {
                            "type": "string",
                            "description": "URL del perfil de LinkedIn de la empresa"
                        },
                        "twitter": {
                            "type": "string",
                            "description": "URL del perfil de Twitter/X de la empresa"
                        },
                        "youtube": {
                            "type": "string",
                            "description": "URL del canal de YouTube de la empresa"
                        },
                        "instagram": {
                            "type": "string",
                            "description": "URL del perfil de Instagram de la empresa"
                        },
                        "facebook": {
                            "type": "string",
                            "description": "URL del perfil de Facebook de la empresa"
                        },
                        "whatsapp": {
                            "type": "string",
                            "description": "Número de WhatsApp de contacto"
                        },
                        "alliances": {
                            "type": "array",
                            "items": {
                                "type": "string"
                            },
                            "minItems": 1,
                            "description": "Alianzas estratégicas de la empresa. Debe incluir al menos UNA alianza"
                        },
                        "founders": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "name_founder": {
                                        "type": "string",
                                        "description": "Nombre completo del fundador"
                                    },
                                    "position": {
                                        "type": "string",
                                        "description": "Puesto del fundador en la empresa"
                                    },
                                    "descripcion_founder": {
                                        "type": "string",
                                        "minLength": 50,
                                        "description": "Breve descripción del fundador, debe tener al menos 50 palabras"
                                    },
                                    "url_linkedin": {
                                        "type": "string",
                                        "description": "URL del perfil de LinkedIn del fundador"
                                    },
                                    "email": {
                                        "type": "string",
                                        "format": "email",
                                        "description": "Email del fundador, debe dejarse vacío"
                                    },
                                },
                                "required": ["name_founder","position","descripcion_founder","url_linkedin","email"],
                                "propertyOrdering": ["name_founder", "position", "descripcion_founder", "url_linkedin", "email"], 
                                "additionalProperties": False
                            },
                            "minItems": 1,
                            "description": "Lista de fundadores de la empresa"
                        },
                        "contacto": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "name": {
                                        "type": "string",
                                        "description": "Nombre de la persona para el contacto de la empresa"
                                    },
                                    "email": {
                                        "type": "string",
                                        "format": "email",
                                        "description": "Email del contacto"
                                    },
                                    "phone": {
                                        "type": "string",
                                        "description": "Número de teléfono del contacto"
                                    },
                                    "position": {
                                        "type": "string",
                                        "description": "Puesto del contacto"
                                    },
                                    "notes": {
                                        "type": "string",
                                        "description": "Notas adicionales del contacto, debe dejarse vacío"
                                    },
                                    "projects": {
                                        "type": "string",
                                        "description": "Proyectos del contacto, debe dejarse vacío"
                                    }
                                },
                                "required": [
                                    "name",
                                    "email",
                                    "phone",
                                    "position",
                                    "notes",
                                    "projects"
                                ],
                                "propertyOrdering": ["name", "email", "phone", "position", "notes", "projects"],
                                "additionalProperties": False
                            },
                            "minItems": 1,
                            "description": "Información de contacto de la empresa, puede ser de uno de sus integrantes"
                        },
                        "active": {
                            "type": "boolean",
                            "description": "Estado activo de la empresa. siempre debe ser True"
                        },
                        "dateinactive": {
                            "type": "string",
                            "description": "Fecha de inactividad, debe dejarse vacío si está activa"
                        },
                        "contactocid": {
                            "type": "string",
                            "const": "Ada Palazuelos",
                            "description": "Contacto principal CID, siempre debe ser 'Ada Palazuelos'"
                        },
                        "capturista": {
                            "type": "string",
                            "description": "Persona o sistema que capturó la información, siempre es vacío"
                        },
                    },
                    "required": [
                        "name", "logo_link", "website", "description", "hashtags", "foundation", "location", "size", 
                        "sectors", "industries", "technology", "secundaryTechnology", "market", "income", "funding", 
                        "valuation", "opportunities", "investors", "video_url", "linkedin", "twitter", "youtube", 
                        "instagram", "facebook", "whatsapp", "alliances", "founders", "contacto", "active", 
                        "dateinactive", "contactocid", "capturista"
                    ],
                    "propertyOrdering": [
                        "name", "logo_link", "website", "description", "hashtags", "foundation", "location", "size", 
                        "sectors", "industries", "technology", "secundaryTechnology", "market", "income", "funding", 
                        "valuation", "opportunities", "investors", "video_url", "linkedin", "twitter", "youtube", 
                        "instagram", "facebook", "whatsapp", "alliances", "founders", "contacto", "active", 
                        "dateinactive", "contactocid", "capturista"
                    ],
                    "additionalProperties": False,
                    "description": "Esquema completo para la creación de registros de empresas en el sistema CID. Incluye información corporativa, financiera, de contacto y tecnológica."   
                }
            }
        },
        temperature=0.2,
        max_output_tokens=4000,
        top_p=0.9,
        store=False
    )
    try:
        json_output = json.loads(response.output_text)
    except Exception:
        json_output = {
            "error": "No se pudo convertir la respuesta a JSON válido en fallback.",
            "raw_response": response.output_text
        }
    return response.output_text
