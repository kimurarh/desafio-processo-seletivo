import os
from classes import db

os.remove("pessoas.db")
os.remove("salasevento.db")
os.remove("espacoscafe.db")

db.create_all()
