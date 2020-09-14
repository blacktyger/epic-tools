from tinydb import TinyDB, table, Query
import os

db = TinyDB('epic_tools.json', sort_keys=True, indent=4)

FIRST_RUN = True

file_paths = db.table('file_paths')
miners = db.table('miners')
user = db.table('user')
wallets = db.table("wallets")
configs = db.table("configs")


if not user.get(doc_id=1):
    user.insert({'first_run': True})
else:
    pass
