import pytest

def test_health_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_generate_copy_success(client, mock_llm):
    payload = {
        "content_type": "Landing page hero",
        "audience": "busy freelancers",
        "product_info": "An AI tool that drafts proposals",
        "cta": True
    }
    response = client.post("/generate", json=payload)
    assert response.status_code == 200
    
    data = response.json()
    assert "content" in data
    assert "keywords" in data
    assert len(data["keywords"]) > 0
    assert data["content_type"] == "Landing page hero"

def test_generate_copy_missing_field(client):
    payload = {
        "audience": "freelancers",
        "product_info": "AI tool",
        "cta": True
    }
    response = client.post("/generate", json=payload)
    assert response.status_code == 422

def test_generate_copy_with_keywords(client, mock_llm):
    payload = {
        "content_type": "Email",
        "audience": "marketers",
        "product_info": "Analytics tool",
        "cta": False,
        "keywords": ["custom", "keywords"]
    }
    response = client.post("/generate", json=payload)
    assert response.status_code == 200
