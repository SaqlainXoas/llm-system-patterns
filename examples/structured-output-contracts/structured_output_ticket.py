import json
import os
from typing import Literal

from google import genai
from pydantic import BaseModel, Field


class TicketDecision(BaseModel):
    category: Literal["billing", "technical", "account", "other"]
    priority: Literal["low", "medium", "high"]
    summary: str = Field(min_length=1, max_length=160)
    requires_human_review: bool


def build_prompt(ticket_text: str) -> str:
    """Return one small routing prompt for the model."""
    return f"""
Classify this support ticket.

Return:
- category: one of billing, technical, account, other
- priority: one of low, medium, high
- summary: one short sentence
- requires_human_review: boolean

Ticket:
{ticket_text}
""".strip()


def classify_ticket(ticket_text: str) -> TicketDecision:
    """Ask Gemini for structured output and validate it as application data."""
    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    prompt = build_prompt(ticket_text)

    # 1. Define the application contract once.
    schema = TicketDecision.model_json_schema()

    # 2. Ask the provider for structured output using that contract.
    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=prompt,
        config={
            "response_format": {
                "text": {
                    "mime_type": "application/json",
                    "schema": schema,
                }
            }
        },
    )

    # 3. Validate before the rest of the application uses the result.
    return TicketDecision.model_validate_json(response.text)


def build_ticket_payload(decision: TicketDecision) -> dict:
    """Convert the typed object into normal JSON-safe application data."""
    return decision.model_dump(mode="json")


def run_demo() -> None:
    """Show the full contract flow from prompt to validated payload."""
    ticket_text = (
        "I was charged twice for the same subscription renewal. "
        "Please fix this and confirm whether I will get a refund."
    )

    decision = classify_ticket(ticket_text)
    payload = build_ticket_payload(decision)

    print("Typed object:")
    print(decision)
    print()
    print("Payload:")
    print(json.dumps(payload, indent=2))
    print()
    print(
        "Note: The same contract pattern works with OpenAI and other providers "
        "that support structured output. The API call changes, but the schema "
        "and validation boundary should stay stable."
    )


if __name__ == "__main__":
    run_demo()
