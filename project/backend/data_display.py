# backend.py

from flask import Flask, request, jsonify
from flask_cors import CORS
import pymysql
from datetime import datetime
from urllib.parse import unquote

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

# 后端接口，用于查询异常数据
@app.route('/api/anomaly', methods=['POST'])
def get_anomaly():
    connection, cursor = create_connection()

    try:
        now = datetime.now().strftime("%Y-%m-%d %H")
        data = request.json
        device_id = data.get('device_id', 'all')
        start_date = data.get('start_date', '2023-11-11 11:11:11')
        end_date = data.get('end_date', now)

        if device_id == 'all':
            query = "SELECT id,time,delt_x,delt_y,delt_z FROM anomaly_data WHERE time BETWEEN %s AND %s ORDER BY time DESC"
            cursor.execute(query, (start_date, end_date))
        else:
            query = "SELECT id,time,delt_x,delt_y,delt_z FROM anomaly_data WHERE id = %s AND time BETWEEN %s AND %s ORDER BY time DESC"
            cursor.execute(query, (device_id, start_date, end_date))
        # query = "SELECT delt_x,delt_y,delt_z FROM data WHERE id = %s AND time BETWEEN %s AND %s"
        # cursor.execute(query, (device_id, start_date, end_date))
        device_data = cursor.fetchall()

        return jsonify(device_data)
    except Exception as e:
        print(f"Error fetching device data: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500
    finally:
        close_connection(connection, cursor)

if __name__ == '__main__':
    app.run()
