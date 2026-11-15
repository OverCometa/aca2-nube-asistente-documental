from pathlib import Path
import os,json,time,threading
import streamlit as st
from dotenv import load_dotenv
from src.rag import Retriever,answer,documents,build_catalog
from src.public_runtime import ensure_runtime
load_dotenv('.env')
try:
 for key in ['QDRANT_URL','QDRANT_API_KEY','QDRANT_COLLECTION','LLM_BASE_URL','LLM_API_KEY','LLM_MODEL','OLLAMA_URL','HF_LLM_MODEL','LLAMA_CPP_BIN','GGUF_MODEL_PATH']:
  if key in st.secrets: os.environ[key]=str(st.secrets[key])
except FileNotFoundError: pass

def connect_cloud_session():
 url=st.session_state.get('session_qdrant_url','')
 key=st.session_state.get('session_qdrant_key','')
 try:
  from urllib.parse import urlparse
  parsed=urlparse(url)
  if parsed.scheme!='https' or not parsed.hostname or not parsed.hostname.endswith('.cloud.qdrant.io') or parsed.username or parsed.password:
   raise ValueError('Endpoint Qdrant Cloud HTTPS requerido')
  if not key:raise ValueError('Clave requerida')
  st.session_state.cloud_retriever=Retriever('cloud',cloud_url=url,cloud_api_key=key)
  st.session_state.cloud_connected_at=time.time()
  st.session_state.cloud_connection_message='Conexión de solo lectura configurada para esta sesión.'
 except Exception as exc:
  st.session_state.pop('cloud_retriever',None)
  st.session_state.cloud_connection_message='No se pudo conectar. Revisa endpoint, alcance, vigencia y estado del clúster. Tipo: '+type(exc).__name__
 finally:
  st.session_state.session_qdrant_key=''
  key=None

def disconnect_cloud_session(clear_widget=True):
 r=st.session_state.pop('cloud_retriever',None)
 if r is not None:
  try:r.client.close()
  except Exception:pass
 st.session_state.pop('cloud_connected_at',None)
 if clear_widget:st.session_state.session_qdrant_key=''
 st.session_state.cloud_connection_message='Conexión retirada del estado de la sesión.'

st.set_page_config(page_title='Orientación académica · ACA 2',page_icon='📚',layout='wide')
st.title('Orientación académica con evidencia')
st.caption('Over Santiago Cometa Hernández · CUN · Computación en la Nube · ACA 2')
st.caption('Chatbot generativo en CPU, sin API de pago. La recuperación predeterminada usa el corpus local; no Qdrant Cloud. La primera consulta descarga modelos oficiales y puede tardar varios minutos.')
st.info('Prototipo didáctico: las tres guías son de elaboración propia, no reglamentos oficiales de CUN. No introducir información personal sensible.')
with st.sidebar:
 st.header('Configuración')
 mode=st.selectbox('Recuperación',['semantic_local','local','cloud'],format_func=lambda x:{'local':'Local · TF-IDF (diagnóstico)','semantic_local':'Qdrant local · embeddings ACA 1','cloud':'Qdrant Cloud · embeddings ACA 1'}[x])
 provider=st.selectbox('Generación',['llamacpp','extractive','ollama','api','hf'],format_func=lambda x:{'extractive':'Sin LLM · inspección documental','ollama':'LLM local · Ollama','api':'LLM · API compatible','hf':'LLM local · Hugging Face (experimental)','llamacpp':'LLM local · llama.cpp (GGUF)'}[x])
 if mode=='cloud':
  st.caption('Acceso privado efímero: el endpoint y la clave se transmiten al servidor Streamlit. Solo introducir con autorización expresa. No se guardan en archivos ni secretos del servicio; el cliente autenticado permanece en RAM de esta sesión.')
  with st.form('cloud_access'):
   st.text_input('Endpoint HTTPS de Qdrant Cloud',key='session_qdrant_url')
   st.text_input('Clave temporal de solo lectura',type='password',key='session_qdrant_key')
   st.form_submit_button('Conectar solo esta sesión',on_click=connect_cloud_session)
  st.button('Desconectar acceso privado',on_click=disconnect_cloud_session)
  if st.session_state.get('cloud_connection_message'):st.info(st.session_state.cloud_connection_message)
 k=st.slider('Fragmentos recuperados',1,6,3)
 tema=st.selectbox('Filtro temático',['Todos','academico','financiero','bienestar'])
 if st.button('Nueva conversación'): st.session_state.history=[];st.session_state.last=None
 st.caption('Credenciales solo en variables de entorno o secrets. No se incluyen en el código.')
 if mode!='cloud' or provider=='extractive':st.warning('Modo parcial: no demuestra integración completa cloud + LLM.')
@st.cache_resource
def retriever(m):
 if m=='cloud':raise ValueError('Cloud no se almacena en caché global.')
 return Retriever(m)

def current_retriever(m):
 if m!='cloud':return retriever(m)
 r=st.session_state.get('cloud_retriever')
 if r is None:raise ValueError('Conecta el acceso privado de esta sesión.')
 if time.time()-st.session_state.get('cloud_connected_at',0)>900:
  disconnect_cloud_session(clear_widget=False);raise ValueError('Sesión cloud expirada tras15min; conectar de nuevo.')
 return r
@st.cache_resource
def query_lock():return threading.Lock()
st.session_state.setdefault('history',[])
chat,docs,evaltab=st.tabs(['Conversación','Documentos y fuentes','Evaluación'])
with chat:
 for m in st.session_state.history:
  with st.chat_message(m['role']):st.markdown(m['content'])
 question=st.chat_input('Pregunta sobre acompañamiento académico, apoyos o bienestar')
 if question:
  with st.chat_message('user'):st.write(question)
  acquired=query_lock().acquire(blocking=False)
  try:
   if not acquired:raise RuntimeError('El servidor está atendiendo otra consulta; reintenta en unos segundos.')
   if provider=='llamacpp':
    with st.spinner('Preparando modelo local gratuito; primera descarga puede tardar varios minutos…'):ensure_runtime()
   with st.spinner('Recuperando evidencia y generando respuesta…'):r=answer(question,current_retriever(mode),provider,k,None if tema=='Todos' else tema,st.session_state.history)
   st.session_state.history.extend([{'role':'user','content':question},{'role':'assistant','content':r['answer']}]);st.session_state.last=r
   with st.chat_message('assistant'):st.markdown(r['answer'])
  except Exception as exc:st.error('Servidor ocupado o consulta no completada. Espera unos segundos y revisa configuración. No se generó una respuesta.');st.caption(type(exc).__name__)
  finally:
   if acquired:query_lock().release()
 if st.session_state.get('last'):
  r=st.session_state.last;st.caption(f"Consulta ejecutada: {r.get('retrieval_mode','histórica')} + {r.get('provider','histórico')} · LLM llamado: {r.get('llm_called',False)} · Estado: {r['status']} · Recuperación {r['retrieval_ms']} ms · Total {r['total_ms']} ms")
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
