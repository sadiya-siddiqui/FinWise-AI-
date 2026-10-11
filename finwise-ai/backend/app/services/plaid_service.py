import plaid
from datetime import date
from plaid.api import plaid_api
from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser
from plaid.model.products import Products
from plaid.model.country_code import CountryCode
from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest
from plaid.model.accounts_get_request import AccountsGetRequest
from plaid.model.transactions_sync_request import TransactionsSyncRequest
from sqlalchemy.orm import Session
from ..config import settings
from ..models import Account, Transaction
from . import categorizer
from ..utils.cache import invalidate

_hosts = {"sandbox": plaid.Environment.Sandbox, "production": plaid.Environment.Production}
_client = plaid_api.PlaidApi(plaid.ApiClient(plaid.Configuration(
    host=_hosts.get(settings.PLAID_ENV, plaid.Environment.Sandbox),
    api_key={"clientId": settings.PLAID_CLIENT_ID, "secret": settings.PLAID_SECRET})))

def create_link_token(user_id: int) -> str:
    req = LinkTokenCreateRequest(products=[Products("transactions")], client_name="FinWise AI",
                                 country_codes=[CountryCode("US")], language="en",
                                 user=LinkTokenCreateRequestUser(client_user_id=str(user_id)))
    return _client.link_token_create(req)["link_token"]

def exchange_and_store(db: Session, user_id: int, public_token: str, institution: str = ""):
    ex = _client.item_public_token_exchange(ItemPublicTokenExchangeRequest(public_token=public_token))
    token, item_id = ex["access_token"], ex["item_id"]
    for a in _client.accounts_get(AccountsGetRequest(access_token=token))["accounts"]:
        if db.query(Account).filter_by(plaid_account_id=a["account_id"]).first():
            continue
        db.add(Account(user_id=user_id, plaid_account_id=a["account_id"], item_id=item_id, access_token=token,
                       name=a["name"], institution=institution, type=str(a["type"]),
                       balance=a["balances"]["current"] or 0))
    db.commit()
    sync_user(db, user_id)

def sync_user(db: Session, user_id: int) -> int:
    accounts = db.query(Account).filter_by(user_id=user_id).all()
    by_plaid = {a.plaid_account_id: a for a in accounts}
    added_total = 0
    for token in {a.access_token for a in accounts}:
        group = [a for a in accounts if a.access_token == token]
        cursor, new = group[0].cursor or "", []
        while True:
            r = _client.transactions_sync(TransactionsSyncRequest(access_token=token, cursor=cursor))
            new += r["added"]
            for rm in r["removed"]:
                db.query(Transaction).filter_by(plaid_txn_id=rm["transaction_id"]).delete()
            cursor = r["next_cursor"]
            if not r["has_more"]:
                break
        cats = categorizer.categorize_batch(list({t["name"] for t in new}))
        for t in new:
            acc = by_plaid.get(t["account_id"])
            if not acc or db.query(Transaction).filter_by(plaid_txn_id=t["transaction_id"]).first():
                continue
            db.add(Transaction(user_id=user_id, account_id=acc.id, plaid_txn_id=t["transaction_id"],
                               date=t["date"] if isinstance(t["date"], date) else date.fromisoformat(t["date"]),
                               name=t["name"], merchant=t.get("merchant_name") or "", amount=t["amount"],
                               category=cats.get(t["name"], "Other"), pending=t["pending"]))
            added_total += 1
        for a in group:
            a.cursor = cursor
    db.commit()
    invalidate(user_id)
    return added_total
