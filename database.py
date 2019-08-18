import sqlite3
import numpy as np
import cv2
import os
import io

def adapt_array(arr):
    out = io.BytesIO()
    np.save(out, arr)
    out.seek(0)
    return sqlite3.Binary(out.read())

def convert_array(text):
    out = io.BytesIO(text)
    out.seek(0)
    out = io.BytesIO(out.read())
    return np.load(out)

def insert(j,frameID, player, ball, other, c):
    qu = 'INSERT INTO tab VALUES(?,?,?,?,?)'
    x = tuple([j,frameID, player, ball, other])
    c.execute(qu, x)

def createTable(c):
    sql_create = 'CREATE TABLE IF NOT EXISTS tab (id integer PRIMARY KEY, frameID integer NOT NULL, player arr NOT NULL, ball arr NOT NULL, other arr NOT NULL)'
    c.execute(sql_create)

def getdata(query, Database):
    conn = sqlite3.connect(Database, detect_types=sqlite3.PARSE_DECLTYPES)
    c = conn.cursor()
    c.execute(query)
    rows = c.fetchall()
    conn.close()
    return rows[0]

def addData(table_files):
    length = len(os.listdir(table_files))
    length = 10
    for i in range(0,length):
        conn = sqlite3.connect('./database_folder/data'+str(i+1)+'.db', detect_types=sqlite3.PARSE_DECLTYPES)
        c = conn.cursor()
        createTable(c)

        f = open(table_files+'testfile'+str(i+1)+'.txt', 'r')
        lines=[]
        for line in f:
            line = line.split()
            line[0]=(line[0].split('/')[-1]).split('.')[0]
            line = list(map(int, line))
            print(line)
            lines.append(line)
        f.close()

        prev = lines[0][0]
        num = len(lines)
        player=[]
        ball=[]
        other=[]
        frameID=0
        for j in range(num):
            if(lines[j][0]!=prev):
                player=np.asarray(player)
                ball = np.asarray(ball)
                other = np.asarray(other)
                frameID+=1
                insert(j+1, prev, player, ball, other, c)
                player=[]
                ball=[]
                other=[]
                prev = lines[j][0]

            if(lines[j][1]==1):
                player.append([lines[j][2], lines[j][3], lines[j][4], lines[j][5]])

            elif(lines[j][1]==2):
                ball.append([lines[j][2], lines[j][3], lines[j][4], lines[j][5]])

            else:
                other.append([lines[j][2], lines[j][3], lines[j][4], lines[j][5]])
        frameID += 1
        player = np.asarray(player, dtype=np.int_)
        ball = np.asarray(ball, dtype=np.int_)
        other = np.asarray(other, dtype=np.int_)
        insert(num+1,lines[num-1][0], player, ball, other,c)
        # print([i+1, lines[num-1][0]])
        conn.commit()
        conn.close()

    return

def main():
    dir = './txtfiles/'
    sqlite3.register_adapter(np.ndarray, adapt_array)
    sqlite3.register_converter("arr", convert_array)
    addData(dir)
    print(getdata("SELECT * FROM tab WHERE frameID=99", 'database_folder/data1.db'))

if __name__ == '__main__':
    main()
