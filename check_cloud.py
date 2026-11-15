"""Comprobación cloud de solo lectura, sin mostrar endpoint ni credenciales."""
import json, os, hashlib
from pathlib import Path
from datetime import datetime, timezone
from dotenv import load_dotenv
from qdrant_client import QdrantClient
ROOT=Path(__file__).resolve().parent
load_dotenv(ROOT/'.env')

def check():
    result={'timestamp_utc':datetime.now(timezone.utc).isoformat(),'cloud_verified':False,'read_only':True}
    url=os.getenv('QDRANT_URL','');key=os.getenv('QDRANT_API_KEY','')
    if not url.startswith('https://') or not key:
        return {**result,'status':'configuration_missing'}
    try:
        client=QdrantClient(url=url,api_key=key,timeout=30)
        name=os.getenv('QDRANT_COLLECTION','aca1_permanencia_documental_v1')
        info=client.get_collection(name)
        vectors=info.config.params.vectors
        size=getattr(vectors,'size',None)
        result.update(collection=name,vector_size=size,points_count=info.points_count)
        if size!=384:return {**result,'status':'incompatible_vector_configuration'}
        expected={str(x['id']):x for x in json.loads((ROOT/'data/aca1_chunks.json').read_text())}
        points=[];offset=None
        while True:
            batch,offset=client.scroll(name,limit=100,offset=offset,with_payload=True,with_vectors=False)
            points.extend(batch)
            if offset is None:break
            if len(points)>10000:return {**result,'status':'unexpected_large_collection'}
        matched=0
        for p in points:
            e=expected.get(str(p.id));payload=p.payload or {}
            if e and all(payload.get(k)==e.get(k) for k in ('file','text','sha256','word_start')):matched+=1
        result.update(expected_points=len(expected),read_points=len(points),matching_points=matched)
        result['cloud_verified']=matched==len(expected)==len(points)
        result['status']='original_corpus_matches' if result['cloud_verified'] else 'payload_mismatch_review_required'
        return result
    except Exception as e:
        # No se imprime str(e): algunos clientes incluyen URL o detalles privados.
        return {**result,'status':'connection_or_access_failed','error_type':type(e).__name__}
if __name__=='__main__':
    r=check();path=ROOT/'results/cloud_preflight.json';path.write_text(json.dumps(r,ensure_ascii=False,indent=2));print(json.dumps(r,ensure_ascii=False,indent=2))
