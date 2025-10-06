# app/services/prompt_builder.py
from textwrap import dedent
from typing import List, Dict
from app.schemas.copy import CopyRequest

def build_prompt(req: CopyRequest) -> List[Dict[str, str]]:
    """Return ordered chat messages for OpenAI API."""

    # === System role ===
    system_msg = dedent("""
    You are an expert direct-response copywriter.
    - Always follow constraints exactly.
    - Include a CTA only if requested.
    - Write in clear, persuasive language.
    - Avoid fluff, filler, and unverifiable claims.
    """)

    # === User message (structured facts + style/constraints) ===
    user_parts = []

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
        user_parts.append(f"Brand voice sample (reference, do not copy verbatim):\n{req.brand_sample}")
    if req.keywords:
        kws = ", ".join(req.keywords)
        user_parts.append(f"Keywords to weave in naturally: {kws}")

    # Guardrails
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

    # Assemble user content
    user_msg = "\n".join(user_parts + ["", *guardrails])

    # Return as chat messages
    return [
        {"role": "system", "content": system_msg.strip()},
        {"role": "user", "content": user_msg.strip()},
        # optional few-shot example could go here
    ]
