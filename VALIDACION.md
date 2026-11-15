# Registro de validación

## Revisión 1: implementación y ejecución local
- Integridad del corpus: mismos tres documentos y fragmentos entregados en ACA1.
- Catálogo SQLite reconstruido con consultas reales.
- Evaluación TF-IDF/extractiva realizada. Las respuestas son fragmentos, no generaciones.
- 15 pruebas automatizadas: validación de entradas, filtro, citas, abstención y contrato cloud simulado. El doble de prueba cloud no valida una conexión remota.
- Streamlit AppTest: inicio, pregunta local, reinicio y error cloud sin credenciales, sin excepciones de aplicación.
- Notebook: cinco celdas ejecutadas secuencialmente como Python, salidas guardadas. La ejecución mediante kernel Jupyter se bloqueó por restricciones de red del entorno; no se afirma validada esa ruta.

## Revisión 2: auditoría independiente
Se detectó que el indicador de prueba LLM dependía de elegir el proveedor, no de una llamada efectiva. Se corrigió añadiendo llm_called y conteo real. Se separaron archivos por modo/proveedor, identificación del modelo, fecha y versiones. Se añadió puente privado entre Streamlit secrets y variables de entorno. Se ampliaron pruebas.

## Revisión 3: evaluación de generación
Baseline Qwen2.5-0.5B local: seis llamadas reales; cinco salidas rechazadas por citas inválidas, una salida con cita pero no útil. No se considera satisfactorio. Se preserva baseline_qwen05b.json. El modelo mayor se evalúa separadamente; resultados actuales en evaluation_semantic_local_hf.json con model_id. Requiere revisión humana de afirmaciones y fuentes.

## Bloqueos que impiden afirmar entrega completa
Conexión actual a Qdrant Cloud del ACA1, publicación GitHub/URL de aplicación y video de sustentación del estudiante. No se incluyen claves. No atribuir las pruebas locales al clúster remoto.

Intento Qwen1.5B: FP32 salió por código137 (límite de recursos); BF16 pudo cargar, pero la prueba de generación terminó por señal139. No se registra como evaluación superada. La ruta HF queda experimental; no es la recomendación de producción.

### Corrección de negación y revisión de citas
La auditoría de fronteras v2 detectó una inversión de negación por fragmento truncado y atribución temática incorrecta. Se agregó expansión a párrafos completos del documento original, control de documento existente, conservación del fragmento crudo y prueba de regresión. Los resultados v2 son históricos no aprobados. Validación actual: archivos v3.

## Cinco pasadas técnicas del paquete (15 de noviembre)
1. **Rúbrica y continuidad:** contraste de `src/rag.py`, `app.py`, notebook, README, corpus y datos con guía ACA2. Conserva colección/modelo/corpus; incorpora LLM, historial, panel y citas. Falta comprobar clúster cloud, URL pública, GitHub y video. Póster y presentación se revisan por separado por el equipo de materiales.
2. **Ejecución y regresiones:** compilación Python; 16 pruebas automatizadas; AppTest inicio, consulta, reinicio y error de credenciales; ocho celdas del notebook ejecutadas secuencialmente. Salidas reales guardadas. Kernel Jupyter estándar bloqueado por sandbox y no marcado como aprobado.
3. **Evidencia y coherencia:** archivos JSON separan TF-IDF, Qdrant local, modelos y versiones. v3 tiene cuatro casos generativos: estudio útil, tasa ausente reconocida, dos respuestas bloqueadas por citas. No se usan métricas temáticas como exactitud del chatbot. Intentos fallidos se conservan etiquetados como históricos.
4. **Seguridad y trazabilidad:** credenciales fuera del código; `.env.example` vacío; `.gitignore` excluye secretos; escaneo de patrones de claves sin hallazgos. Hash de documentos cotejado antes de expansión. El índice remoto solo se consulta. Preguntas/datos compartidos con API requieren configuración del usuario; predeterminado no llama proveedor remoto.
5. **Reproducibilidad y presentación técnica:** README, dependencias, rutas relativas, instrucciones Windows y Linux, nombres de resultados y salidas del notebook revisados. AppTest no presenta excepciones. Captura de navegador/QA visual queda a cargo de la revisión visual separada; no se afirma que AppTest compruebe estética.

### Resultado actual de generación v3
Qwen1.5B Q4_K_M + llama.cpp b12400 ejecutado realmente en CPU con MiniLM y Qdrant en memoria. Expansión a párrafos y control de hash corrigen el caso de negación truncada. No puede afirmarse que el sistema resuelva todo: dos de cuatro casos v3 fueron bloqueados por formato de cita. Recomendación: revisar salidas y emplear modelo más competente para una demostración final, sin eliminar controles.

## Reanudación y preparación cloud
Se restauró la versión 1 entregada desde Library tras el cambio de entorno. Regresión nueva: 19 pruebas aprobadas (las 16 anteriores y 3 pruebas simuladas del preflight). Se incorporó check_cloud.py, que solo consulta metadatos y recorre payloads para contrastar ID, contenido, posición y hash con ACA1; no crea ni modifica colecciones. No imprime claves ni endpoint y limita el detalle de errores. Sin configuración, devuelve configuration_missing y cloud_verified=false. Estas pruebas no acreditan conexión cloud.
El constructor cloud verifica dimensión antes de inicializar embeddings y reutiliza FASTEMBED_CACHE_PATH con dos hilos. El correo de suspensión del clúster comunicado por coordinación requiere comprobación actual en consola; no se ha reactivado ni alterado estado desde este código.

## Aceptación real cloud
 del 15 de noviembre de 2026
Clúster original reactivado; API consultada con clave temporal de solo lectura, limitada a la colección y manejada únicamente en memoria. El preflight contrastó 26 de 26 identificadores/payloads con el corpus ACA1, dimensión384. No se reindexó ni modificó ningún documento. La clave NO se distribuye: para reproducir hace falta acceso propio autorizado.
`results/cloud_rag_acceptance.json` registra cuatro consultas Qdrant Cloud + llama.cpp local: estudio semanal produjo respuesta útil; beca fue bloqueada por citas inválidas; tasa de financiación reconoció ausencia del dato; fecha específica se abstuvo antes del LLM por recuperación. Hubo tres llamadas reales al modelo. Los tiempos totales fueron16.08s,14.42s,13.12s y0.36s respectivamente. La muestra no prueba precisión general. La respuesta de tasa contiene marcadores adicionales sin explicación; revisión humana requerida.
La captura de app incluida sigue mostrando la ejecución LOCAL anterior y está etiquetada así; no es captura de despliegue público. La conexión cloud comprobada no significa que la app esté publicada ni que el generador tenga calidad de producción.
