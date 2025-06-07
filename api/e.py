# ... existing code ...
#http://127.0.0.1:5000/api/softdata?limit=20&page=2
# 配置项 (建议放在配置文件或环境变量中)
# SECRET_KEY = "QWErty56"  # 替换为强密钥
# TOKEN_EXPIRE_HOURS = 24

# @app.route('/api/auth/register', methods=['POST'])
# def register():
#     try:
#         # 获取注册数据
#         register_data = request.get_json()
#         username = register_data.get('username')
#         password = register_data.get('password')
        
#         if not username or not password:
#             return jsonify({'error': '用户名和密码不能为空'}), 400

#         # 密码加密
#         hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

#         # 连接数据库
#         conn = pymysql.connect(**DB_CONFIG)
#         with conn.cursor() as cursor:
#             # 检查用户名是否已存在
#             cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
#             if cursor.fetchone():
#                 return jsonify({'error': '用户名已存在'}), 400

#             # 插入新用户
#             cursor.execute(
#                 "INSERT INTO users (username, password) VALUES (%s, %s)",
#                 (username, hashed_password.decode('utf-8'))
#             )
#             conn.commit()
        
#         return jsonify({'message': '注册成功'}), 201
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500
#     finally:
#         if conn:
#             conn.close()

# @app.route('/api/auth/login', methods=['POST'])
# def login():
#     try:
#         # 确保是 JSON 请求
#         if not request.is_json:
#             return jsonify({'error': 'Missing JSON in request'}), 400

#         login_data = request.get_json(force=True, silent=True)

#         if login_data is None:
#             return jsonify({'error': 'Invalid JSON format'}), 400

#         username = login_data.get('username')
#         password = login_data.get('password')
#         remember_me = bool(login_data.get('rememberMe', False))  # 强制转为布尔值

#         if not username or not password:
#             return jsonify({'error': '用户名和密码不能为空'}), 400

#         conn = pymysql.connect(**DB_CONFIG)
#         with conn.cursor(pymysql.cursors.DictCursor) as cursor:
#             cursor.execute("SELECT id, password FROM users WHERE username = %s", (username,))
#             user = cursor.fetchone()

#             if not user:
#                 return jsonify({'error': '用户不存在'}), 401

#             if not bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
#                 return jsonify({'error': '密码错误'}), 401

#             expire_hours = TOKEN_EXPIRE_HOURS * 2 if remember_me else TOKEN_EXPIRE_HOURS
#             token = jwt.encode({
#                 'user_id': user['id'],
#                 'username': username,
#                 'exp': datetime.utcnow() + timedelta(hours=expire_hours)
#             }, SECRET_KEY, algorithm='HS256')

#         return jsonify({
#             'token': token,
#             'username': username,
#             'expires_in': expire_hours * 3600
#         })

#     except Exception as e:
#         print(f"Error during login: {e}")  # 打印错误日志
#         return jsonify({'error': '服务器内部错误，请稍后再试'}), 500

#     finally:
#         if conn:
#             conn.close()
