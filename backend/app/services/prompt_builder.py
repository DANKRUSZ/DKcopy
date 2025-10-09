from textwrap import dedent
from typing import List
from app.schemas.copy import CopyRequest
from app.services.llm.types import Message, Messages  # keep if you return Messages

def build_prompt(req: CopyRequest) -> Messages:
    system_msg = dedent("""
    You are an expert direct-response copywriter.
    - Always follow constraints exactly.
    - Include a CTA only if requested.
    - Write in clear, persuasive language.
    - Avoid fluff, filler, and unverifiable claims.
    """)
    user_parts: List[str] = []
    user_parts.append(f"Content type: {req.content_type}")
    if req.audience:
        user_parts.append(f"Audience: {req.audience}")
    if req.product_info:
        user_parts.append(f"Product/Service: {req.product_info}")
    if req.tone_of_voice:
        user_parts.append(f"Tone of voice: {req.tone_of_voice}")
    if req.style:
        user_parts.append(f"Style controls: {req.style}")
    if req.brand_sample:
        user_parts.append("Brand voice sample (reference, do not copy verbatim):\n" + req.brand_sample)
    if req.keywords:
        user_parts.append("Keywords to weave in naturally: " + ", ".join(req.keywords))

    guardrails = [
        "Constraints:",
        "- Write for clarity and persuasion; connect features to outcomes.",
        "- UK English spelling if ambiguous.",
        "- Do not add headings, notes, or meta commentary.",
        "- Do not invent product details not provided.",
    ]
    if req.cta:
        guardrails.append("End with one clear call-to-action.")
    else:
        guardrails.append("Do not include a call-to-action.")

    user_msg = "\n".join(user_parts + ["", *guardrails])

    system: Message = {"role": "system", "content": system_msg.strip()}
    user: Message = {"role": "user", "content": user_msg.strip()}
    return [system, user]
