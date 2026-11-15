"""Pruebas de aceptación reales; nunca cambia la colección remota."""
import json,datetime
from pathlib import Path
from dotenv import load_dotenv
from check_cloud import check
from src.rag import Retriever,answer
ROOT=Path(__file__).resolve().parent
load_dotenv(ROOT/'.env')
if __name__=='__main__':
    print('Comprobando colección remota en lectura…',flush=True)
    preflight=check()
    if not preflight['cloud_verified']:
        print(json.dumps(preflight,ensure_ascii=False,indent=2));raise SystemExit(2)
    print('Corpus remoto coincide. Inicializando embeddings…',flush=True)
    r=Retriever('cloud');reports=[]
    for q,theme in [('¿Cómo organizar el estudio semanal?',None),('¿Qué revisar antes de solicitar una beca?','financiero'),('¿Cuál es la tasa de financiación de matrícula?','financiero'),('¿Cuál es la fecha límite de becas CUN en noviembre de 2026?',None)]:
        a=answer(q,r,'llamacpp',3,theme);reports.append(a);print(f"Caso {len(reports)}: {a['status']}",flush=True)
    out={'timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'Qdrant Cloud original + llama.cpp Qwen1.5B Q4_K_M','preflight':preflight,'reports':reports,'limitations':'Cuatro casos exploratorios, revisar fidelidad humana; citas sintácticas no prueban exactitud.'}
    (ROOT/'results/cloud_rag_acceptance.json').write_text(json.dumps(out,ensure_ascii=False,indent=2));print('Evidencia guardada; revisar cada respuesta antes de declarar cumplimiento.')
