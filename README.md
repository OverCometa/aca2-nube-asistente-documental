# Publicación académica ACA2 · Estado de la demostración
Esta copia pública no contiene claves ni datos personales de estudiantes. La app arranca en diagnóstico local sin LLM; ese modo no se presenta como la integración cloud completa. El reporte `results/cloud_rag_acceptance.json` conserva la prueba real de la colección original Qdrant Cloud y llama.cpp local. No hay API de pago configurada ni acceso cloud público automático. Para reproducir esa prueba se requiere acceso privado autorizado; no introducir claves en el chat.

# ACA 2 · Asistente documental educativo
**Over Santiago Cometa Hernández · CUN · Computación en la Nube · Grupo 14**

## Objetivo y continuidad
Integrar un LLM con la recuperación del ACA 1 para orientación educativa sustentada. Se conservan las tres guías propias, identificadores de fragmentos, modelo de embeddings y colección `aca1_permanencia_documental_v1`. Las guías no son reglamentos institucionales. Dataset UCI 697 de Portugal: asociación temática, no correspondencia entre personas y guías.

## Arquitectura
Pregunta → recuperación Top-k → contexto con identificadores F1…Fk → LLM → validación sintáctica de citas → respuesta y fuentes. Streamlit proporciona historial y consulta documental; SQLite conserva el catálogo.

- Ruta final: Qdrant Cloud y embeddings multilingües MiniLM del ACA 1; LLM mediante Ollama o API compatible.
- Ruta diagnóstica sin conexión: TF-IDF local y fragmentos literales. **No constituye RAG generativo ni reemplaza la validación cloud.** No se presenta como resultado de un modelo de lenguaje.
- La colección remota se consulta en lectura: la aplicación no borra ni reindexa datos.

## Instalación
Python 3.12. Desde la carpeta del proyecto:
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
python evaluate.py
python -m pytest -q
streamlit run app.py
```
Copiar `.env.example` a `.env` **solo localmente**. Para Qdrant, recuperar la URL y clave del clúster del ACA1. No compartirlas ni incluirlas en ZIP/GitHub. Para Ollama, instalarlo de su sitio oficial y descargar un modelo disponible (`ollama pull qwen2.5:3b`). Para API usar proveedor, modelo y clave propios. El nombre del modelo y su disponibilidad deben comprobarse en el proveedor.

Para evaluación integral:
```bash
python evaluate.py --mode cloud --provider ollama
# o: python evaluate.py --mode cloud --provider api
```
La aplicación lee `.env`; el script de evaluación también lo carga. Variables en `.env.example`. El prompt y los fragmentos se envían al proveedor seleccionado: usar solo corpus autorizado. La configuración API puede generar costos del proveedor. No hay consumo remoto en modo extractivo.

## Demostración (3–5 minutos)
1. Explicar diferencia entre ACA1 (buscador) y ACA2 (respuesta generada con evidencia).
2. Mostrar configuración real, sin claves.
3. Preguntar «¿Cómo organizar el estudio semanal?».
4. Preguntar «¿Qué revisar antes de solicitar una beca?».
5. Abrir las fuentes y mostrar documento, fragmento y origen.
6. Preguntar una fecha de convocatoria no documentada: revisar si el sistema reconoce el límite.
7. Mostrar panel documental y explicar resultados y limitaciones reales.

## Pruebas y límites
`results/evaluation_local_extractive.json` contiene ejecuciones reales exploratorias de recuperación local. Las métricas no deben atribuirse a cloud ni LLM. `tests/test_rag.py` cubre 19 pruebas: corpus, catálogo, consulta vacía, rango Top-k, filtro, recuperación, etiquetado sin LLM, citas y bloqueo de configuración faltante. Se comprobó además Streamlit con AppTest: apertura, pregunta y reinicio sin excepciones.
El umbral de abstención es heurístico, no calibrado. La similitud no es probabilidad de verdad. La validación de citas solo comprueba índices, no que cada afirmación esté implicada por la fuente. Un LLM puede ignorar el prompt: revisión humana obligatoria. La evaluación temática usa seis preguntas internas y una externa, no un benchmark general.

## Estado de entrega
- Código, corpus, notebook, pruebas locales: preparados.
- Qdrant Cloud: original reactivado y probado; 26 de 26 fragmentos coinciden con ACA1, 384 dimensiones.
- LLM: ruta Hugging Face no satisfactoria; alternativa Qwen1.5B cuantizada con llama.cpp ejecutada localmente. Calidad limitada a los casos registrados; ver evaluación v3 y auditoría independiente. Prueba cloud real completada; ver resultados de aceptación.
- Publicación GitHub de ACA2, enlace público de app y video del estudiante: pendientes.
No grabar ni declarar un despliegue o resultado que no haya sido verificado.

## Referencias
Cometa Hernández, O. S. (2026). *Tres guías didácticas de orientación educativa* [Material académico de elaboración propia]. Corpus del ACA1.
Lewis, P., et al. (2020). Retrieval-augmented generation for knowledge-intensive NLP tasks. *Advances in Neural Information Processing Systems, 33*, 9459–9474. https://arxiv.org/abs/2005.11401
Qdrant. (s. f.). *Documentation*. https://qdrant.tech/documentation/
Ollama. (s. f.). *Generate a chat message*. https://docs.ollama.com/api/chat
Ministerio de Educación Nacional. (2023). *Gestión de la permanencia*. https://www.mineducacion.gov.co/sistemasinfo/spadies/secciones/Gestion-de-la-permanencia/
Ministerio de Educación Nacional. (2016). *Lineamientos de política de bienestar para instituciones de educación superior*. https://www.mineducacion.gov.co/1759/articles-360314_recurso.pdf

## Alternativa local generativa (sin clave LLM)
Instalar `pip install -r requirements-local-llm.txt`. El modo `semantic_local` conserva el modelo MiniLM y fragmentos del ACA1 en una colección Qdrant **en memoria**, no en la nube. El proveedor `hf` usa Qwen2.5-0.5B-Instruct en CPU. Primera ejecución descarga pesos (~1.2 GB en total); necesita memoria y red. No sustituye la exigencia de conectar la base cloud del ACA1.
```bash
python evaluate.py --mode semantic_local --provider hf
```
La UI ofrece ambos modos. Solo usar métricas del archivo correspondiente; una muestra pequeña no prueba seguridad ni precisión general.
Qwen Team. (2024). *Qwen2.5-0.5B-Instruct* [Modelo de lenguaje]. https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct

## Ruta cuantizada validada localmente
Después de los fallos anteriores se probó Qwen2.5-1.5B-Instruct **Q4_K_M**, ejecutado por llama.cpp b12400, sin PyTorch. Una consulta sobre organización del estudio produjo una respuesta útil respaldada por los fragmentos F1/F2/F3. Ver `results/probe_quantized_v2.json`; no extrapolar a precisión general ni conexión cloud.

1. Descargar llama.cpp desde la distribución oficial https://github.com/ggml-org/llama.cpp/releases/tag/b12400 y escoger el binario del sistema operativo.
2. Descargar el modelo oficial https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct-GGUF/resolve/main/qwen2.5-1.5b-instruct-q4_k_m.gguf (aproximadamente 1 GB). Los pesos no están dentro del ZIP.
3. Configurar `LLAMA_CPP_BIN` con la ruta absoluta de `llama-completion` (o `llama-completion.exe` en Windows) y `GGUF_MODEL_PATH` con la ruta absoluta al GGUF.
4. Elegir en la aplicación «Qdrant local · embeddings ACA1» y «LLM local · llama.cpp (GGUF)». Primer uso descarga MiniLM. Para cumplir la continuidad cloud, seleccionar Qdrant Cloud **después** de configurar el acceso original y volver a evaluar.
5. Ejecutar `python evaluate.py --mode semantic_local --provider llamacpp` y revisar cada respuesta. Para cloud: `python evaluate.py --mode cloud --provider llamacpp`.

Las rutas de archivo son privadas del computador y no deben apuntar a ejecutables desconocidos. En preparación se probó Linux CPU; Windows no fue ejecutado aquí. No instalar PyTorch para esta alternativa.
Binario oficial Windows CPU x64: https://github.com/ggml-org/llama.cpp/releases/download/b12400/llama-b12400-bin-win-cpu-x64.zip

## Corrección de contexto (revisión 3)
La fragmentación heredada de60 palabras podía cortar una negación. Antes de generar, cada resultado se expande a los párrafos completos originales que intersectan su posición. Se conserva `retrieved_fragment` para trazabilidad. Si no se encuentra el documento, el sistema se abstiene. Una prueba automática exige conservar «no certifica» en el caso detectado. No basta comprobar que una cita exista: la revisión humana contrasta cada afirmación con su fuente. En consultas financieras se puede aplicar el filtro `financiero` para evitar mezcla temática; la demostración registra si se utilizó.

### Balance v3 (cuatro casos)
Organización del estudio: respuesta útil con cita. Tasa de financiación: reconoce dato ausente. Consulta de becas y fecha específica: bloqueadas por citas inválidas. No presentar estos cuatro casos como precisión general ni asegurar que el chatbot está listo para producción. Los ejemplos y registros completos permiten reproducir la auditoría.

## Comprobación previa cloud de solo lectura
Antes de evaluar, ejecutar `python check_cloud.py` con configuración privada. Contrasta la colección de 384 dimensiones y todos sus payloads con el corpus ACA1. El reporte no contiene claves ni endpoint. Un resultado `original_corpus_matches` verifica esa coincidencia, no la calidad del LLM. En caso de suspensión, confirmar el estado en la consola original antes de autorizar reactivación; no crear una colección sustitutiva silenciosamente. La regresión tras restaurar el entorno tiene 19 pruebas (incluye tres simuladas del preflight), no evidencia cloud real.

## Validación cloud real del 15 de noviembre de 2026
Clúster original reactivado; API consultada con clave temporal de solo lectura, limitada a la colección y manejada únicamente en memoria. El preflight contrastó 26 de 26 identificadores/payloads con el corpus ACA1, dimensión384. No se reindexó ni modificó ningún documento. La clave NO se distribuye: para reproducir hace falta acceso propio autorizado.
`results/cloud_rag_acceptance.json` registra cuatro consultas Qdrant Cloud + llama.cpp local: estudio semanal produjo respuesta útil; beca fue bloqueada por citas inválidas; tasa de financiación reconoció ausencia del dato; fecha específica se abstuvo antes del LLM por recuperación. Hubo tres llamadas reales al modelo. Los tiempos totales fueron16.08s,14.42s,13.12s y0.36s respectivamente. La muestra no prueba precisión general. La respuesta de tasa contiene marcadores adicionales sin explicación; revisión humana requerida.
La captura de app incluida sigue mostrando la ejecución LOCAL anterior y está etiquetada así; no es captura de despliegue público. La conexión cloud comprobada no significa que la app esté publicada ni que el generador tenga calidad de producción.
