import os
import json
from hashlib import sha256
from dotenv import load_dotenv

load_dotenv()


class AuthManager:
    def __init__(self, salt=os.environ.get("SALT")):
        self.SALT = salt
        self.db_path = "/srv/code-jam/src/creds.json"
        self.db_file = open(self.db_path, "r+")
        self.db = json.load(self.db_file)

    def test(self):
        print(self.db)

    def check(self, uid):
        return uid in self.db.keys()

    def add(self, uid):
        SECRET_SALT = os.environ.get("SALT")
        if not self.check(uid):
            hash_hex = sha256(f"{uid}{SECRET_SALT}".encode()).hexdigest()
            self.db[uid] = hash_hex
            self.apply()
            return True

    def flush(self):
        self.db = {}
        self.apply()
        return True

    def get(self, uid):
        return self.db[uid] if uid in self.db else False

    def remove(self, uid):  # Needs fix
        try:
            self.db.pop(uid, None)
            self.apply()
            return True
        except Exception:
            return False

    def apply(self):
        try:
            self.db_file.seek(0)
            json.dump(self.db, self.db_file, ensure_ascii=False, indent=2)
            return True
        except Exception:
            return False
