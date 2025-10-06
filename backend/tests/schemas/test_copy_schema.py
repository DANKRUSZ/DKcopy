import pytest
from pydantic_core import ValidationError


from app.schemas.copy import CopyRequest, CopyResponse

def test_copy_request_minimal_valid():
    payload = {
        "content_type": "Landing page hero",
        "audience": "busy freelancers",
        "product_info": "An AI tool that drafts client proposals",
        "cta": True,
    }
    model = CopyRequest(**payload)
    assert model.content_type == "Landing page hero"
    assert model.audience == "busy freelancers"
    assert model.product_info.startswith("An AI tool")
    assert model.cta is True

    # Optional fields should default to None
    assert model.tone_of_voice is None
    assert model.style is None
    assert model.brand_sample is None
    assert model.keywords is None


def test_copy_request_missing_required_field_raises():
    # missing content_type
    payload = {
        "audience": "growth marketers",
        "product_info": "CRM for B2B teams",
        "cta": False,
    }
    with pytest.raises(ValidationError):
        CopyRequest(**payload)


def test_copy_request_brand_sample_too_long():
    payload = {
        "content_type": "facebook ad",
        "audience": "creators",
        "product_info": "Video editing SaaS",
        "cta": True,
        "brand_sample": "x" * 3001,  # > 3000 chars
    }
    with pytest.raises(ValidationError):
        CopyRequest(**payload)


def test_copy_response_shape_valid():
    resp = CopyResponse(
        generated_copy="Your new headline goes here.",
        keywords=["video", "editing", "SaaS"],
        tone_used="conversational",
        content_type="facebook ad",
        metadata={"model": "gpt-5", "tokens": 123},
    )
    assert isinstance(resp.generated_copy, str) and resp.generated_copy != ""
    assert isinstance(resp.keywords, list) and len(resp.keywords) > 0
    assert resp.tone_used == "conversational"
    assert resp.content_type == "facebook ad"
    assert isinstance(resp.metadata, dict)


def test_copy_request_brand_sample_max_boundary_ok():
    payload = {
        "content_type": "facebook ad",
        "audience": "creators",
        "product_info": "Video editing SaaS",
        "cta": True,
        "brand_sample": "x" * 3000,  # exactly 3000
    }
    model = CopyRequest(**payload)

    # Pylance-safe: check for None first
    assert model.brand_sample is not None
    assert len(model.brand_sample) == 3000


def test_copy_request_rejects_empty_content_type():
    # In future you may add a validator to strip/forbid empty strings
    with pytest.raises(ValidationError):
        CopyRequest(
            content_type="   ",
            audience="creators",
            product_info="Video editing SaaS",
            cta=True,
        )