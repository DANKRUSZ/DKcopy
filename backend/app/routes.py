from fastapi import APIRouter, HTTPException
from .schemas import CopyRequest, CopyResponse
from .llm import get_llm
from .validation import validate_copy_output
from .utils import estimate_tokens, calculate_cost
from .logger import logger
from anthropic import APIError, RateLimitError, APITimeoutError

router = APIRouter(tags=["copy"])

@router.post("/generate", response_model=CopyResponse)
async def generate_copy(payload: CopyRequest) -> CopyResponse:
    try:
        logger.info(f"Generating {payload.content_type} for: {payload.audience[:50]}...")
        
        llm = get_llm()
        
        # Generate keywords if not provided
        keywords = payload.keywords
        if not keywords:
            keywords = await llm.generate_keywords(payload.audience, payload.product_info)
            logger.info(f"Generated keywords: {', '.join(keywords[:5])}")
        
        # Estimate input cost
        input_text = f"{payload.content_type} {payload.audience} {payload.product_info}"
        if payload.brand_sample:
            input_text += payload.brand_sample
        input_tokens = estimate_tokens(input_text)
        
        # Generate copy
        text = await llm.generate_copy(payload, keywords)
        
        # Validate
        validate_copy_output(text, require_cta=payload.cta)
        
        # Calculate cost
        output_tokens = estimate_tokens(text)
        cost = calculate_cost(input_tokens, output_tokens)
        
        logger.info(f"✓ Generated {len(text)} chars (~{output_tokens} tokens) - Cost: ${cost}")
        
        return CopyResponse(
            generated_copy=text,
            keywords=keywords,
            tone_used=payload.tone_of_voice or "default",
            content_type=payload.content_type,
            metadata={
                "status": "ok",
                "tokens_used": input_tokens + output_tokens,
                "estimated_cost": cost
            }
        )
    
    except ValueError as e:
        logger.error(f"Validation failed: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    
    except RateLimitError:
        logger.error("Hit Anthropic rate limit!")
        raise HTTPException(
            status_code=429,
            detail="Claude API rate limit reached. Wait a moment and try again."
        )
    
    except APITimeoutError:
        logger.error("Claude API timeout")
        raise HTTPException(
            status_code=504,
            detail="Request timed out. Try again."
        )
    
    except APIError as e:
        logger.error(f"Claude API error: {str(e)}")
        raise HTTPException(
            status_code=502,
            detail=f"Claude API error: {str(e)}"
        )
    
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")