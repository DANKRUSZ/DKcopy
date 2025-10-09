import pytest
from app.utils import estimate_tokens, calculate_cost

def test_estimate_tokens():
    text = "Hello world this is a test"
    tokens = estimate_tokens(text)
    assert tokens > 0
    assert tokens == len(text) // 4

def test_calculate_cost():
    # 1000 input tokens, 500 output tokens
    cost = calculate_cost(1000, 500)
    # (1000/1M * $3) + (500/1M * $15) = $0.003 + $0.0075 = $0.0105
    assert cost == 0.0105

def test_calculate_cost_zero():
    cost = calculate_cost(0, 0)
    assert cost == 0.0