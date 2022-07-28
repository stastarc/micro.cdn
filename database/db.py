from pymysqlpool.pool import Pool
from env import DatabaseEnv

pool: Pool

def init():
    global pool
    pool = Pool(
        host=DatabaseEnv.HOST,
        port=int(DatabaseEnv.PORT),
        user=DatabaseEnv.USERNAME,
        password=DatabaseEnv.PASSWORD,
        db=DatabaseEnv.DATABASE,
        autocommit=True,
        min_size=20,
        max_size=80,
        timeout=10.0,
        ping_check=5,
        interval=200
    )

def destroy():
    pool.destroy()

def execute(sql, args=None):
    conn = pool.get_conn()
    cursor = conn.cursor()
    e = cursor.execute(sql, args)
    pool.release(conn)
    return e

def fetchone(sql, args=None):
    conn = pool.get_conn()
    cursor = conn.cursor()
    cursor.execute(sql, args)
    result = cursor.fetchone()
    pool.release(conn)
    return result

def fetchall(sql, args=None):
    conn = pool.get_conn()
    cursor = conn.cursor()
    cursor.execute(sql, args)
    result = cursor.fetchall()
    pool.release(conn)
    return result
