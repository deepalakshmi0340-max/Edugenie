from fastapi.testclient import TestClient
import main

client = TestClient(main.app)

def test_health():
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json()['status'] == 'ok'

def test_home_page():
    response = client.get('/')
    assert response.status_code == 200
    assert 'EduGenie' in response.text

def test_empty_question_rejected():
    response = client.post('/qa', json={'question': '   '})
    assert response.status_code == 400

def test_qa_api_returns_result(monkeypatch):
    async def fake_answer(question):
        return 'The largest ocean is the Pacific Ocean.'
    monkeypatch.setattr(main, 'answer_question', fake_answer)
    response = client.post('/qa', json={'question': 'Largest ocean?'})
    assert response.status_code == 200
    assert 'Pacific Ocean' in response.json()['result']
