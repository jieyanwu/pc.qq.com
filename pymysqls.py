import json
import pymysql
# ... existing code ...
from db_config import DB_CONFIG
from all import merged_data
#... existing code...
# ... existing code ...
# 创建 softdata 表
def create_softdata_table(conn):
    sql = """
    CREATE TABLE IF NOT EXISTS softdata (
        s INTEGER,
        c INTEGER,
        p INTEGER,
        sn VARCHAR(255),
        num INTEGER,
        lg VARCHAR(255),
        ver VARCHAR(50),
        fs VARCHAR(50),
        url VARCHAR(255),
        star INTEGER,
        ux INTEGER,
        tx INTEGER,
        fe TEXT,
        detailUrl VARCHAR(255),
        os_type INTEGER,
        os_bit INTEGER,
        display_name VARCHAR(255),
        nick_ver VARCHAR(50),
        ver_name VARCHAR(50),
        file_size VARCHAR(20),
        file_name VARCHAR(255),
        publish_date DATE,
        download_url TEXT,
        download_https_url TEXT,
        Logo48File TEXT,
        PRIMARY KEY (s)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """
    with conn.cursor() as cursor:
        cursor.execute(sql)
    conn.commit()

# 插入数据到 softdata 表
def insert_data_to_softdata(conn, data):
    sql = """
    INSERT IGNORE INTO softdata (
        s, c, p, sn, num, lg, ver, fs, url, star,
        ux, tx, fe, detailUrl, os_type, os_bit, display_name, nick_ver,
        ver_name, file_size, file_name, publish_date, download_url, download_https_url, Logo48File
    ) VALUES (
        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
        %s, %s, %s, %s, %s
    )
    """
    with conn.cursor() as cursor:
        cursor.executemany(sql, data)
    conn.commit()

if __name__ == '__main__':
    try:
        # 连接数据库
        conn = pymysql.connect(**DB_CONFIG)
        # 创建表
        create_softdata_table(conn)
        # 读取 all.json 文件
        with open('d:/Github/pc.qq.com/data/all.json', 'r', encoding='utf-8') as f:
            json_data = json.load(f)
        # 准备数据
        data_to_insert = [(
            item.get('s'), item.get('c'), item.get('p'), item.get('sn'), item.get('num'),
            item.get('lg'), item.get('ver'), item.get('fs'), item.get('url'), item.get('star'),
            item.get('ux'), item.get('tx'), item.get('fe'), item.get('detailUrl'), item.get('os_type'),
            item.get('os_bit'), item.get('display_name'), item.get('nick_ver'), item.get('ver_name'),
            item.get('file_size'), item.get('file_name'), item.get('publish_date'), item.get('download_url'),
            item.get('download_https_url'), item.get('Logo48File')
        ) for item in json_data]
        # 插入数据
        insert_data_to_softdata(conn, data_to_insert)
        print('数据插入成功')
    except Exception as e:
        print(f'发生错误: {e}')
    finally:
        if conn:
            conn.close()