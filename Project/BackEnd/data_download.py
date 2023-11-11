import requests
import zipfile
import os
import shutil
from datetime import datetime, timedelta

# 文件夹路径
root = 'E:/test'

# 清空文件夹
for filename in os.listdir(root):
    # 构造文件或文件夹的绝对路径
    file_path = os.path.join(root, filename)
    try:
        # 如果是文件，则删除
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        # 如果是文件夹，则删除整个文件夹
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
    except Exception as e:
        print('Failed to delete %s. Reason: %s' % (file_path, e))

# 获取当前时间
now = datetime.now()

# 格式化当前时间
f_date = now.strftime("%Y-%m-%d %H:%M:%S")

# 获取十分钟前的时间
ten_minutes_ago = now - timedelta(minutes=10)

# 格式化十分钟前的时间
s_date = ten_minutes_ago.strftime("%Y-%m-%d %H:%M:%S")

# print("当前时间：", f_date)
# print("十分钟前的时间：", s_date)

# 设备名称
device_name = ['4787BE3A', '8850A7D7', '7A6BA8C8', '7749E4D9', 'E884C99D', 'E43AC643', '29FA1867', '350E6EFF', '3326F78D', 'F853ED49', 'A77C5238']

# 创建一个session对象，它会保存所有的请求和响应，使得你可以在多个请求之间保持某些参数。
s = requests.Session()

# 用用户名和密码登录
login_url = 'https://diggerinspection.cn/doLogin'
login_payload = {
    'username': 'lu',
    'password': 'tj221204'
}
login_req = s.post(login_url, data=login_payload)

# 检查是否登录成功
if login_req.status_code == 200:
    print("登录成功！")
else:
    print("登录失败。")

for i in range(len(device_name)):
    download_url = 'https://diggerinspection.cn/download/DownloadFile?s_date='+s_date+'&f_date='+f_date+'&device='+device_name[i]+'&type=.csv&ip=diggerinspection.cn&channel=0'

    # 发送GET请求
    response = s.get(download_url, stream=True)

    # 检查请求是否成功s
    if response.status_code == 200:
        file = 'E:/test/'+device_name[i]+'.zip'
        # 打开一个新的文件并写入响应内容
        with open(file, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
        print("文件"+str(i+1)+"下载成功！")
        # 创建一个ZipFile对象
        with zipfile.ZipFile(file, 'r') as zip_ref:
            # 解压文件
            zip_ref.extractall(root)
    else:
        print("文件"+str(i+1)+"下载失败。")
