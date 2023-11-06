# -*- coding: utf-8 -*-
'''
* Updated on 2023/09/23
* python3
**
* Get url of cpolar.
* features:
* - url: https://www.cpolar.com/
* - account: ****
* - password: ****
'''

from datetime import datetime
print('Started at', datetime.now())

import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import io


# =====requests===============

headers = {
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',	
	'Accept-Encoding': 'gzip, deflate',
	'Accept-Language': 'zh-CN,zh;q=0.9',
	'Cache-Control': 'max-age=0',
	'Connection': 'keep-alive',
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 YaBrowser/23.7.2.765 Yowser/2.5 Safari/537.36'
	}

url_login = 'https://dashboard.cpolar.com/login'
url_tunnels = 'https://dashboard.cpolar.com/status'

s = requests.Session()
s.headers = headers

account = os.environ['CPOLAR_ACCOUNT']
password = os.environ['CPOLAR_PASSWORD']

# ====main part=================
page = s.get(url_login)
if page.ok:
	soup = BeautifulSoup(page.content, 'html.parser')
	# token for login
	#token_element = soup.find('input')
	token_element = soup.find(id='captcha-form').find_all('input')[-1]
	token_value = token_element['value']
	#print(token_value)
	
	if token_value:
		payload = { 
			'login': account,
			'password': password,
			'csrf_token': token_value
			}
		# login
		s.post(url_login, data=payload)
		
		page_tunnels = s.get(url_tunnels)
		'''
		test = s.get(url_account)
		print(test.text)
		'''
		
		if page_tunnels.ok:
			soup = BeautifulSoup(page_tunnels.content, 'html.parser')
			'''
			# token for logout
			token_element = soup.find(id='logoutForm').find('input')
			token_value = token_element["value"]
			'''
			table = soup.find('table')			
			try:
				tunnels = pd.read_html(io.StringIO(table))[0]
				print(tunnels)
				target = tunnels[tunnels['本地地址']=='tcp://192.168.31.199:8123'].reset_index().at[0,'URL']
			except:
				print('There is something wrong. Check the Cpolar connection.')
				target = None
			
			if target != None :
				url = target.strip('tcp://')
				with open('cpolar-tunnel-url.csv', 'w') as f:
					f.write(url)
			
print('Done at', datetime.now())
