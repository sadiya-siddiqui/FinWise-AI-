import json
from . import ai_service

RULES = {
    "Groceries": ["walmart", "kroger", "whole foods", "trader joe", "aldi", "costco"],
    "Dining": ["starbucks", "mcdonald", "chipotle", "restaurant", "cafe", "doordash", "uber eats"],
    "Transport": ["uber", "lyft", "shell", "chevron", "exxon", "transit"],
    "Subscriptions": ["netflix", "spotify", "hulu", "disney", "prime", "icloud", "youtube"],
    "Utilities": ["electric", "water", "comcast", "verizon", "at&t", "internet"],
    "Housing": ["rent", "mortgage"],
    "Income": ["payroll", "direct deposit", "salary"],
}
CATS = list(RULES) + ["Shopping", "Health", "Entertainment", "Travel", "Other"]

def rule_category(name: str):
    n = name.lower()
    for cat, kws in RULES.items():
        if any(k in n for k in kws):
            return cat

def categorize_batch(names: list[str]) -> dict[str, str]:
    out = {n: rule_category(n) for n in names}
    todo = [n for n, c in out.items() if not c]
    if todo and ai_service.enabled():
        try:
            raw = ai_service.complete(
                f"Categorize each merchant into one of {CATS}. Reply ONLY JSON object {{name: category}}.\n{json.dumps(todo[:50])}",
                json_mode=True)
            for n, c in json.loads(raw).items():
                out[n] = c if c in CATS else "Other"
        except Exception:
            pass
    return {n: c or "Other" for n, c in out.items()}
