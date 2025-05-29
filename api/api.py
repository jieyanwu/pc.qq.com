import json
import pymysql
from flask import Flask, request, jsonify
from db_config import DB_CONFIG
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # 允许所有来源的跨域请求
# ... existing code ...
#http://127.0.0.1:5000/api/softdata?limit=20&page=2

@app.route('/api/softdata', methods=['GET'])
def get_softdata():
    # 获取查询参数
    limit = request.args.get('limit', default=10, type=int)
    page = request.args.get('page', default=1, type=int)
    offset = (page - 1) * limit

    try:
        # 连接数据库
        conn = pymysql.connect(**DB_CONFIG)
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            # 构建查询语句
            sql = "SELECT * FROM softdata LIMIT %s OFFSET %s"
            cursor.execute(sql, (limit, offset))
            results = cursor.fetchall()

        return jsonify(results)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    # 启动 Flask 应用
    app.run(debug=True)