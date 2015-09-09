#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import os
import re
import requests
import json
import pprint

callbackurl = 'http://www.baidu.com'
url_klist = 'http://kk.bigk2.com:8080/KOAuthDemeter/User/getKList'
url_grlist = 'http://kk.bigk2.com:8080/KOAuthDemeter/User/getGeneralRemoteList'
url_sendgr = 'http://kk.bigk2.com:8080/KOAuthDemeter/KControl/sendGeneralRemoteOrder'
url_airlist = 'http://kk.bigk2.com:8080/KOAuthDemeter/User/getAirConditionerRemoteList'
url_sendair = 'http://kk.bigk2.com:8080/KOAuthDemeter/KControl/sendAirConditionerOrder'
url_switchk = 'http://kk.bigk2.com:8080/KOAuthDemeter/KControl/doSwitchK'
url_klight = 'http://kk.bigk2.com:8080/KOAuthDemeter/User/switchKLight'
url_kstate = 'http://kk.bigk2.com:8080/KOAuthDemeter/Kinfo/getKState'
url_kinfo = 'http://kk.bigk2.com:8080/KOAuthDemeter/User/getKInfo'

h = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.154 Safari/537.36'}


def load(filename='dat'):
    if filename in os.listdir(os.getcwd()):
        with open(filename) as f:
            return json.loads(f.read())
    return {}


def save(d, filename='dat'):
    args = load(filename)
    args.update(d)
    with open(filename, 'w') as f:
        f.write(json.dumps(args))


def update_token(p):
    s = requests.Session()  # 会话形式访问，保存cookie
    r = s.get(p['url_code'] + 'http://www.baidu.com')
    mc = re.findall(r'"mobilecode".+"(\w{16})"', r.text)[0]

    data = {
        'username': p['username'],
        'password': p['password'],
        'clientid': p['client_id'],
        'mobilecode': mc
    }
    r = s.post(p['url_code'] + 'http://www.baidu.com', data=data)
    code = r.url.split("=")[1]

    data = {
        'grant_type': 'authorization_code',
        'client_id': p['client_id'],
        'client_secret': p['client_secret'],
        'code': code,
        'redirect_uri': 'http://www.baidu.com'
    }
    r = requests.post('http://kk.bigk2.com:8080/KOAuthDemeter/accessToken', data=data)
    token = r.json()

    headers = {'Authorization': 'Bearer %s' % token['access_token']}
    r = requests.post('http://kk.bigk2.com:8080/KOAuthDemeter/UserInfo', headers=headers)
    userinfo = r.json()

    return dict(mobilecode=mc, code=code, access_token=token['access_token'], refresh_token=token['refresh_token'],
                userid=userinfo['userid'])


# save(update_token(load()))
P = load()

hds = {
    'Authorization': 'Bearer %s' % P['access_token'],
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'Accept-Encoding': 'identity'
}
dat = {
    'userid': P['userid']
}
req = requests.post(url_grlist, headers=hds, data=json.dumps(dat))
if req.status_code == 200:
    rst = req.json()
    if rst['result'] == 0:
        pprint.pprint(req.json())
    else:
        save(update_token(load()))
        P = load()
print req.content.decode('utf-8')  # , '\n', req.url, '\n', req.status_code, '\n', req.history, '\n', req.json()
