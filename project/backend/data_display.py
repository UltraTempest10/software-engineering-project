# backend.py

from flask import Flask, request, jsonify
from flask_cors import CORS
import pymysql
from datetime import datetime
from urllib.parse import unquote
from login import create_token, verify_token

app = Flask(__name__)
CORS(app)

# MySQL数据库配置
db_config = {
    'host': '47.102.210.25',
    'user': 'root',
    'password': '@Tongjisseproject2023',
    'database': 'curtain_wall',
    'port': 3306,
    'charset': 'utf8mb4'

}

# Function to create a new database connection and cursor
def create_connection():
    connection = pymysql.connect(**db_config)
    cursor = connection.cursor()
    return connection, cursor

# Function to close the database connection and cursor
def close_connection(connection, cursor):
    cursor.close()
    connection.close()

# 后端接口，用于获取楼宇列表
@app.route('/api/buildings', methods=['GET'])
def get_buildings():
    connection, cursor = create_connection()

    try:
        query = "SELECT DISTINCT name FROM device"
        cursor.execute(query)
        buildings = cursor.fetchall()
        return jsonify(buildings)
    except Exception as e:
        print(f"Error fetching buildings: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500
    finally:
        close_connection(connection, cursor)

# 后端接口，用于获取楼宇对应的设备编号列表
@app.route('/api/devices', methods=['GET'])
def get_devices():
    building = request.args.get('building')
    decoded_building = unquote(building)  # 解码参数
    connection, cursor = create_connection()

    try:
        query = "SELECT id FROM device WHERE name = %s"
        cursor.execute(query, (decoded_building,))
        devices = cursor.fetchall()
        return jsonify(devices)
    except Exception as e:
        print(f"Error fetching devices: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500
    finally:
        close_connection(connection, cursor)

# 后端接口，用于获取所有设备列表
@app.route('/api/all', methods=['GET'])
def get_all_devices():
    connection, cursor = create_connection()

    try:
        query = "SELECT id,name,no FROM device"
        cursor.execute(query)
        devices = cursor.fetchall()
        return jsonify(devices)
    except Exception as e:
        print(f"Error fetching devices: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500
    finally:
        close_connection(connection, cursor)

# 后端接口，用于获取可用日期列表（精确到小时）
@app.route('/api/available_dates', methods=['GET'])
def get_available_dates():
    connection, cursor = create_connection()

    try:
        query = "SELECT DISTINCT DATE_FORMAT(time, '%Y-%m-%d %H:00:00') as time_hour FROM data"
        cursor.execute(query)
        dates = cursor.fetchall()
        return jsonify(dates)
    except Exception as e:
        print(f"Error fetching available dates: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500
    finally:
        close_connection(connection, cursor)

# 后端接口，用于查询设备数据
@app.route('/api/device_data', methods=['POST'])
def get_device_data():
    connection, cursor = create_connection()

    try:
        data = request.json
        device_id = data['device_id']
        start_date = data['start_date']
        end_date = data['end_date']


        query = "SELECT delt_x,delt_y,delt_z FROM data WHERE id = %s AND time BETWEEN %s AND %s"
        cursor.execute(query, (device_id, start_date, end_date))
        device_data = cursor.fetchall()

        return jsonify(device_data)
    except Exception as e:
        print(f"Error fetching device data: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500
    finally:
        close_connection(connection, cursor)

# 后端接口，用于查询设备数据（按事件）
@app.route('/api/device_data_byevent', methods=['POST'])
def get_device_data_byevent():

    connection, cursor = create_connection()

    try:

        data = request.json
        device_id = data['device_id']
        eventname= data['event_name']

        query = "SELECT delt_x, delt_y, delt_z FROM data WHERE id = %s AND time BETWEEN (SELECT start_time FROM event_record WHERE event_name = %s) AND (SELECT end_time FROM event_record WHERE event_name = %s)"
        cursor.execute(query, (device_id,eventname,eventname))
        device_data = cursor.fetchall()

        return jsonify(device_data)
    except Exception as e:
        print(f"Error fetching device data: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500
    finally:
        close_connection(connection, cursor)

# 后端接口，用于查询异常数据
@app.route('/api/anomaly', methods=['POST'])
def get_anomaly():
    connection, cursor = create_connection()

    try:
        data = request.json
        event_name = data['event_name']
        if len(event_name) == 0:
            query = "SELECT id,time,delt_x,delt_y,delt_z FROM anomaly_data ORDER BY time DESC, sequence DESC"
            cursor.execute(query)
        else:
            query = "SELECT id,time,delt_x,delt_y,delt_z FROM anomaly_data WHERE time BETWEEN (SELECT start_time FROM event_record WHERE event_name = %s) AND (SELECT end_time FROM event_record WHERE event_name = %s) ORDER BY time DESC, sequence DESC"
            cursor.execute(query, (event_name, event_name))
        device_data = cursor.fetchall()

        return jsonify(device_data)
    except Exception as e:
        print(f"Error fetching device data: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500
    finally:
        close_connection(connection, cursor)

# 后端接口，用于查询阈值
@app.route('/api/thresholds', methods=['GET'])
def get_threshold():
    connection, cursor = create_connection()

    try:
        query = "SELECT x, y, z FROM threshold"
        cursor.execute(query)
        result = cursor.fetchall()
        if len(result) > 0:
            for (x, y, z) in result:
                threshold_x = x
                threshold_y = y
                threshold_z = z

        return jsonify({'x': threshold_x, 'y': threshold_y, 'z': threshold_z})
    except Exception as e:
        print(f"Error fetching threshold: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500
    finally:
        close_connection(connection, cursor)

# 后端接口，用于修改阈值
@app.route('/api/set_thresholds', methods=['POST'])
def set_threshold():
    connection, cursor = create_connection()

    try:
        data = request.json
        x = data['x']
        y = data['y']
        z = data['z']

        query = "UPDATE threshold SET x = %s, y = %s, z = %s"
        cursor.execute(query, (x, y, z))
        connection.commit()

        return jsonify({'success': True})
    except Exception as e:
        print(f"Error setting threshold: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500
    finally:
        close_connection(connection, cursor)

# 后端接口，用于获取事件列表
@app.route('/api/event_names', methods=['GET'])
def get_event_names():
    connection, cursor = create_connection()

    try:
        query = "SELECT DISTINCT event_name FROM event_record"
        cursor.execute(query)
        event_names = cursor.fetchall()
        return jsonify(event_names)
    except Exception as e:
        print(f"Error fetching event names: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500
    finally:
        close_connection(connection, cursor)

# 后端接口，用于添加事件
@app.route('/api/add_event', methods=['POST'])
def add_event():
    connection, cursor = create_connection()

    try:
        data = request.json

        event_name = data.get('eventName')
        start_time = datetime.strptime(data.get('startDate'), '%Y-%m-%d %H') if data.get('startDate') else None
        end_time = datetime.strptime(data.get('endDate'), '%Y-%m-%d %H') if data.get('endDate') else None

        query = "INSERT INTO event_record (event_name, start_time, end_time) VALUES (%s, %s, %s)"
        cursor.execute(query, (event_name, start_time, end_time))
        connection.commit()

        return jsonify({'success': True})
    except Exception as e:
        print(f"Error adding event: {e}")
        return jsonify({'success': False, 'error': 'Internal Server Error'}), 500
    finally:
        close_connection(connection, cursor)

# 后端接口，用于查询用户信息
@app.route('/api/user', methods=['POST'])
def get_user():
    connection, cursor = create_connection()

    try:
        data = request.json
        username = data['username']
        email = data['email']

        query = "SELECT username FROM user WHERE username = %s"
        cursor.execute(query, (username))
        result = cursor.fetchall()

        query = "SELECT username FROM user WHERE email = %s"
        cursor.execute(query, (email))
        result += cursor.fetchall()

        if len(result) > 0:
            return jsonify({'exist': True})
        else:
            return jsonify({'exist': False})
    except Exception as e:
        print(f"Error fetching user: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500
    finally:
        close_connection(connection, cursor)

# 后端接口，用于增加用户
@app.route('/api/add_user', methods=['POST'])
def add_user():
    connection, cursor = create_connection()

    try:
        data = request.json
        username = data['username']
        password = data['password']
        email = data['email']

        query = "INSERT INTO user (username, password, email) VALUES (%s, %s, %s)"
        cursor.execute(query, (username, password, email))
        connection.commit()

        return jsonify({'success': True})
    except Exception as e:
        print(f"Error adding user: {e}")
        return jsonify({'success': False, 'error': 'Internal Server Error'}), 500
    finally:
        close_connection(connection, cursor)

# 后端接口，用于登录
@app.route('/api/login', methods=['POST'])
def login():
    connection, cursor = create_connection()

    try:
        data = request.json
        username = data['username']
        password = data['password']

        query = "SELECT username FROM user WHERE username = %s AND password = %s"
        cursor.execute(query, (username, password))
        result = cursor.fetchall()

        if len(result) > 0:
            token = create_token(username)
            return jsonify({'success': True, 'token': token})
        else:
            return jsonify({'success': False})
    except Exception as e:
        print(f"Error logging in: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500
    finally:
        close_connection(connection, cursor)

if __name__ == '__main__':
    app.run()
