import sqlite3
import re

thresh = 1
def check(msg):
    f = open(r"dictionary.txt", "r")
    msg = msg.strip()
    s = f.readlines()
    a_count = 0
    for st in s:
        print(msg)
        print(st)
        # msg = "hi hi hi hi hi"
        st = "hi"
        print(msg.count(st))
        a_count = a_count + msg.count(st.strip())
        # print(count)
    print(a_count)
    f.close()
    if a_count >= thresh:
        return True
    return False

conn = sqlite3.connect('data.db')
query = 'select username from user_token'
cursor = conn.execute(query)
l = []
for row in cursor:
    l.append(row[0])

danger = []

queryy = "select * from messages"
zz = conn.execute(queryy)
for i in zz:
    print(i)
flagged_conv = []
for i in range(0, len(l)):
    for j in range(i, len(l)):
        query2 = "select * from messages where (from_username = '" + l[i] + "'and to_username = '" + l[j] + "') or (from_username = '" + l[j] + "'and to_username = '" + l[i] + "')"
        cursor2 = conn.execute(query2)
        msg = ""
        checkmsg = ""
        for k in cursor2:
            msg = msg + k[2] + "(" + k[1] + ")" + ": " + k[5] + "\n"
            checkmsg = checkmsg + " " + str(k[5])
        if(msg != ""):
            print(msg)
        if(check(checkmsg)):
            danger.append((i, j))
            flagged_conv.append(msg)

f = open("flagged_messages.txt", "w")
for i in flagged_conv:
    f.writelines(i + "\n")
f.close()
conn.close()