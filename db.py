from tinydb import TinyDB, table, Query
import os

db = TinyDB('epic_tools.json', sort_keys=True, indent=4)

FIRST_RUN = True

file_paths = db.table('file_paths')
miners = db.table('miners')
users = db.table('user')
wallets = db.table("wallets")
configs = db.table("configs")


if not users.get(doc_id=1):
    users.insert({'first_run': True})
else:
    pass
