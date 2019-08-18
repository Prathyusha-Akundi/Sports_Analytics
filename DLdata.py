import sqlite3
import numpy as np
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

def connectDB(DATABASE):
    sqlite3.register_adapter(np.ndarray, adapt_array)
    sqlite3.register_converter("arr", convert_array)
    conn = sqlite3.connect(DATABASE, detect_types=sqlite3.PARSE_DECLTYPES)
    return conn

def getFrameData(conn, frameNum):
    query = "SELECT * FROM tab WHERE frameID = "+str(frameNum)
    c = conn.cursor()
    c.execute(query)
    row = c.fetchall()[0]
    playerData = row[2]
    ballData = row[3]
    goalData = row[4]
    return playerData, ballData, goalData

def getPlayersMask(playerData, ballData):
    img = np.ones((1080,1920), np.uint8)

    for l in range(len(playerData)):
        img[playerData[l][1]:playerData[l][3]+1,playerData[l][0]:playerData[l][2]+1]=np.zeros((playerData[l][3]-playerData[l][1]+1,playerData[l][2]-playerData[l][0]+1))
    for l in range(len(ballData)):
        img[ballData[l][1]:ballData[l][3]+1,ballData[l][0]:ballData[l][2]+1]=np.zeros((ballData[l][3]-ballData[l][1]+1,ballData[l][2]-ballData[l][0]+1))

    return img


def disconnectDB(conn):
    conn.close()

if __name__ == '__main__':
    dbDir = '../DB/data1.db'
    db = connectDB(dbDir)
    playerData, ballData, goalData = getFrameData(db, 68)
    disconnectDB(db)
    print(playerData, ballData, goalData)
