"""
Day 1 — LLM API Foundation
Solution for optional LLM API lab.
"""

import os
import time
from typing import Any, Callable

# ---------------------------------------------------------------------------
# Estimated costs per 1K OUTPUT tokens (USD) — OpenAI pricing page, 11/2026.
# ---------------------------------------------------------------------------
COST_PER_1K_OUTPUT_TOKENS = {
    "gpt-6.1-terra": 0.005,   # $5.00 / 1M output tokens
    "gpt-6-luna": 0.0005,     # $0.50 / 1M output tokens
}

OPENAI_MODEL = "gpt-6.1-terra"
OPENAI_MINI_MODEL = "gpt-6-luna"


# ---------------------------------------------------------------------------
# Task 1 — Call the large model (OPENAI_MODEL)
# ---------------------------------------------------------------------------
def call_openai(
    prompt: str,
    model: str = OPENAI_MODEL,
    temperature: float = 0.7,
    top_p: float = 0.9,
    max_tokens: int = 256,
) -> tuple[str, float]:
    """
    Call the OpenAI Chat Completions API and return the response text + latency.
    """
    from openai import OpenAI
    api_key = os.getenv("OPENAI_API_KEY", "mock-key")
    client = OpenAI(api_key=api_key)

    t0 = time.perf_counter()
    resp = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        reasoning_effort="none",
        temperature=temperature,
        top_p=top_p,
        max_completion_tokens=max_tokens,
    )
    latency = max(time.perf_counter() - t0, 1e-4)
    text = resp.choices[0].message.content or ""
    return text, latency


# ---------------------------------------------------------------------------
# Task 2 — Call the small model (OPENAI_MINI_MODEL)
# ---------------------------------------------------------------------------
def call_openai_mini(
    prompt: str,
    temperature: float = 0.7,
    top_p: float = 0.9,
    max_tokens: int = 256,
) -> tuple[str, float]:
    """
    Call the OpenAI Chat Completions API using OPENAI_MINI_MODEL and return the
    response text + latency.
    """
    return call_openai(
        prompt=prompt,
        model=OPENAI_MINI_MODEL,
        temperature=temperature,
        top_p=top_p,
        max_tokens=max_tokens,
    )


# ---------------------------------------------------------------------------
# Task 3 — Compare the large vs the small model
# ---------------------------------------------------------------------------
def compare_models(prompt: str) -> dict:
    """
    Call both OPENAI_MODEL and OPENAI_MINI_MODEL with the same prompt and return a
    comparison dictionary.
    """
    t_start = time.perf_counter()
    gpt4o_resp, gpt4o_lat = call_openai(prompt, model=OPENAI_MODEL)
    mini_resp, mini_lat = call_openai_mini(prompt)

    cost_rate = COST_PER_1K_OUTPUT_TOKENS.get(OPENAI_MODEL, 0.005)
    cost_estimate = (len(gpt4o_resp.split()) / 0.75) / 1000 * cost_rate

    return {
        "gpt4o_response": gpt4o_resp,
        "mini_response": mini_resp,
        "gpt4o_latency": gpt4o_lat,
        "mini_latency": mini_lat,
        "gpt4o_cost_estimate": cost_estimate,
    }


# ---------------------------------------------------------------------------
# Task 4 — Streaming chatbot with conversation history
# ---------------------------------------------------------------------------
def streaming_chatbot() -> None:
    """
    Run an interactive streaming chatbot in the terminal.
    """
    from openai import OpenAI
    api_key = os.getenv("OPENAI_API_KEY", "mock-key")
    client = OpenAI(api_key=api_key)

    history: list[dict] = []
    print("Starting chatbot. Type 'quit' or 'exit' to end.")

    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            break

        if not user_input or user_input.lower() in ("quit", "exit"):
            break

        history.append({"role": "user", "content": user_input})
        messages_to_send = history[-6:]

        stream = client.chat.completions.create(
            model=OPENAI_MINI_MODEL,
            messages=messages_to_send,
            stream=True,
            reasoning_effort="none",
        )

        reply_parts = []
        for chunk in stream:
            delta = chunk.choices[0].delta.content or ""
            print(delta, end="", flush=True)
            reply_parts.append(delta)
        print()

        history.append({"role": "assistant", "content": "".join(reply_parts)})


# ---------------------------------------------------------------------------
# Bonus Task A — Retry with exponential backoff
# ---------------------------------------------------------------------------
def retry_with_backoff(
    fn: Callable,
    max_retries: int = 3,
    base_delay: float = 0.1,
) -> Any:
    """
    Call fn(). If it raises an exception, retry up to max_retries times
    with exponential backoff (base_delay * 2^attempt).
    """
    last_ex = None
    for attempt in range(max_retries + 1):
        try:
            return fn()
        except Exception as e:
            last_ex = e
            if attempt < max_retries:
                time.sleep(base_delay * (2 ** attempt))
    raise last_ex


# ---------------------------------------------------------------------------
# Bonus Task B — Batch compare
# ---------------------------------------------------------------------------
def batch_compare(prompts: list[str]) -> list[dict]:
    """
    Run compare_models on each prompt in the list.
    """
    results = []
    for p in prompts:
        res = compare_models(p)
        res["prompt"] = p
        results.append(res)
    return results


# ---------------------------------------------------------------------------
# Bonus Task C — Format comparison table
# ---------------------------------------------------------------------------
def format_comparison_table(results: list[dict]) -> str:
    """
    Format a list of compare_models results as a readable text table.
    """
    header = "| Prompt | GPT-4o Response | Mini Response | GPT-4o Latency | Mini Latency |"
    sep = "| :--- | :--- | :--- | :--- | :--- |"
    rows = [header, sep]

    for r in results:
        p = r.get("prompt", "")[:40]
        g_resp = r.get("gpt4o_response", "").replace("\n", " ")[:40]
        m_resp = r.get("mini_response", "").replace("\n", " ")[:40]
        g_lat = f"{r.get('gpt4o_latency', 0.0):.2f}s"
        m_lat = f"{r.get('mini_latency', 0.0):.2f}s"
        rows.append(f"| {p} | {g_resp} | {m_resp} | {g_lat} | {m_lat} |")

    return "\n".join(rows)


if __name__ == "__main__":
    test_prompt = "Explain the difference between temperature and top_p in one sentence."
    print("=== Comparing models ===")
    result = compare_models(test_prompt)
    for k, v in result.items():
        print(f"{k}: {v}")
