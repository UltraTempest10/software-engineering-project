import os
import shutil

from datetime import datetime, timedelta
import requests
import zipfile
import pandas as pd

import mysql.connector
from mysql.connector import Error

# 文件夹路径
root_path = 'E:/test'

# 登录信息
login_url = 'https://diggerinspection.cn/doLogin'
login_payload = {
    'username': 'lu',
    'password': 'tj221204'
}

# 数据库连接信息
db_user = 'root'
db_password = 'root'
db_host = '47.102.210.25'
db_port = 3306
database = 'curtain_wall'

# 设备名称
device_id = ['4787BE3A', '8850A7D7', '7749E4D9', 'E884C99D', 'E43AC643', '29FA1867', '350E6EFF', 'F853ED49', 'A77C5238']
# 失效设备: '7A6BA8C8', '3326F78D'

# 每组数据个数
group_num = 500
# 阈值
threshold_x_y = 1.6
threshold_z = 2.4

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

cnx = None
cursor = None

try:
    # 连接MySQL数据库
    cnx = mysql.connector.connect(user=db_user, password=db_password, host=db_host, port=db_port, database=database)
    # 创建游标对象
    cursor = cnx.cursor()

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
                        for j in range(0, len(df), group_num):
                            df_temp = df[j:j+group_num]
                            has_inserted = False
                            # 检查是否存在超阈值数据
                            for data in df_temp.values:
                                if abs(data[0]) > threshold_x_y or abs(data[1]) > threshold_x_y or abs(data[2]) > threshold_z:
                                    print("Device " + id + " has exceeded the threshold.")
                                    print("Data: ", data)
                                    # 保存数据到数据库
                                    sql = "INSERT INTO data (id, time, sequence, delt_x, delt_y, delt_z) VALUES (%s, %s, %s, %s, %s, %s)"
                                    val = (id, f_date, seq, data[0], data[1], data[2])
                                    cursor.execute(sql, val)
                                    cnx.commit()
                                    seq += 1
                                    has_inserted = True
                            # 如果没有超阈值数据，则保存平均值
                            if not has_inserted:
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

except Error as e:
    print("Error while connecting to MySQL:", e)

finally:
    # closing database connection.
    if cnx is not None and cnx.is_connected():
        cnx.close()
        if cursor is not None:
            cursor.close()
