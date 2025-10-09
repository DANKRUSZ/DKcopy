def estimate_tokens(text: str) -> int:
    """Rough token estimation (Claude uses ~4 chars per token)"""
    return len(text) // 4

def calculate_cost(input_tokens: int, output_tokens: int) -> float:
    """
    Calculate cost for Claude Sonnet 4.5:
    - Input: $3 per million tokens
    - Output: $15 per million tokens
    """
    input_cost = (input_tokens / 1_000_000) * 3.0
    output_cost = (output_tokens / 1_000_000) * 15.0
    return round(input_cost + output_cost, 6)