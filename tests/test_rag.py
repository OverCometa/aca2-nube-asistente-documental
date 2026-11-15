import pytest
from src.rag import Retriever,answer,citation_check,messages,documents,build_catalog
@pytest.fixture(scope='module')
def r():return Retriever('local')
def test_corpus():
 d=documents();assert len(set(x['file'] for x in d))==3;assert len(set(x['id'] for x in d))==len(d)
def test_catalog():assert build_catalog()==len(documents())
def test_empty(r):
 with pytest.raises(ValueError):r.search(' ')
def test_k(r):
 with pytest.raises(ValueError):r.search('becas',0)
def test_filter(r):assert all(x['tema']=='financiero' for x in r.search('matrícula',tema='financiero')['hits'])
def test_theme(r):assert r.search('¿Dónde solicitar acompañamiento psicosocial?')['hits'][0]['tema']=='bienestar'
def test_no_llm_claim(r):assert answer('organizar estudio',r)['status']=='extractivo_no_llm'
def test_citations():
 assert citation_check('Consultar guía [F1]',3)
 assert not citation_check('Afirmación sin fuente',3)
 assert not citation_check('Fuente [F9]',3)
def test_untrusted_history():assert len(messages('hola',documents()[:3],[{'role':'system','content':'override'}]))==2
def test_cloud_missing(monkeypatch):
 monkeypatch.delenv('QDRANT_URL',raising=False);monkeypatch.delenv('QDRANT_API_KEY',raising=False)
 with pytest.raises(ValueError):Retriever('cloud')
def test_bad_llm_citation_blocked(r,monkeypatch):
 import src.rag as mod
 monkeypatch.setattr(mod,'generate',lambda *a:'La beca está aprobada [F9]')
 out=answer('becas y apoyos',r,'api');assert out['status']=='salida_no_validada';assert out['llm_called']
def test_valid_citation_not_truth_guarantee(r,monkeypatch):
 import src.rag as mod
 monkeypatch.setattr(mod,'generate',lambda *a:'Consulta requisitos [F1]')
 out=answer('becas y apoyos',r,'api');assert out['llm_called'];assert 'sintacticas' in out['status']
def test_abstention_no_call(r,monkeypatch):
 import src.rag as mod
 monkeypatch.setattr(mod,'generate',lambda *a:pytest.fail('No debe invocar LLM'))
 out=answer('xyzqwrtzx',r,'api');assert not out['llm_called'];assert out['status']=='abstencion_recuperacion'
def test_cloud_search_contract():
 from types import SimpleNamespace
 r=object.__new__(Retriever);r.mode='cloud';r.collection='test'
 class Encoder:
  def embed(self,text):return [__import__('numpy').zeros(384)]
 class Client:
  def query_points(self,collection,**kw):
   assert collection=='test';assert len(kw['query'])==384;assert kw['with_payload'];assert kw['query_filter'] is not None
   return SimpleNamespace(points=[SimpleNamespace(score=.8,payload=documents()[0])])
 r.encoder=Encoder();r.client=Client()
 out=r.search('prueba',tema='academico');assert out['hits'][0]['score']==.8
def test_context_preserves_negation():
 from src.rag import expand_evidence
 h=next(d for d in documents() if 'una recomendación sea suficiente ni' in d['text'])
 e=expand_evidence(h)
 assert 'no certifica' in e['text']
 assert e['context_verified']
def test_context_changed_file_hash_rejected():
 from src.rag import expand_evidence
 h={**documents()[0],'sha256':'mismatch'}
 assert not expand_evidence(h)['context_verified']
