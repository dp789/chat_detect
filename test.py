import sqlite3

conn = sqlite3.connect("data.db")
# qq = "insert into user_token values (6, 'hoho', 'sdasdasd', '127.0.0.1')"
# co = conn.execute(qq)
# for i in co:
#     print(i)
# qq = "insert into messages values (6, '123.213.213.32', 'hoho', '321.23.3.2', 'jj', 'hi hi hi')"
# co = conn.execute(qq)
conn.commit()
conn.close()