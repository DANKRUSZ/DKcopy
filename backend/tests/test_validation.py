import pytest
from app.validation import validate_copy_output

def test_validation_passes_normal_copy():
    text = "Great copy here. CTA: Click now!"
    validate_copy_output(text, require_cta=True)

def test_validation_fails_too_long():
    text = "x" * 4001
    with pytest.raises(ValueError, match="too long"):
        validate_copy_output(text, require_cta=False)

def test_validation_fails_missing_cta():
    text = "This is some great marketing copy that describes the product."
    with pytest.raises(ValueError, match="CTA"):
        validate_copy_output(text, require_cta=True)

def test_validation_passes_no_cta_required():
    text = "Great copy without a CTA"
    validate_copy_output(text, require_cta=False)
