from typing import Any, List, Optional

from env import get_env, load_dotenv_if_present

try:
    import openai
except Exception:
    openai = None

_client: Optional["openai.OpenAI"] = None


def get_client() -> "openai.OpenAI":
    global _client
    if _client is None:
        if openai is None:
            raise RuntimeError("openai package not installed. pip install openai")
        load_dotenv_if_present()
        api_key = get_env("OPENAI_API_KEY")
        api_base = get_env("OPENAI_API_BASE")
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY not set in environment")
        _client = openai.OpenAI(api_key=api_key, base_url=api_base)
    return _client


def process_with_openai(
    prompts: List[str],
    model: str = "gpt-4o",
    temperature: float = 0.3,
    **kwargs: Any,
) -> List[str]:
    client = get_client()
    out: List[str] = []
    for prompt in prompts:
        try:
            resp = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
                **kwargs,
            )
            if resp.choices:
                out.append(resp.choices[0].message.content or "")
            else:
                out.append("")
        except Exception as e:
            print(f"OpenAI API error for prompt: {prompt[:50]}... Error: {e}")
            out.append("")
    return out
