from fastapi.testclient import TestClient

from app.main import app
from app.core.config import settings

client = TestClient(app)

API_BASE = settings.API_V1_PREFIX

URL = f"{API_BASE}/copy/generate"


def test_generate_minimal_payload_returns_200_and_shape():
    payload = {
        "content_type": "Landing page hero",
        "audience": "busy freelancers",
        "product_info": "An AI tool that drafts client proposals",
        "cta": True,
    }
    res = client.post(URL, json=payload)
    assert res.status_code == 200, res.text
    data = res.json()

    assert isinstance(data.get("generated_copy"), str) and len(data["generated_copy"]) > 0
    assert isinstance(data.get("keywords"), list) and len(data["keywords"]) > 0
    assert isinstance(data.get("tone_used"), str)
    assert data.get("content_type") == payload["content_type"]
    assert isinstance(data.get("metadata"), dict)


def test_generate_missing_required_field_422():
    payload = {
        # "content_type" missing
        "audience": "growth marketers",
        "product_info": "CRM for B2B",
        "cta": False,
    }
    res = client.post(URL, json=payload)
    assert res.status_code == 422


def test_generate_brand_sample_too_long_422():
    payload = {
        "content_type": "facebook ad",
        "audience": "creators",
        "product_info": "Video editing SaaS",
        "cta": True,
        "brand_sample": "x" * 3001,
    }
    res = client.post(URL, json=payload)
    assert res.status_code == 422


def test_generate_with_keywords_keeps_list_nonempty():
    payload = {
        "content_type": "email_intro",
        "audience": "sales leaders",
        "product_info": "Pipeline analytics tool",
        "cta": True,
        "keywords": ["analytics", "pipeline", "forecasting"],
    }
    res = client.post(URL, json=payload)
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data.get("keywords"), list)
    assert len(data["keywords"]) > 0
