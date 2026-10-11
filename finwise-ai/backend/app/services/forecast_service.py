import pandas as pd
from collections import defaultdict
from datetime import timedelta

def forecast_spending(txns, days: int = 30) -> list[dict]:
    daily = defaultdict(float)
    for t in txns:
        if t.amount > 0 and t.category != "Income":
            daily[t.date] += t.amount
    if len(daily) < 14:
        return []
    df = pd.DataFrame({"ds": pd.to_datetime(list(daily)), "y": list(daily.values())})
    df = df.set_index("ds").asfreq("D", fill_value=0).reset_index()
    try:
        from prophet import Prophet
        m = Prophet(daily_seasonality=False, weekly_seasonality=True)
        m.fit(df)
        fc = m.predict(m.make_future_dataframe(periods=days)).tail(days)
        return [{"date": r.ds.date().isoformat(), "predicted": max(0, round(r.yhat, 2))} for r in fc.itertuples()]
    except Exception:  # fallback: 14-day moving average
        avg = df["y"].tail(14).mean()
        last = df["ds"].max()
        return [{"date": (last + timedelta(days=i + 1)).date().isoformat(), "predicted": round(avg, 2)} for i in range(days)]

def detect_subscriptions(txns) -> list[dict]:
    groups = defaultdict(list)
    for t in txns:
        if t.amount > 0:
            groups[(t.merchant or t.name).lower()].append(t)
    subs = []
    for name, ts in groups.items():
        if len(ts) < 3:
            continue
        ts.sort(key=lambda x: x.date)
        gaps = [(b.date - a.date).days for a, b in zip(ts, ts[1:])]
        amts = [x.amount for x in ts]
        if all(26 <= g <= 35 for g in gaps) and max(amts) - min(amts) <= 0.1 * max(amts):
            subs.append({"merchant": name.title(), "amount": round(amts[-1], 2), "last_charge": ts[-1].date.isoformat(),
                         "annual_cost": round(amts[-1] * 12, 2)})
    return sorted(subs, key=lambda s: -s["amount"])
