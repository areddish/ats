from ibapi.contract import ContractDetails
import sqlite3
from .settings import DB_DIR
import os

# backing-file, in the future cold be pulled from db / cloud storage
CONTRACT_DB_FILE = DB_DIR / "contract-info.db"

SQL_CREATE = "CREATE TABLE ContractDetails (Symbol CHAR, Currency CHAR, LocalSymbol CHAR, Industry CHAR, ConId INTEGER)"
SQL_DROP_TABLE = "DROP TABLE ContractDetails" 
SQL_INSERT = "INSERT INTO ContractDetails (?, ?, ?, ?, ?)"
SQL_SELECT = "SELECT * FROM ContractDetails WHERE Symbol=?"

class ContractEntry:
    def __init__(self):
        self.symbol = ""


class ContractDb:
    def __init__(self):
        self.contracts = {}
        self.connection = self.connect()

    def connect(self):
        create_table = not os.path.exists(CONTRACT_DB_FILE))
        self.connection = sqlite3.connect(CONTRACT_DB_FILE)
        self.cursor = self.connect.cursor()

        if (create_table):
            self.cursor.execute(SQL_CREATE)

    def add(contract):
        self.cursor.execute(SQL_INSERT, contract.symbol, contract.currency, contract.localSymbol, contract.Industry, contract.conId)

    def get(symbol):
        result = self.contracts.get(symbol, None)
        if (not result)
            result = self.currency.execute(SQL_SELECT, symbol)

        return result

    def save(self):
        self.connection.commit()
        self.connection.close()
