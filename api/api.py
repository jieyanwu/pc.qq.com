import json
import pymysql
from flask import Flask, request, jsonify
from db_config import DB_CONFIG
from flask_cors import CORS
import jwt
import bcrypt
from datetime import datetime, timedelta

app = Flask(__name__)
CORS(app)  # 允许所有来源的跨域请求

'''做一个传入图片的接口，返回图片的{
          url: 'https://tse4-mm.cn.bing.net/th/id/OIP-C.5Wknt3nVBaNOypsHBJoMaAHaEK?w=279&h=180&c=7&r=0&o=5&dpr=1.5&pid=1.7',
          caption: '683c92147b8a2.jpg'
        }
'''
@app.route('/api/image', methods=['POST', 'GET'])
def handle_images():
    if request.method == 'POST':
        """
        POST方法 - 上传图片信息到MySQL
        输入: {"url": "图片链接"}
        输出: {
            "id": "数据库记录ID",
            "url": "图片链接",
            "caption": "从链接提取的文件名",
            "status": "success/error"
        }
        """
        try:
            data = request.get_json()
            url = data.get('url')
            
            if not url:
                return jsonify({'error': 'url parameter is required'}), 400
            
            caption = url.split('/')[-1]
            
            conn = pymysql.connect(**DB_CONFIG)
            with conn.cursor() as cursor:
                sql = "INSERT INTO loverimages (url, caption) VALUES (%s, %s)"
                cursor.execute(sql, (url, caption))
                record_id = cursor.lastrowid
                conn.commit()
                
            return jsonify({
                'id': record_id,
                'url': url,
                'caption': caption,
                'status': 'success'
            }), 200
            
        except Exception as e:
            return jsonify({
                'error': str(e),
                'status': 'error'
            }), 500
            
        finally:
            if 'conn' in locals() and conn:
                conn.close()

    elif request.method == 'GET':
        """
        GET方法 - 从MySQL获取图片数据
        输入: 可选参数 limit, page
        输出: {
            "images": [
                {
                    "id": "记录ID", 
                    "url": "图片链接",
                    "caption": "文件名",
                    "created_at": "创建时间"
                },
                ...
            ],
            "total": "总记录数",
            "page": "当前页码",
            "status": "success/error"
        }
        """
        try:
            limit = request.args.get('limit', default=10, type=int)
            page = request.args.get('page', default=1, type=int)
            offset = (page - 1) * limit
            
            conn = pymysql.connect(**DB_CONFIG)
            with conn.cursor(pymysql.cursors.DictCursor) as cursor:
                # 获取总记录数
                cursor.execute("SELECT COUNT(*) as total FROM loverimages")
                total = cursor.fetchone()['total']
                
                # 获取分页数据
                sql = """
                    SELECT id, url, caption, created_at 
                    FROM loverimages 
                    ORDER BY created_at DESC 
                    LIMIT %s OFFSET %s
                """
                cursor.execute(sql, (limit, offset))
                images = cursor.fetchall()
            
            return jsonify({
                'images': images,
                'total': total,
                'page': page,
                'status': 'success'
            }), 200
            
        except Exception as e:
            return jsonify({
                'error': str(e),
                'status': 'error'
            }), 500
            
        finally:
            if 'conn' in locals() and conn:
                conn.close()
@app.route('/api/softdata/search', methods=['GET'])
def search_softdata():
    # 获取查询参数
    keyword = request.args.get('keyword', default=None, type=str)
    limit = request.args.get('limit', default=10, type=int)
    page = request.args.get('page', default=1, type=int)
    offset = (page - 1) * limit

    if not keyword:
        return jsonify({'error': 'keyword parameter is required'}), 400

    try:
        # 连接数据库
        conn = pymysql.connect(**DB_CONFIG)
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            # 构建搜索查询语句 (假设我们搜索name和description字段)
            sql = """
                SELECT * FROM softdata 
                WHERE sn LIKE %s OR fe LIKE %s
                LIMIT %s OFFSET %s
            """
            search_pattern = f'%{keyword}%'
            cursor.execute(sql, (search_pattern, search_pattern, limit, offset))
            results = cursor.fetchall()

        return jsonify({
            'results': results,
            'total': len(results),
            'keyword': keyword
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if conn:
            conn.close()
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