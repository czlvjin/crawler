#!/usr/bin/env python3

from lxml import html
import json
import os
import pickle
import requests
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import sys

global driver


# 以一组医生的 doctor_id 拉取有号的排班信息 list
# 一个上午/一个下午 为一个排班周期
def schedule_list(doctor_ids):
    if len(doctor_ids) <= 0:
        return []
    doctor_ids = list(map(str, doctor_ids))

    url = 'https://wap.91160.com/doctor/schedule.html?unit_id=21&doctor_ids=' + ','.join(doctor_ids)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
        'Referer': url,
        'X-Requested-With': 'XMLHttpRequest'
    }
    rsp = requests.get(url = url, headers = headers)
    content = rsp.content
    ret = json.loads(content)
    # print(ret)
    schedules = []
    if type(ret['sch']) == type({}):
        for k, unit in ret['sch'].items():
            for k, doctor in unit.items():
                for k, unit in doctor.items():
                    for k, date in unit.items():
                        for k, halfday in date['sch'].items():
                            print(halfday['doctor_id'] + ': ' + halfday['to_date'] + ' ' + k + ' (' + halfday['left_num'] + ')')
                            if int(halfday['left_num']) > 0:
                                schedules.append(halfday)
    return schedules

    # ret = {'sch': {'21': {'681_14666': {'22': {'2018-05-28': {'week_num': '1', 'week': '周一', 'day': '2018-05-28', 'sch': {'am': {'unit_id': '21', 'dep_id': '681', 'to_date': '2018-05-28', 'time_type': 'am', 'doctor_id': '14666', 'level_code': '190', 'level_name': '普通', 'y_state': '1', 'schedule_id': '9a449ab1340321e633478cd6fd94f8fe', 'guahao_amt': '25.0', 'yuyue_max': '24', 'yuyue_num': '8', 'left_num': '16', 'y_state_desc': '可预约', 'schext_clinic_label': ''}, 'pm': {'unit_id': '21', 'dep_id': '681', 'to_date': '2018-05-28', 'time_type': 'pm', 'doctor_id': '14666', 'level_code': '190', 'level_name': '普通', 'y_state': '1', 'schedule_id': '9ae201740311963e48244b3ecf85fb08', 'guahao_amt': '25.0', 'yuyue_max': '13', 'yuyue_num': '5', 'left_num': '8', 'y_state_desc': '可预约', 'schext_clinic_label': ''}}}, '2018-05-29': {'week_num': '2', 'week': '周二', 'day': '2018-05-29', 'sch': {'am': {'unit_id': '21', 'dep_id': '681', 'to_date': '2018-05-29', 'time_type': 'am', 'doctor_id': '14666', 'level_code': '190', 'level_name': '普通', 'y_state': '1', 'schedule_id': '9a411d40381c63649f57636826a6c9d7', 'guahao_amt': '25.0', 'yuyue_max': '24', 'yuyue_num': '1', 'left_num': '23', 'y_state_desc': '可预约', 'schext_clinic_label': ''}}}, '2018-05-30': {'week_num': '3', 'week': '周三', 'day': '2018-05-30', 'sch': {'pm': {'unit_id': '21', 'dep_id': '681', 'to_date': '2018-05-30', 'time_type': 'pm', 'doctor_id': '14666', 'level_code': '190', 'level_name': '普通', 'y_state': '1', 'schedule_id': '9a75b8e51140371c6305e02360afdd95', 'guahao_amt': '25.0', 'yuyue_max': '13', 'yuyue_num': '1', 'left_num': '12', 'y_state_desc': '可预约', 'schext_clinic_label': ''}}}, '2018-05-31': {'week_num': '4', 'week': '周四', 'day': '2018-05-31', 'sch': {'am': {'unit_id': '21', 'dep_id': '681', 'to_date': '2018-05-31', 'time_type': 'am', 'doctor_id': '14666', 'level_code': '190', 'level_name': '普通', 'y_state': '1', 'schedule_id': '9a66c213a1c40371a63b5a1ac46faa3f', 'guahao_amt': '25.0', 'yuyue_max': '24', 'yuyue_num': '0', 'left_num': '24', 'y_state_desc': '可预约', 'schext_clinic_label': ''}, 'pm': {'unit_id': '21', 'dep_id': '681', 'to_date': '2018-05-31', 'time_type': 'pm', 'doctor_id': '14666', 'level_code': '190', 'level_name': '普通', 'y_state': '1', 'schedule_id': '9a05063910403e1c6375422b0e26a141', 'guahao_amt': '25.0', 'yuyue_max': '13', 'yuyue_num': '0', 'left_num': '13', 'y_state_desc': '可预约', 'schext_clinic_label': ''}}}, '2018-06-01': {'week_num': '5', 'week': '周五', 'day': '2018-06-01', 'sch': {'pm': {'unit_id': '21', 'dep_id': '681', 'to_date': '2018-06-01', 'time_type': 'pm', 'doctor_id': '14666', 'level_code': '190', 'level_name': '普通', 'y_state': '1', 'schedule_id': '9ab31915403f12632573b9baf76db936', 'guahao_amt': '25.0', 'yuyue_max': '13', 'yuyue_num': '2', 'left_num': '11', 'y_state_desc': '可预约', 'schext_clinic_label': ''}}}}}}}, 'foreshow': {'21': {'681': '06月02日号源在今日15:00放出'}}, 'noSchRedirect': {'21': {'681_14666': {'no_sch': 1, 'refeInfo': {'refe_doctor': '14666', 'refe_dep': 681, 'refe_unit': 21, 'is_redirect': 1}}}}, 'hasNightSch': {'21': 0}}


# 使用 schedule_list() 拉取的排班 dict 拼到下单的 url
# 一个排班周期对应不同时间段, 只取其中一个时间段
def detl_url(schedule):
    url = 'https://wap.91160.com/doctor/detlnew.html?unit_detl_map=[{%22unit_id%22:' + str(schedule['unit_id']) + ',%22doctor_id%22:%22' + str(schedule['doctor_id']) + '%22,%22dep_id%22:' + str(schedule['dep_id']) + ',%22schedule_id%22:%22' + str(schedule['schedule_id']) + '%22}]'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
        'Referer': url,
        'X-Requested-With': 'XMLHttpRequest'
    }
    rsp = requests.get(url = url, headers = headers)
    content = rsp.content
    ret = json.loads(content)
    # print(ret)
    max_stock = 0
    best_detl_id = ''
    for k, schedules in ret['data'].items():
        for sch in schedules:
            # 这个逻辑是取一个剩余号数最大的时间段, 增加预约成功的概率
            stock = int(sch['yuyue_max']) - sch['yuyue_num']
            if stock > max_stock:
                max_stock = stock
                best_detl_id = sch['detl_id']
    if best_detl_id != '':
        return 'https://wap.91160.com/order/confirm.html?unit_id=' + str(schedule['unit_id']) + '&sch_id=' + str(schedule['schedule_id']) + '&dep_id=' + str(schedule['dep_id']) + '&detl_id=' + best_detl_id
    return ''

    # ret = {'status': 1, 'msg': '', 'data': {'9a6655fc1144037116384705536b4347': [{'detl_id': '42ac8fedc2dbs2rc4:21d:681d:164666:201a8-6058-e28:acm8:08:00:08:340', 'schedule_id': '9a6655fc1144037116384705536b4347', 'begin_time': '08:00', 'end_time': '08:30', 'yuyue_max': '4', 'yuyue_num': 1, 'guahao_max': '4', 'guahao_num': 0, 'state': None, 'remark': '', 'detl_time_desc': '08:00-08:30'}, {'detl_id': '42a93d1s5rc1:21b:681a:174666:20118-a05d-728:admf:08:350:09f:00', 'schedule_id': '9a6655fc1144037116384705536b4347', 'begin_time': '08:30', 'end_time': '09:00', 'yuyue_max': '5', 'yuyue_num': 1, 'guahao_max': '5', 'guahao_num': 0, 'state': None, 'remark': '', 'detl_time_desc': '08:30-09:00'}, {'detl_id': '42ae5213fs7rc1:21c:681c:134666:201f8-3057-128:aem7:09e:00:09f:3e0', 'schedule_id': '9a6655fc1144037116384705536b4347', 'begin_time': '09:00', 'end_time': '09:30', 'yuyue_max': '4', 'yuyue_num': 1, 'guahao_max': '4', 'guahao_num': 0, 'state': None, 'remark': '', 'detl_time_desc': '09:00-09:30'}, {'detl_id': '42a0516afs1rcd:212:681f:164666:20128-6056-628:a5me:090:360:170:00', 'schedule_id': '9a6655fc1144037116384705536b4347', 'begin_time': '09:30', 'end_time': '10:00', 'yuyue_max': '4', 'yuyue_num': 3, 'guahao_max': '4', 'guahao_num': 0, 'state': None, 'remark': '', 'detl_time_desc': '09:30-10:00'}, {'detl_id': '42a36596c1s3rc8:213:681e:124666:201f8-6052-528:aam1:110:00:160:320', 'schedule_id': '9a6655fc1144037116384705536b4347', 'begin_time': '10:00', 'end_time': '10:30', 'yuyue_max': '4', 'yuyue_num': 1, 'guahao_max': '4', 'guahao_num': 0, 'state': None, 'remark': '', 'detl_time_desc': '10:00-10:30'}, {'detl_id': '42a970ae661sdrc8:21f:6817:1a4666:20198-f05b-928:a6m0:100:3f0:1d16:00', 'schedule_id': '9a6655fc1144037116384705536b4347', 'begin_time': '10:30', 'end_time': '11:00', 'yuyue_max': '3', 'yuyue_num': 1, 'guahao_max': '3', 'guahao_num': 0, 'state': None, 'remark': '', 'detl_time_desc': '10:30-11:00'}]}}


# 调用浏览器打开下单页面, 20s 后退出程序
def order(url):
    global driver
    driver.get(url)
    if os.path.exists('cookies.pkl'):
        for cookie in pickle.load(open("cookies.pkl", "rb")):
            driver.add_cookie(cookie)
    driver.get(url)
    time.sleep(20)
    pickle.dump(driver.get_cookies(), open("cookies.pkl", "wb"))
    driver.quit()
    exit()


# 给 MacOS 推送一条消息通知, 需要系统安装 terminal-notifier 支持
# Refer: http://codewenda.com/python%E5%8F%91%E5%B8%83osx%E9%80%9A%E7%9F%A5/
def notify(title, subtitle, message):
    t = '-title {!r}'.format(title)
    s = '-subtitle {!r}'.format(subtitle)
    m = '-message {!r}'.format(message)
    os.system('terminal-notifier {}'.format(' '.join([m, t, s])))


if __name__ == "__main__":
    # 为了减少刷到号的等待时间, 脚本执行时就先加载浏览器
    print('\x1b[32;m%s\x1b[0m' % 'Initializing browser... ')
    global driver
    driver = webdriver.Chrome('chromedriver')
    print('')

    if len(sys.argv) > 1 and sys.argv[1] == 'login':
        print('\x1b[32;m%s\x1b[0m' % ('Make sure your account has been signed in in 20s...'))
        order('https://wap.91160.com/account/index.html')

    doctor_ids = [\
        1926,  # sample doctor id
    ]

    while (1):
        print('\x1b[32;m%s\x1b[0m' % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        sch_list = schedule_list(doctor_ids)

        if len(sch_list) > 0:
            detl = detl_url(sch_list[0])
            notify(title    = 'Order is preparing...',
                   subtitle = 'Python Crawler',
                   message  = 'At least one valid option was found.')
            print('\x1b[32;m%s\x1b[0m' % 'Available schedule detected. Enter captcha in the browser...')
            order(detl)
            break
        else:
            print("no valid option")
            time.sleep(0.5)

        print("")

# logout: https://wap.91160.com/account/logout.html
