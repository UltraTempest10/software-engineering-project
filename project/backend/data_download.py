# data_download.py: 从平台下载数据，保存到数据库中，并发送邮件通知

# import argparse

import os
import shutil
import math

from datetime import datetime, timedelta
import requests
import zipfile
import pandas as pd

import mysql.connector
from mysql.connector import Error

from mail import alarm

# 解析命令行参数
# parser = argparse.ArgumentParser()
# # parser.add_argument('--group_num', type=int, default=500, help='number of data in each group')
# parser.add_argument('--txy', type=float, default=6.0, help='threshold of x and y')
# parser.add_argument('--tz', type=float, default=18.0, help='threshold of z')
# args = parser.parse_args()

# 文件夹路径
root_path = '/root/curtain_wall/data'
# root_path = 'E:/test'

# 登录信息
login_url = 'https://diggerinspection.cn/doLogin'
login_payload = {
    'username': 'lu',
    'password': 'tj221204'
}

# 数据库连接信息
db_user = 'root'
db_password = '@Tongjisseproject2023'
db_host = '47.102.210.25'
db_port = 3306
database = 'curtain_wall'

# 设备名称
device_id = ['4787BE3A', '8850A7D7', '7749E4D9', 'E884C99D', 'E43AC643', '29FA1867', '350E6EFF', 'F853ED49', 'A77C5238']
# 失效设备: '7A6BA8C8', '3326F78D'

# 阈值
# threshold_x_y = args.txy
# threshold_z = args.tz
threshold_x = 6.0
threshold_y = 6.0
threshold_z = 18.0

email_list = []

def clear_dir(path):
    for filename in os.listdir(path):
        # 构造文件或文件夹的绝对路径
        file_path = os.path.join(path, filename)
        try:
            # 如果是文件，则删除
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            # 如果是文件夹，则删除整个文件夹
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

def mod(x, y, z):
    return math.sqrt(x**2 + y**2 + z**2)

cnx = None
cursor = None

try:
    # 连接MySQL数据库
    cnx = mysql.connector.connect(user=db_user, password=db_password, host=db_host, port=db_port, database=database)
    # 创建游标对象
    cursor = cnx.cursor()

    # 查询并设置设备
    query = ('SELECT id FROM device WHERE status = 1')
    cursor.execute(query)
    result = cursor.fetchall()
    if len(result) > 0:
        device_id.clear()
        for id in result:
            device_id.append(id[0])
        print('Devices: ', device_id)

    # 查询并设置阈值
    query = ('SELECT x, y, z FROM threshold')
    cursor.execute(query)
    result = cursor.fetchall()
    if len(result) > 0:
        for (x, y, z) in result:
            threshold_x = x
            threshold_y = y
            threshold_z = z
        print('Thresholds: ', threshold_x, threshold_y, threshold_z)

    # 查询并设置邮箱列表
    query = ('SELECT email FROM user WHERE is_receiving_email = 1')
    cursor.execute(query)
    result = cursor.fetchall()
    if len(result) > 0:
        for (email,) in result:
            email_list.append(email)
    print('Email list: ', email_list)

    # 清空文件夹
    clear_dir(root_path)

    # 获取时间
    now = datetime.now()
    f_date = now.strftime("%Y-%m-%d %H:%M:%S")
    ten_minutes_ago = now - timedelta(minutes=10)
    s_date = ten_minutes_ago.strftime("%Y-%m-%d %H:%M:%S")
    # print("当前时间：", f_date)
    # print("十分钟前的时间：", s_date)

    # 创建一个session对象，它会保存所有的请求和响应，使得你可以在多个请求之间保持某些参数。
    s = requests.Session()
    # 用用户名和密码登录网站
    login_req = s.post(login_url, data=login_payload)

    # 检查是否登录成功
    if login_req.status_code == 200:
        print("Login successfully.")
    else:
        print("Login failed.")

    anomaly_data_list = []
    for id in device_id:
        download_url = 'https://diggerinspection.cn/download/DownloadFile?s_date=' + s_date + '&f_date=' + f_date + \
                       '&device=' + id + '&type=.csv&ip=diggerinspection.cn&channel=0'

        # 发送GET请求
        response = s.get(download_url, stream=True)

        # 检查请求是否成功s
        if response.status_code == 200:
            file = root_path + '/' + id + '.zip'
            # 打开一个新的文件并写入响应内容
            with open(file, 'wb') as f:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
            print("File " + id + ".zip downloaded successfully.")
            # 创建一个ZipFile对象
            with zipfile.ZipFile(file, 'r') as zip_ref:
                extracted_dir_path = root_path + '/' + id
                # 解压文件
                zip_ref.extractall(extracted_dir_path)
                if not os.path.exists(extracted_dir_path):
                    continue
                # 获取解压后的文件列表
                file_names = os.listdir(extracted_dir_path)
                for filename in file_names:
                    if filename.endswith('.csv'):
                        # 读取csv文件
                        csv_file_path = extracted_dir_path + '/' + filename
                        df = pd.read_csv(csv_file_path, encoding='utf_8_sig', header=None, names=['x', 'y', 'z', 'dummy'])
                        df = df.dropna(axis=1, how='all')
                        # print(df.head())
                        seq = 0
                        # 分组处理数据
                        group_num = math.ceil(len(df) / 60)
                        for j in range(0, len(df), group_num):
                            df_temp = df[j:j+group_num]
                            found_anomaly = False
                            # 检查是否存在超阈值数据
                            anomaly_data = None
                            max_mod = 0
                            for data in df_temp.values:
                                if abs(data[0]) > threshold_x or abs(data[1]) > threshold_y or abs(data[2]) > threshold_z:
                                    # print("Device " + id + " has exceeded the threshold.")
                                    # print("Data: ", data)
                                    anomaly_mod = mod(data[0], data[1], data[2])
                                    if anomaly_mod > max_mod:
                                        max_mod = anomaly_mod
                                        anomaly_data = {"设备ID": id, "时间段": s_date + ' ~ ' + f_date, "x": data[0], "y": data[1], "z": data[2]}
                                    found_anomaly = True
                            # 如果有超阈值数据，则保存最大值
                            if found_anomaly and anomaly_data is not None:
                                # 将异常数据添加到列表中
                                anomaly_data_list.append(anomaly_data)
                                # 保存数据到正常数据表
                                sql_normal = "INSERT INTO data (id, time, sequence, delt_x, delt_y, delt_z) VALUES (%s, %s, %s, %s, %s, %s)"
                                # 保存数据到异常数据表
                                sql_anomaly = "INSERT INTO anomaly_data (id, time, sequence, delt_x, delt_y, delt_z) VALUES (%s, %s, %s, %s, %s, %s)"
                                val = (id, f_date, seq, anomaly_data['x'], anomaly_data['y'], anomaly_data['z'])
                                cursor.execute(sql_normal, val)
                                cnx.commit()
                                cursor.execute(sql_anomaly, val)
                                cnx.commit()
                                seq += 1
                            # 如果没有超阈值数据，则保存平均值
                            else:
                                avg_x = df_temp['x'].mean()
                                avg_y = df_temp['y'].mean()
                                avg_z = df_temp['z'].mean()
                                # print("Average data: ", avg_x, avg_y, avg_z)
                                # 保存数据到数据库
                                sql = "INSERT INTO data (id, time, sequence, delt_x, delt_y, delt_z) VALUES (%s, %s, %s, %s, %s, %s)"
                                val = (id, f_date, seq, avg_x, avg_y, avg_z)
                                cursor.execute(sql, val)
                                cnx.commit()
                                seq += 1
            print("Device " + id + " data saved successfully.")
        else:
            print("File " + id + ".zip downloaded failed.")
    if len(anomaly_data_list) > 0:
        # 发送邮件，一次发送所有异常数据
        alarm(anomaly_data_list, email_list)

except Error as e:
    print("Error while connecting to MySQL:", e)

finally:
    # closing database connection.
    if cnx is not None and cnx.is_connected():
        cnx.close()
        if cursor is not None:
            cursor.close()
