# GENERADOR One Page IA API - Documentación
 
> [!NOTE]
> v1: instancia de modelo integrada a API de Flask con structured output como esquema de respuesta.

> [!NOTE]
> v2: instancia de modelo integrada a API de Flask con structured output como esquema de respuesta con apoyo de un modelo auxiliar en caso de demora o falla en la respuesta.

## Descripción del Proyecto

EL generador One Page IA API es una aplicación Flask que utiliza inteligencia artificial para analizar y extraer información detallada de empresas y startups a partir de sus URLs. La aplicación procesa sitios web corporativos y devuelve información estructurada sobre la empresa, incluyendo datos financieros, tecnológicos, de contacto y corporativos.

## Estructura del Proyecto

```
generadorOnePageIA/
├── app.py                     # Aplicación principal Flask (API)
├── ai_model.py                # Instancia del modelo gpt-4.1-mini con web search activo
├── ai_model_fallback.py       # Instancia del modelo gpt-4.1-mini auxiliar sin web search
├── utils.py                   # Utilidades y funciones validaroas
├── requirements.txt           # Dependencias del proyecto
└── .env                       # Variables de entorno
```

## Instalación y Configuración

### Prerrequisitos
- Python 3.8 o superior
- Cuenta de OpenAI con API key con créditos suficientes (consumo estimado )
- Git (para efectos de clonación del proyecto)

### Pasos de Instalación

1. **Clonar o descargar el proyecto**
   ```bash
   git clone "https://github.com/EdreiJezreel/generadorOnePageIA.git"
   cd proyecto
   ```

2. **Crear un entorno virtual (recomendado)**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # o
   venv\Scripts\activate    # Windows
   ```

3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar variables de entorno**
   - Crear archivo `.env` en la raíz del proyecto
   - Agregar tu API key de OpenAI:
     ```
     OPENAI_API_KEY="tu-api-key-aqui"
     ```

5. **Ejecutar la aplicación**
   ```bash
   python app.py
   ```

La aplicación estará disponible en `http://localhost:5000` puede ser modificado en el `app.py` en caso de ser requerido.

## Endpoints de la API

> [!IMPORTANT]
> ### POST `/api/infostartup`

Extrae información detallada de una empresa a partir de su URL.

#### Parámetros de Entrada
- **Content-Type**: `application/json`
- **Body**:
  ```json
  {
    "url": "https://ejemplo.com"
  }
  ```

#### Respuesta Exitosa (200)
```json
{
  "name": "Nombre de la empresa",
  "logo_link": "URL del logo",
  "website": "URL del sitio web",
  "description": "Descripción detallada...",
  "hashtags": ["tag1", "tag2", "tag3"],
  "foundation": "Año de fundación",
  "location": "Ubicación",
  "size": "Tamaño en empleados",
  "sectors": "Sector principal",
  "industries": ["Industria1", "Industria2"],
  "technology": "Tecnología primaria",
  "secundaryTechnology": ["Tech1", "Tech2"],
  "market": ["Mercado1", "Mercado2"],
  "income": "Ingresos anuales",
  "funding": "Fondos recaudados",
  "valuation": "Valoración",
  "opportunities": "Oportunidades de negocio...",
  "investors": ["Inversor1", "Inversor2"],
  "video_url": "URL de video corporativo",
  "linkedin": "URL LinkedIn",
  "twitter": "URL Twitter/X",
  "youtube": "URL YouTube",
  "instagram": "URL Instagram",
  "facebook": "URL Facebook",
  "whatsapp": "Número WhatsApp",
  "alliances": ["Alianza1", "Alianza2"],
  "founders": [
    {
      "name_founder": "Nombre",
      "position": "Puesto",
      "descripcion_founder": "Descripción...",
      "url_linkedin": "URL LinkedIn",
      "email": ""
    }
  ],
  "contacto": [
    {
      "name": "Nombre contacto",
      "email": "email@empresa.com",
      "phone": "Teléfono",
      "position": "Puesto",
      "notes": "",
      "projects": ""
    }
  ],
  "active": true,
  "dateinactive": "",
  "contactocid": "Ada Palazuelos",
  "capturista": ""
}
```

#### Códigos de Error

- **400**: 
  - Cuerpo de solicitud no es JSON
  - Campo 'url' faltante
  - URL no válida

- **404**: Ruta no encontrada

- **500**: 
  - Error interno del servidor
  - Error de formato JSON en la respuesta

## Funciones Principales

### `app.py`
Aplicación de Flask para los endpoints de ejecución del modelo y de pruebas.

#### `validar_url(url: str) -> bool`
Valida el formato de una URL utilizando la librería `validators`.

#### `api_empresa()`
Endpoint principal que procesa las solicitudes POST para extraer información de empresas.

#### `not_found(e)`
Manejador de errores 404 para rutas no encontradas.

### `ai_model.py`
Corresponde a la invocación del modelo principal por medio del API de OpenAI.

### `ai_model_fallback.py`
Corresponde a la invocación del modelo auxiliar por medio del API de OpenAI.

#### `get_info_startup(input_text: str)`
Función principal que interactúa con la API de OpenAI para analizar la URL proporcionada y extraer información estructurada de la empresa.

**Características:**
- Utiliza GPT-4.1-mini con búsqueda web habilitada
- Esquema JSON estricto para respuestas consistentes como structured output
- System prompt implementado
- Análisis de múltiples dimensiones empresariales
- Validación de datos y relaciones entre categorías

### `utils.py`

#### `validar_url(url: str) -> bool`
Función auxiliar que verifica si una URL tiene formato válido.

## Esquema de Datos

La API devuelve información estructurada en las siguientes categorías:

### Información Básica
- Nombre, logo, sitio web, descripción
- Hashtags relevantes, año de fundación, ubicación

### Tamaño y Sector
- Rango de empleados
- Sector principal e industrias específicas

### Tecnología
- Tecnología primaria y tecnologías secundarias relacionadas
- Mercados objetivo

### Finanzas
- Ingresos anuales, fondos recaudados, valoración
- Oportunidades de negocio
- Lista de inversionistas

### Redes Sociales y Contacto
- URLs de redes sociales (LinkedIn, X, YouTube, etc.)
- Información de contacto y WhatsApp
- Alianzas estratégicas

### Fundadores y Equipo
- Información detallada de fundadores
- Datos de contacto corporativo

### Metadatos del Sistema
- Estado activo/inactivo
- Información de captura y contacto CID

## Configuración del Modelo AI

- **Modelo**: GPT-4.1-mini
- **Temperatura**: 0.4 (para respuestas consistentes)
- **Tokens máximos**: 11,000
- **Búsqueda web**: Habilitada con contexto alto
- **Ubicación**: México, Ciudad de México

## Validaciones

- Validación estricta de formato URL
- Esquema JSON con propiedades requeridas
- Validación de enumeraciones para sectores, industrias y tecnologías
- Relaciones jerárquicas entre categorías principales y secundarias
- Longitudes mínimas para descripciones

## Dependencias

- **Flask**: Framework web
- **OpenAI**: Cliente para API de OpenAI
- **python-dotenv**: Manejo de variables de entorno
- **validators**: Validación de formatos de URL

## Manejo de Excepciones

### Excepciones en `app.py`

#### `JSONDecodeError`
- **Causa**: Respuesta de OpenAI no es un JSON válido
- **Manejo**: Retorna error 500 con mensaje descriptivo
- **Solución**: Verificar la respuesta del modelo AI

#### `Exception` General
- **Causa**: Cualquier error no capturado específicamente
- **Manejo**: Retorna error 500 con detalles del error
- **Solución**: Revisar logs para diagnóstico del error

### Excepciones en `ai_model.py`

#### `JSONDecodeError` en Procesamiento de Respuesta
- **Causa**: La salida del modelo no puede ser parseada como JSON
- **Manejo**: Retorna objeto de error con respuesta original
- **Solución**: Validar el formato de salida del prompt

#### `Exception` en Llamada a OpenAI
- **Causa**: Error de conexión, autenticación o quota excedido
- **Manejo**: Propaga la excepción para manejo en capa superior
- **Solución**: Verificar API key, conexión a internet y límites de uso

### Excepciones en `utils.py`

#### `ValidationFailure` (de la librería validators)
- **Causa**: URL con formato inválido
- **Manejo**: Retorna `False` en la validación
- **Solución**: Usuario debe proporcionar URL válida

### Posibles Excepciones del Sistema

#### `ModuleNotFoundError`
- **Causa**: Dependencias no instaladas
- **Solución**: Ejecutar `pip install -r requirements.txt`

#### `KeyError` (Variables de entorno)
- **Causa**: `OPENAI_API_KEY` no configurada
- **Solución**: Verificar archivo `.env` y variables de entorno

#### `OSError`
- **Causa**: Problemas de acceso al sistema de archivos
- **Solución**: Verificar permisos y existencia de archivos

#### `ConnectionError`
- **Causa**: Problemas de conectividad con API de OpenAI
- **Solución**: Verificar conexión a internet y firewall

### Manejo de Excepciones Específicas de OpenAI

#### `openai.APIError`
- **Causa**: Error interno del servidor de OpenAI
- **Manejo**: Reintentar después de un tiempo

#### `openai.APIConnectionError`
- **Causa**: Problemas de conexión con OpenAI
- **Manejo**: Verificar conectividad y reintentar

#### `openai.RateLimitError`
- **Causa**: Límite de requests excedido
- **Manejo**: Implementar backoff exponencial

#### `openai.AuthenticationError`
- **Causa**: API key inválida o expirada
- **Manejo**: Solicitar nueva API key

## Notas de Uso

- La aplicación está configurada en modo debug para desarrollo
- Requiere conexión a internet para la búsqueda web
- El procesamiento puede tomar varios segundos dependiendo de la complejidad (de 15 a 30 segundos)
- Los campos opcionales devuelven "N/D" cuando la información no está disponible
- **Importante**: Todas las excepciones son registradas y manejadas apropiadamente para evitar caídas del servicio

## Solución de Problemas

### Error: "OPENAI_API_KEY no encontrada"
- Verificar que el archivo `.env` exista y contenga la clave correcta
- Confirmar que la variable esté accesible en el entorno

### Error: "URL no válida"
- Asegurarse que la URL incluya protocolo (http:// o https://)
- Verificar que la URL sea accesible públicamente

### Error: "Error de formato JSON"
- El modelo AI podría estar devolviendo respuestas mal formadas
- Verificar los límites de tokens y el esquema correcto del prompt (correspondiente al commit inicial)

### Error: "Timeout o conexión rechazada"
- Verificar conectividad a internet
- Confirmar que los servicios de OpenAI estén operativos

## Consideraciones de Seguridad

- Nunca hacer commit con el archivo `.env` con claves reales
- Validar y sanitizar todas las entradas del usuario
- Implementar rate limiting en producción
- Usar HTTPS en entornos de producción

> [!IMPORTANT]
> ### GET `/api/infostartup-test`

Endpoint de prueba que simula la respuesta del sistema de extracción de información de startups, devolviendo datos estáticos de ejemplo con una latencia artificial.

#### Propósito
Proporcionar datos de prueba predefinidos para desarrollo, testing y demostración del formato de respuesta esperado.

#### Comportamiento
- **Simulación de latencia**: Introduce un retraso artificial de 3 segundos (`time.sleep(3)`)
- **Datos estáticos**: Siempre devuelve la misma información de "n.technology"
- **Solo desarrollo**: No debe usarse en entornos de producción

#### Respuesta Exitosa (200)
```json
{
  "active": true,
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
}
```
#### Notas de Uso
- **Exclusivo para desarrollo**: No utilizar en producción
- **Latencia artificial**: 3 segundos de delay intencional
- **Datos estáticos**: Misma respuesta en cada solicitud

#### Casos de Uso Recomendados
1. Pruebas de frontend y desarrollo
2. Validación de estructuras de datos
3. Demostraciones del sistema
4. Testing de integración
5. Documentación de formato de respuesta
