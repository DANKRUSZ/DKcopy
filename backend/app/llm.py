import json
from typing import List
from anthropic import AsyncAnthropic
from anthropic.types import TextBlock, Message
from .config import settings
from .schemas import CopyRequest

class CopywritingLLM:
    def __init__(self):
        self.client = AsyncAnthropic(api_key=settings.ANTHROPIC_API_KEY)
        self.model = settings.ANTHROPIC_MODEL
    
    async def generate_keywords(self, audience: str, product_info: str) -> List[str]:
        """Generate SEO keywords using Claude"""
        message = await self.client.messages.create(
            model=self.model,
            max_tokens=1024,
            messages=[{
                "role": "user",
                "content": f"""You are an SEO assistant. Generate 5-10 relevant SEO keywords for this copywriting project.

Audience: {audience}
Product/Service: {product_info}

Return ONLY a JSON array of lowercase keyword strings, nothing else. Example: ["keyword1", "keyword2", "keyword3"]"""
            }]
        )
        
        # Extract text from the response content
        text = ""
        for block in message.content:
            if isinstance(block, TextBlock):
                text = block.text
                break
        
        try:
            keywords = json.loads(text.strip())
            if not isinstance(keywords, list):
                raise ValueError("not a list")
            keywords = [str(k).strip().lower() for k in keywords if str(k).strip()]
        except:
            # Fallback parsing
            keywords = [k.strip().lower() for k in text.replace("\n", ",").split(",") if k.strip()]
        
        # Dedupe and limit
        seen = set()
        result = []
        for k in keywords:
            if k and k not in seen:
                seen.add(k)
                result.append(k)
        
        return result[:10] or ["marketing", "productivity", "automation"]
    
    async def generate_copy(self, request: CopyRequest, keywords: List[str]) -> str:
        """Generate marketing copy using Claude"""
        message = await self.client.messages.create(
            model=self.model,
            max_tokens=4096,
            system="""You are an expert direct-response copywriter.
- Always follow constraints exactly.
- Write in clear, persuasive language.
- Avoid fluff, filler, and unverifiable claims.
- Return ONLY the copy itself, no meta commentary.""",
            messages=[{
                "role": "user",
                "content": self._build_prompt(request, keywords)
            }]
        )
        
        # Extract text from the response content
        text = ""
        for block in message.content:
            if isinstance(block, TextBlock):
                text = block.text
                break
        
        return text
    
    def _build_prompt(self, req: CopyRequest, keywords: List[str]) -> str:
        parts = [
            f"Content type: {req.content_type}",
            f"Audience: {req.audience}",
            f"Product/Service: {req.product_info}"
        ]
        
        if req.tone_of_voice:
            parts.append(f"Tone of voice: {req.tone_of_voice}")
        if req.style:
            parts.append(f"Style controls: {req.style}")
        if req.brand_sample:
            parts.append(f"Brand voice sample (reference, do not copy):\n{req.brand_sample}")
        if keywords:
            parts.append(f"Keywords to weave in naturally: {', '.join(keywords)}")
        
        parts.append("\nConstraints:")
        parts.append("- Connect features to outcomes")
        parts.append("- UK English spelling")
        parts.append("- No meta commentary or headings")
        parts.append("- Don't invent product details")
        parts.append(f"- {'End with ONE clear call-to-action' if req.cta else 'Do NOT include a call-to-action'}")
        
        return "\n".join(parts)


class FakeCopywritingLLM(CopywritingLLM):
    """For testing without API calls"""
    def __init__(self, mode: str = "compliant"):
        self.mode = mode
    
    async def generate_keywords(self, audience: str, product_info: str) -> List[str]:
        return ["ai tool", "copywriting", "automation", "marketing", "productivity"]
    
    async def generate_copy(self, request: CopyRequest, keywords: List[str]) -> str:
        if self.mode == "too_long":
            return " ".join(["Long body"] * 800)
        if self.mode == "missing_cta":
            return "Great copy without a CTA."
        return "Headline: Win Back Your Time\n\nBody: Freelancers love this tool.\n\nCTA: Start your free trial."


def get_llm() -> CopywritingLLM:
    """Factory function for getting the right LLM instance"""
    if settings.USE_FAKE_LLM:
        return FakeCopywritingLLM()
    return CopywritingLLM()