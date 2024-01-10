# mail.py: 用于发送邮件

# from flask import Flask, jsonify, request, redirect, render_template
# from flask_httpauth import HTTPBasicAuth
import pandas as pd
# import json
import smtplib
# from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


# 设置服务器所需信息
# QQ邮箱服务器地址
mail_host = 'smtp.qq.com'  
# 邮件发送方邮箱地址
mail_user = 'curtain.wall@foxmail.com'  
# 密码(部分邮箱为授权码)
mail_pass = 'xvmuzktebjsgiedb'   
# 邮件接受方邮箱地址，注意需要[]包裹，这意味着你可以写多个邮件地址群发
# receivers = ['1160414948@qq.com']

# app = Flask(__name__, static_url_path="")
# auth = HTTPBasicAuth()

# @app.route("/alarm", methods=['GET', 'POST'])
def alarm(data, receivers):
    # 获取传感器数据
    # data = request.get_json().get('data', [])
    # 创建一个DataFrame，其中包含获取到的传感器数据
    df = pd.DataFrame(data)
    # df = pd.DataFrame(data, index=[0])
    # 修改索引，使其从1开始
    df.index = df.index + 1
    # 将DataFrame转换为HTML表格
    html_table = df.to_html()
    # html_table = df.to_html(index=False)
    text1 = '安全监控中心的自动报警系统在监测玻璃幕墙的振动传感器数据时，发现部分传感器的数据超过了设定的上下限。这可能意味着玻璃幕墙存在裂缝或松动等安全隐患，请及时检查并处理。'
    text2 = '以下是超过上下限的传感器的编号和数据，请在收到本邮件后，尽快安排人员对相关位置进行检查，并上报检查结果和处理措施。如果有任何疑问或需要协助，请联系安全监控中心。'
    # 将文本和HTML表格组合在一起
    html = f"""
    <html>
    <body>
    <p>{text1}</p>
    <p>{text2}</p>
    {html_table}
    </body>
    </html>
    """

    # 纯文本格式的传感器数据表格
    # sensor_list = []
    # for item in data:
    #     sensor_list.append(str(item['id']) + '  ' + str(item['time']) + '  ' + str(item['x']) + '  ' + str(item['y']) + '  ' + str(item['z']) + '\n')
    # sensor_info = ''
    # for item in sensor_list:
    #     sensor_info += item
    # 纯文本邮件内容设置
    # content = '安全监控中心的自动报警系统在监测玻璃幕墙的振动传感器数据时，发现部分传感器的数据超过了设定的上下限。这可能意味着玻璃幕墙存在裂缝或松动等安全隐患，请及时检查并处理。\n' \
    #           '以下是超过上下限的传感器的编号和数据：\n\n传感器编号  采样时间  x轴(毫米)  y轴(毫米)  z轴(毫米)\n' + sensor_info + \
    #           '\n请在收到本邮件后，尽快安排人员对相关位置进行检查，并上报检查结果和处理措施。如果有任何疑问或需要协助，请联系安全监控中心。'

    # 设置email信息
    message = MIMEText(html, 'html', 'utf-8')
    # 邮件主题
    message['Subject'] = '警告' 
    # 发送方信息
    message['From'] = mail_user

    for receiver in receivers:
        # 接受方信息
        message['To'] = receiver
        # 登录并发送邮件
        try:
            smtp_obj = smtplib.SMTP_SSL(mail_host, 465)
            # 登录到服务器
            smtp_obj.login(mail_user, mail_pass)
            # 发送
            smtp_obj.sendmail(mail_user, receiver, message.as_string())
            # 退出
            smtp_obj.quit()
            print('Successfully sent email.')
            # return "success"
        except smtplib.SMTPException as e:
            print('error', e)
            # return "error"
