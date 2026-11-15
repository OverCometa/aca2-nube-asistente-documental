# ACA2 · Asistente documental educativo
Over Santiago Cometa Hernández · CUN · Computación en la Nube · Grupo 14

## Estado comprobado
Repositorio público: https://github.com/OverCometa/aca2-nube-asistente-documental

Se verificó la colección original de Qdrant Cloud `aca1_permanencia_documental_v1`:384 dimensiones y 26 de 26 fragmentos coincidentes con ACA1. Se ejecutaron cuatro consultas con recuperación cloud y generación local Qwen2.5-1.5B-Instruct-GGUF Q4_K_M mediante llama.cpp b12400. El modelo se llamó tres veces; una consulta se abstuvo antes de generación. No se modificó la colección.

Esta versión habilita generación local en el servidor con Qwen1.5B cuantizado, sin API de pago ni claves. Por defecto recupera el corpus en Qdrant en memoria y genera con llama.cpp. La primera consulta descarga los modelos oficiales (aproximadamente1.4GB) con integridad verificada. La operación en el alojamiento público debe verificarse tras desplegar; el límite de memoria puede impedirla. URL: https://aca2-nube-asistente-overcometa.streamlit.app/ .

El modo Qdrant Cloud requiere acceso privado efímero: un formulario explica que la clave se transmite al servidor Streamlit y permanece en RAM del cliente de esa sesión, no en archivos ni Secrets. Solo debe utilizarse con autorización explícita. El campo de clave se vacía tras conectar; Desconectar retira el cliente del estado. A los15min se rechazan nuevas consultas hasta reconectar. No se comparte el cliente entre sesiones ni se escribe la clave en variables globales. Esto no vuelve permanente ni autónoma la conexión cloud pública.

## Evidencia incluida
- `results/cloud_rag_acceptance.json`: cuatro consultas reales cloud+LLM local y comprobación del corpus.
- `results/cloud_preflight.json`:26/26 fragmentos,384 dimensiones.
- `results/auditoria_cloud_independiente.txt`: contraste humano con las fuentes, sin repetir llamadas remotas.
- `results/regression_restored_environment.txt`:19 pruebas de software aprobadas; no son 19 consultas cloud.
- `notebook/ACA2_Computacion_Nube.ipynb`: salidas diagnósticas históricas y sección posterior que lee el reporte cloud real, diferenciadas.

| Consulta | Resultado observado |
|---|---|
| Organización del estudio | Respuesta fiel a F1, pero más larga que el límite solicitado |
| Solicitud de beca | Contenido coherente del modelo sin citas; el filtro lo bloqueó por formato, no por falta de evidencia |
| Tasa de financiación | Reconoce correctamente que el dato no está, con marcadores adicionales sin explicación |
| Fecha específica de becas | Abstención durante recuperación, sin llamar al LLM |

Esta muestra no mide precisión general. Las citas se validan sintácticamente, no garantizan fidelidad; se requiere revisión humana. Las tres guías son material didáctico propio, no normativa oficial de CUN. El dataset UCI697 es público y de Portugal; su asociación es temática y no enlaza personas con guías colombianas.

## Instalación y demostración sin credenciales
Python 3.12. Desde la raíz:
```bash
python -m venv .venv
# Activar: Windows .venv\Scripts\activate; Linux/macOS source .venv/bin/activate
pip install -r requirements.txt
python -m pytest -q
streamlit run app.py
```
Para diagnóstico sin modelo, seleccionar Local y Sin LLM. Para chatbot gratuito, seleccionar Qdrant local y llama.cpp. Probar «¿Cómo organizar el estudio semanal?» y revisar fuentes/panel documental. `python evaluate.py` ejecuta evaluación diagnóstica local y genera su propio reporte; no atribuir ese resultado a cloud.

## Repetir la integración cloud+LLM local
Se requiere acceso privado autorizado a la colección original. No se comparte la clave temporal usada en la prueba. Configurar QDRANT_URL y QDRANT_API_KEY en el entorno del proceso, sin publicarlas ni mostrarlas en video. La colección se consulta solo en lectura. Ejecutar `python check_cloud.py` antes de la evaluación.

Descargar el binario oficial de llama.cpp para el sistema y el modelo GGUF por separado; no están en este repositorio:
- https://github.com/ggml-org/llama.cpp/releases/tag/b12400
- https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct-GGUF/resolve/main/qwen2.5-1.5b-instruct-q4_k_m.gguf

Configurar LLAMA_CPP_BIN y GGUF_MODEL_PATH con rutas locales absolutas. Ejecutar `python verify_cloud_rag.py`. Se probó Linux CPU, no Windows. Los modos API/Ollama/HuggingFace son alternativas configurables, no rutas acreditadas por la evidencia cloud incluida. No introducir claves en el chat de la app.

## Arquitectura y controles
Pregunta → MiniLM multilingüe del ACA1 → Qdrant Top-k → párrafos originales completos → LLM → control de citas → respuesta y fuentes. Se conservan fragmentos, identificadores y hashes. La expansión evita cortar negaciones; una prueba comprueba el caso detectado. SQLite puede reconstruir el catálogo local. La UI ofrece historial, panel documental y resultados.

## Pendientes de entrega
- Verificar generación real tras desplegar esta versión y, solo si está autorizado, probar conexión cloud efímera. Las pruebas cloud anteriores corresponden a otra ejecución y no demuestran por sí solas el alojamiento público.
- Video personal de sustentación de 3–5 min y enlaces finales en póster.
- Revisión de las limitaciones de generación. No declarar calidad de producción.
No se ha enviado la actividad en CDigital.

## Referencias
Proyecto ACA1: https://github.com/OverCometa/aca1-nube-busqueda-semantica

Lewis, P., et al.(2020). Retrieval-augmented generation for knowledge-intensive NLP tasks. NeurIPS33. https://arxiv.org/abs/2005.11401

Qdrant. Documentation. https://qdrant.tech/documentation/

Cometa Hernández, O.S.(2026). Tres guías didácticas de orientación educativa. Material propio incluido en corpus/.

## Recursos y seguridad de ejecución
Los binarios y pesos se descargan de lanzamientos oficiales fijados por SHA256. No se suben al repositorio. La aplicación serializa consultas para evitar ejecutar varios modelos simultáneamente y libera el encoder antes de generar para reducir memoria. La descarga inicial tarda más que las consultas siguientes. Los usuarios reciben un aviso si el servidor está ocupado o una consulta falla. Las pruebas locales no garantizan disponibilidad ni rendimiento de Streamlit gratuito.
