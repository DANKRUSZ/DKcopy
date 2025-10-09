MAX_COPY_LENGTH = 2000

def validate_copy_output(text: str, require_cta: bool) -> None:
    """Validate generated copy meets requirements"""
    if len(text) > MAX_COPY_LENGTH:
        raise ValueError(f"Generated copy too long ({len(text)} chars, max {MAX_COPY_LENGTH})")
    
    if require_cta:
        # Check for common CTA patterns - be more lenient
        text_lower = text.lower()
        cta_indicators = [
            "click", "sign up", "try", "get started", "buy now", "learn more", 
            "contact us", "shop now", "order now", "download", "subscribe",
            "join", "register", "book", "schedule", "visit", "discover",
            "explore", "start", "begin", "claim", "grab", "unlock", "see",
            "find out", "check out", "apply", "reserve", "call now", "today"
        ]
        
        # Also check for imperative verbs at the start of sentences (common in CTAs)
        sentences = text.split('.')
        for sentence in sentences[-3:]:  # Check last 3 sentences
            sentence = sentence.strip().lower()
            if sentence and any(sentence.startswith(word) for word in cta_indicators):
                return  # Found a CTA
        
        # Check if any CTA indicator appears in the text
        has_cta = any(indicator in text_lower for indicator in cta_indicators)
        
        if not has_cta:
            raise ValueError("CTA required but missing from generated copy")