import json
from typing import List
from anthropic import AsyncAnthropic
from anthropic.types import TextBlock
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
                "content": f"""Generate 5-10 relevant SEO keywords for this copywriting project.

Audience: {audience}
Product/Service: {product_info}

Return ONLY a JSON array of lowercase keyword strings. No markdown, no code blocks, no explanations. Just the raw JSON array.

Example format: ["keyword1", "keyword2", "keyword3"]"""
            }]
        )
        
        # extract text from the response content
        text = ""
        for block in message.content:
            if isinstance(block, TextBlock) and hasattr(block, 'text'):
                text = block.text
                break
        
        # clean up any markdown code block formatting
        text = text.strip()
        if text.startswith("```"):
            lines = text.split("\n")
            lines = lines[1:]
            if lines and lines[-1].strip() == "```":
                lines = lines[:-1]
            text = "\n".join(lines).strip()
        
        try:
            keywords = json.loads(text)
            if not isinstance(keywords, list):
                raise ValueError("not a list")
            keywords = [str(k).strip().lower() for k in keywords if str(k).strip()]
        except:
            keywords = [k.strip().lower() for k in text.replace("\n", ",").split(",") if k.strip()]
            keywords = [k.strip('"\'[]') for k in keywords]
        
        seen = set()
        result = []
        for k in keywords:
            k = k.strip('"\'[]')
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
- Return ONLY the copy itself, no meta commentary.
- Write naturally as if speaking to a person, NOT optimizing for search engines.
- Do NOT create multiple keyword variations (e.g., don't say "fitness program," "workout routine," and "exercise plan" in the same copy).
- Use specific product/service terms once or twice, then refer to "it," "this," "the product," or "the service" thereafter.""",
            messages=[{
                "role": "user",
                "content": self._build_prompt(request, keywords)
            }]
        )
        
        # extract text from the response content
        text = ""
        for block in message.content:
            if isinstance(block, TextBlock) and hasattr(block, 'text'):
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
            parts.append("IMPORTANT: Use ONLY these keywords (maximum 1-2 mentions each). Do not generate keyword variations or synonyms.")
        
        parts.append("\nConstraints:")
        parts.append("- Connect features to outcomes")
        parts.append("- UK English spelling")
        parts.append("- No meta commentary or headings")
        parts.append("- Don't invent product details")

        # adding length guidance based on content type
        length_guidance = self._get_length_guidance(req.content_type)
        if length_guidance:
            parts.append(f"- {length_guidance}")


        parts.append(f"- {'End with ONE clear call-to-action' if req.cta else 'Do NOT include a call-to-action'}")
        
        return "\n".join(parts)
    

    def _get_length_guidance(self, content_type: str) -> str:
        """Return appropriate length guidance based on content type"""
        content_lower = content_type.lower()

        if "subject line" in content_lower or "headline" in content_lower:
            return "Keep extremely brief: 5-10 words maximum"
    
        if "tweet" in content_lower:
            return "Keep very brief: 280 characters maximum"
        
        if "social media" in content_lower or "social post" in content_lower:
            return "Keep concise: 50-150 words"
        
        if "google" in content_lower and "ad" in content_lower:  
            return "Keep brief and punchy: 50-100 words"
        
        if "facebook" in content_lower and "ad" in content_lower:
            return "Keep engaging: 100-150 words"
        
        if "ad" in content_lower:
            return "Keep concise: 75-100 words"
        
        if "email intro" in content_lower:
            return "Keep brief: 75-150 words maximum"
        
        if "blog intro" in content_lower:  
            return "Keep concise: 100-200 words - hook the reader and transition to main content"
        
        if "product description" in content_lower:
            return "Aim for 200-350 words"
        
        if "landing page" in content_lower and "hero" in content_lower:
            return "Aim for 250 maximum"
        
        if "landing page" in content_lower:
            return "aim for 250 - 400 words"        
        
        if "blog" in content_lower or "article" in content_lower:  
            return "Aim for 800-1200 words for a complete article"
        
        if "sales page" in content_lower or "long form" in content_lower:
            return "Aim for 600-1000 words"
        
        return "Be concise and impactful"


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