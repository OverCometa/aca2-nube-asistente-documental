"""Bootstrap of official CPU model assets. No API keys or paid inference."""
from pathlib import Path
from functools import lru_cache
import hashlib,os,tarfile,platform,requests,threading
CACHE=Path(os.getenv('ACA_PUBLIC_CACHE','/tmp/aca_public_models'))
ASSETS={
 'llama.tar.gz':('https://github.com/ggml-org/llama.cpp/releases/download/b12400/llama-b12400-bin-ubuntu-x64.tar.gz','2fc619d367f6a6bed8a0d2436c25d33eab1b60167ccef4906147d7d3a6ad3020'),
 'qwen15b.gguf':('https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct-GGUF/resolve/main/qwen2.5-1.5b-instruct-q4_k_m.gguf','6a1a2eb6d15622bf3c96857206351ba97e1af16c30d7a74ee38970e434e9407e')}
LOCK=threading.Lock()
def sha(path):
 h=hashlib.sha256()
 with path.open('rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
 return h.hexdigest()
def download(name,url,checksum):
 path=CACHE/name
 if path.is_file() and sha(path)==checksum:return path
 temp=path.with_suffix(path.suffix+'.part')
 try:
  with requests.get(url,stream=True,timeout=(30,120)) as r:
   r.raise_for_status();total=0
   with temp.open('wb') as f:
    for block in r.iter_content(1024*1024):
     total+=len(block)
     if total>1_500_000_000:raise ValueError('Asset exceeds expected size')
     f.write(block)
  if sha(temp)!=checksum:raise ValueError('Asset integrity check failed')
  temp.replace(path);return path
 finally:temp.unlink(missing_ok=True)
@lru_cache(maxsize=1)
def ensure_runtime():
 with LOCK:
  if platform.system()!='Linux' or platform.machine() not in ('x86_64','AMD64'):raise RuntimeError('Automatic runtime supports Linux x86_64 only')
  CACHE.mkdir(parents=True,exist_ok=True)
  archive=download('llama.tar.gz',*ASSETS['llama.tar.gz'])
  model=download('qwen15b.gguf',*ASSETS['qwen15b.gguf'])
  with tarfile.open(archive) as tar:tar.extractall(CACHE,filter='data')
  binary=CACHE/'llama-b12400/llama-completion'
  if not binary.is_file():raise RuntimeError('Official binary not found')
  os.environ['ACA_LOW_MEMORY']='1'
  os.environ['LLAMA_CPP_BIN']=str(binary);os.environ['GGUF_MODEL_PATH']=str(model)
  os.environ.setdefault('FASTEMBED_CACHE_PATH',str(CACHE/'fastembed'))
  os.environ.setdefault('HF_HOME',str(CACHE/'huggingface'))
  os.environ.setdefault('HF_HUB_DISABLE_XET','1')
  return {'model':'Qwen2.5-1.5B-Instruct Q4_K_M','engine':'llama.cpp b12400','scope':'CPU runtime; no API key'}
