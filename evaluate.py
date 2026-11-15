import json,statistics,os,datetime,importlib.metadata
from dotenv import load_dotenv
load_dotenv('.env')
from pathlib import Path
from src.rag import Retriever,answer,build_catalog
CASES=[('¿Cómo organizar el estudio semanal?','academico'),('¿Qué hacer cuando no comprendo una asignatura?','academico'),('¿Dónde consultar alternativas para pagar matrícula?','financiero'),('¿Cómo consultar becas y preparar soportes?','financiero'),('¿Dónde solicitar acompañamiento psicosocial?','bienestar'),('¿Cómo pedir orientación sobre barreras de aprendizaje?','bienestar'),('¿Quién ganó el mundial de fútbol?','fuera')]
def run(mode='local',provider='extractive'):
 r=Retriever(mode);build_catalog();reports=[]
 for q,theme in CASES:
  a=answer(q,r,provider);a['expected_theme']=theme
  a['theme_precision_at_3']=sum(x['tema']==theme for x in a['hits'])/len(a['hits']) if theme!='fuera' else None
  reports.append(a)
  print(f'Caso {len(reports)}/{len(CASES)}: {a["status"]} ({a["total_ms"]} ms)',flush=True)
 result={'timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'model_id':os.getenv('HF_LLM_MODEL','Qwen/Qwen2.5-0.5B-Instruct') if provider=='hf' else 'Qwen/Qwen2.5-1.5B-Instruct-GGUF Q4_K_M' if provider=='llamacpp' else os.getenv('LLM_MODEL') if provider!='extractive' else None,'embedding_model':'sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2' if mode!='local' else 'TF-IDF','versions':{n:importlib.metadata.version(n) for n in ['numpy','scikit-learn','qdrant-client']},'scope':f'{mode} / {provider}', 'llm_tested':any(x['llm_called'] for x in reports),'llm_calls':sum(x['llm_called'] for x in reports),'cloud_tested':mode=='cloud','cases':len(CASES),'median_total_ms':statistics.median(x['total_ms'] for x in reports),'theme_precision_at_3':statistics.mean(x['theme_precision_at_3'] for x in reports if x['theme_precision_at_3'] is not None),'reports':reports,'limitations':'Muestra exploratoria de 7 consultas elegidas manualmente. La coincidencia temática no mide fidelidad de generación ni calidad general.'}
 path=Path('results')/f'evaluation_{mode}_{provider}.json';path.write_text(json.dumps(result,ensure_ascii=False,indent=2));print(json.dumps({k:v for k,v in result.items() if k!='reports'},indent=2));return result
if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser();p.add_argument('--mode',choices=['local','semantic_local','cloud'],default='local');p.add_argument('--provider',choices=['extractive','ollama','api','hf','llamacpp'],default='extractive');a=p.parse_args();run(a.mode,a.provider)
