import time
import requests

from app.config import settings


SYSTEM_MESSAGE = (
    "You are CloudCampus AI Bot. Your users are university students. "
    "Your replies should be conversational, informative, use simple words, and be straightforward."
)


def build_hkbu_url() -> str:
    """Construct the HKBU Azure-style chat completion URL."""
    return (
        f"{settings.hkbu_base_url}/deployments/"
        f"{settings.hkbu_model}/chat/completions"
        f"?api-version={settings.hkbu_api_ver}"
    )


def estimate_cost_usd() -> float:
    """
    Placeholder value.
    HKBU internal API may not expose direct billing details to students.
    You can refine this later if your course expects a custom estimate.
    """
    return 0.0


def generate_reply(user_message: str) -> dict:
    """
    Call the HKBU AI API and return the model reply and response metadata.
    """
    url = build_hkbu_url()
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "api-key": settings.hkbu_api_key,
    }

    payload = {
        "messages": [
            {"role": "system", "content": SYSTEM_MESSAGE},
            {"role": "user", "content": user_message},
        ],
        "temperature": 1,
        "max_tokens": 150,
        "top_p": 1,
        "stream": False,
    }

    start_time = time.perf_counter()
    response = requests.post(url, json=payload, headers=headers, timeout=60)
    elapsed_ms = int((time.perf_counter() - start_time) * 1000)

    if response.status_code != 200:
        raise RuntimeError(f"HKBU API error: {response.text}")

    data = response.json()
    reply_text = data["choices"][0]["message"]["content"].strip()

    usage = data.get("usage", {})
    prompt_tokens = usage.get("prompt_tokens", 0)
    completion_tokens = usage.get("completion_tokens", 0)

    return {
        "reply_text": reply_text,
        "prompt_tokens": prompt_tokens,
        "completion_tokens": completion_tokens,
        "estimated_cost": estimate_cost_usd(),
        "response_time_ms": elapsed_ms,
        "raw_response": data,
    }