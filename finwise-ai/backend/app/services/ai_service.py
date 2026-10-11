from openai import OpenAI
from ..config import settings

def enabled() -> bool:
    return bool(settings.LLM_API_KEY)

def complete(prompt: str, system: str = "You are a precise financial assistant.", json_mode=False) -> str:
    client = OpenAI(api_key=settings.LLM_API_KEY, base_url=settings.LLM_BASE_URL)
    kw = {"response_format": {"type": "json_object"}} if json_mode else {}
    r = client.chat.completions.create(
        model=settings.LLM_MODEL, temperature=0.2,
        messages=[{"role": "system", "content": system}, {"role": "user", "content": prompt}], **kw)
    return r.choices[0].message.content

def finance_context(txns) -> str:
    by_cat, rows = {}, []
    for t in txns:
        by_cat[t.category] = by_cat.get(t.category, 0) + t.amount
        rows.append(f"{t.date}|{t.merchant or t.name}|{t.amount:.2f}|{t.category}")
    summary = ", ".join(f"{k}: ${v:.0f}" for k, v in sorted(by_cat.items(), key=lambda x: -x[1]))
    return f"Category totals (last 90d; positive=spend): {summary}\nRecent transactions:\n" + "\n".join(rows[:150])

def chat(question: str, txns) -> str:
    if not enabled():
        return "Set LLM_API_KEY in backend/.env to enable the AI assistant."
    sys = "You are FinWise, a friendly personal finance assistant. Answer ONLY from the user's data below. Be concise and cite numbers."
    return complete(f"{finance_context(txns)}\n\nQuestion: {question}", system=sys)
