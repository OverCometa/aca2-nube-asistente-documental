from types import SimpleNamespace
import check_cloud

def test_missing_config(monkeypatch):
    monkeypatch.delenv('QDRANT_API_KEY',raising=False)
    assert check_cloud.check()['status']=='configuration_missing'

def test_original_payloads_match(monkeypatch):
    monkeypatch.setenv('QDRANT_URL','https://test.invalid');monkeypatch.setenv('QDRANT_API_KEY','not-a-real-secret')
    docs=check_cloud.json.loads((check_cloud.ROOT/'data/aca1_chunks.json').read_text())
    class Client:
        def __init__(self,**kw):pass
        def get_collection(self,name):return SimpleNamespace(config=SimpleNamespace(params=SimpleNamespace(vectors=SimpleNamespace(size=384))),points_count=len(docs))
        def scroll(self,*a,**kw):return ([SimpleNamespace(id=d['id'],payload=d) for d in docs],None)
    monkeypatch.setattr(check_cloud,'QdrantClient',Client)
    assert check_cloud.check()['cloud_verified'] is True

def test_errors_redacted(monkeypatch):
    monkeypatch.setenv('QDRANT_URL','https://test.invalid');monkeypatch.setenv('QDRANT_API_KEY','not-a-real-secret')
    def fail(**kw):raise ValueError('secret=not-a-real-secret')
    monkeypatch.setattr(check_cloud,'QdrantClient',fail)
    result=check_cloud.check()
    assert result['cloud_verified'] is False
    assert 'not-a-real-secret' not in str(result)
