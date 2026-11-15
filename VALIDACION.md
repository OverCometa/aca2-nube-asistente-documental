# Validación · Estado vigente al 15 de noviembre de 2026

## Comprobado ahora
- Qdrant Cloud original reactivado y consultado en lectura.26/26 fragmentos e identificadores coinciden;384 dimensiones. Evidencia: `results/cloud_rag_acceptance.json` y `results/cloud_preflight.json`.
- Cuatro casos reales con Qdrant Cloud y llama.cpp local, tres llamadas al LLM. Estudio: respuesta fiel pero larga. Beca: salida coherente sin citas, bloqueada por formato. Tasa: ausencia correctamente reconocida, marcadores extra. Fecha: abstención antes del LLM.
- Auditoría independiente de las respuestas contra corpus y hashes: `results/auditoria_cloud_independiente.txt`. No es otra ejecución remota.
-19 pruebas de software aprobadas, incluyendo tres simulaciones del preflight; registro `results/regression_restored_environment.txt`. AppTest confirmó carga y consulta diagnóstica de la copia pública sin excepciones.
- Repositorio publicado: https://github.com/OverCometa/aca2-nube-asistente-documental . Publicar código no implica desplegar la app.
- No se guardó la clave temporal en archivos. No se incluyen credenciales, endpoint real de cuenta, cachés ni pesos. La clave usada fue restringida a lectura de la colección y se manejó únicamente en memoria.

## Notebook y alcance de ejecución
Las ocho celdas originales se ejecutaron secuencialmente como Python y conservan salidas históricas. La ejecución de kernel Jupyter estaba bloqueada en el entorno inicial y no se marca como superada. Se añadió una celda ejecutada que lee el reporte cloud real, generado por verify_cloud_rag.py. No atribuir las salidas locales antiguas al clúster remoto.

## Historia de correcciones, no bloqueos actuales
Antes de recuperar acceso, Qdrant Cloud estaba pendiente. Ese bloqueo ya se resolvió. Antes de publicar, GitHub estaba pendiente; también se resolvió. Los experimentos HF pequeños no dieron calidad satisfactoria; uno mayor falló por recursos. Se adoptó llama.cpp cuantizado. Los reportes detallados de esos intentos históricos pertenecen al paquete académico completo y no se distribuyen en esta copia pública mínima.

Se corrigió llm_tested para contar llamadas efectivas, se separaron proveedores y se expandieron fragmentos a párrafos completos tras detectar una negación cortada. Se comprueba SHA256 antes de utilizar contexto. Las citas válidas en sintaxis no prueban fidelidad semántica.

## Cinco revisiones focalizadas de publicación
1. Continuidad: colección/modelo/corpus originales; código remoto sin mutaciones.
2. Ejecución:19 tests aprobados y AppTest de diagnóstico; prueba cloud registrada separadamente.
3. Evidencia: cuatro casos/tres llamadas; estados reales sin presentar porcentaje general.
4. Seguridad: sin secretos ni .env; .env.example vacío; patrones de claves y endpoint real sin hallazgos.
5. Coherencia: documentación pública actualizada, evidencias citadas presentes, límites de demo explícitos.

## Pendientes actuales
Despliegue y URL pública verificable, video personal y actualización de sus enlaces en póster. La demo sin configuración privada es local/extractiva, no la integración cloud+LLM completa. La generación conserva límites de formato y longitud; requiere revisión humana. Actividad no enviada a CDigital.
