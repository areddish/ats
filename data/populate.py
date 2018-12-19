import sqlite3


def create_table():
    # Create a table to hold data or return existing table
    pass


def insert_bar(table, dt, open, high, low, close, volume, bar_count):
    # Insert a bar as a row
    #c.execute("INSERT INTO ? VALUES (?, ?, ?, ?, ?, ?, ?)", table, dt, open, high, low, close, volume, bar_count)
    pass


def insert_bars(table, bars):
    # Insert a list of bars
    #c.executemany("INSERT INTO ? VALUES (?, ?, ?, ?, ?, ?, ?)", table, bars)
    pass


if __name__ == "__main__":
    print("Creating")
    connection = sqlite3.connect('stock.db')
    c = connection.cursor()

    # Create table, if missing
    table_name = create_table()

    # 1. find all files
    # 2. for each file, parse out the lines and insert
    
    connection.commit()
    connection.close()
