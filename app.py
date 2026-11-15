from pathlib import Path
import os,json
import streamlit as st
from dotenv import load_dotenv
from src.rag import Retriever,answer,documents,build_catalog
load_dotenv('.env')
try:
 for key in ['QDRANT_URL','QDRANT_API_KEY','QDRANT_COLLECTION','LLM_BASE_URL','LLM_API_KEY','LLM_MODEL','OLLAMA_URL','HF_LLM_MODEL','LLAMA_CPP_BIN','GGUF_MODEL_PATH']:
  if key in st.secrets: os.environ[key]=str(st.secrets[key])
except FileNotFoundError: pass
st.set_page_config(page_title='Orientación académica · ACA 2',page_icon='📚',layout='wide')
st.title('Orientación académica con evidencia')
st.caption('Over Santiago Cometa Hernández · CUN · Computación en la Nube · ACA 2')
st.info('Prototipo didáctico: las tres guías son de elaboración propia, no reglamentos oficiales de CUN. No introducir información personal sensible.')
with st.sidebar:
 st.header('Configuración')
 mode=st.selectbox('Recuperación',['local','semantic_local','cloud'],format_func=lambda x:{'local':'Local · TF-IDF (diagnóstico)','semantic_local':'Qdrant local · embeddings ACA 1','cloud':'Qdrant Cloud · embeddings ACA 1'}[x])
 provider=st.selectbox('Generación',['extractive','ollama','api','hf','llamacpp'],format_func=lambda x:{'extractive':'Sin LLM · inspección documental','ollama':'LLM local · Ollama','api':'LLM · API compatible','hf':'LLM local · Hugging Face (experimental)','llamacpp':'LLM local · llama.cpp (GGUF)'}[x])
 k=st.slider('Fragmentos recuperados',1,6,3)
 tema=st.selectbox('Filtro temático',['Todos','academico','financiero','bienestar'])
 if st.button('Nueva conversación'): st.session_state.history=[];st.session_state.last=None
 st.caption('Credenciales solo en variables de entorno o secrets. No se incluyen en el código.')
 if mode!='cloud' or provider=='extractive':st.warning('Modo parcial: no demuestra integración completa cloud + LLM.')
@st.cache_resource
def retriever(m):return Retriever(m)
st.session_state.setdefault('history',[])
chat,docs,evaltab=st.tabs(['Conversación','Documentos y fuentes','Evaluación'])
with chat:
 for m in st.session_state.history:
  with st.chat_message(m['role']):st.markdown(m['content'])
 question=st.chat_input('Pregunta sobre acompañamiento académico, apoyos o bienestar')
 if question:
  with st.chat_message('user'):st.write(question)
  try:
   with st.spinner('Recuperando evidencia…'):r=answer(question,retriever(mode),provider,k,None if tema=='Todos' else tema,st.session_state.history)
   st.session_state.history.extend([{'role':'user','content':question},{'role':'assistant','content':r['answer']}]);st.session_state.last=r
   with st.chat_message('assistant'):st.markdown(r['answer'])
  except Exception as exc:st.error('No se completó la consulta. Revisa conexión y configuración privada. No se generó una respuesta.');st.caption(type(exc).__name__)
 if st.session_state.get('last'):
  r=st.session_state.last;st.caption(f"Estado: {r['status']} · Recuperación {r['retrieval_ms']} ms · Total {r['total_ms']} ms")
  with st.expander('Inspeccionar fragmentos y procedencia'):
   for i,h in enumerate(r['hits'],1):st.markdown(f"**[F{i}] {h['document']}** · similitud {h['score']:.3f}");st.write(h['text']);st.caption(h['file']+' · '+h['source'])
with docs:
 d=documents();st.metric('Guías',len(set(x['file'] for x in d)));st.metric('Fragmentos ACA 1',len(d))
 selected=st.selectbox('Documento',sorted(set(x['file'] for x in d)))
 st.markdown((Path('corpus')/selected).read_text())
 st.download_button('Descargar guía', (Path('corpus')/selected).read_text(),file_name=selected)
 st.caption('Catálogo SQL local generado a partir del mismo corpus. La consulta cloud no sobrescribe el índice ACA 1.')
with evaltab:
 files=sorted(Path('results').glob('*.json'))
 selected=st.selectbox('Registro de pruebas',files,format_func=lambda p:p.name)
 if selected:st.json(json.loads(selected.read_text()))
 st.warning('Los registros conservan pruebas de distintas configuraciones. cloud_rag_acceptance.json documenta la prueba real de Qdrant Cloud + LLM local; no significa que el modo actual de esta app esté conectado a cloud o genere con LLM. Consulta la configuración y el estado de cada respuesta.')
