
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import random
from fake_useragent import UserAgent
import requests
import json
import re
import pandas as pd
from datetime import datetime


class InstagramBot:
#a instagram bot that allow you to login in and extract data from the page

	# define the url for login in and log out
	url = 'https://www.instagram.com/'
	url_login = 'https://www.instagram.com/accounts/login/ajax/'
	url_logout = 'https://www.instagram.com/accounts/logout/'
	url_user_info = "https://www.instagram.com/{}/"

	user_agent = "" ""
	accept_language = 'en-US,en;q=0.5'

	# information required for login
	def __init__(self, login, password):
		self.useragent = UserAgent()
		self.s = requests.Session()
		self.user_login = login.lower()
		self.user_password = password
		self.login_status = False
		self.test_content = ''

	def login(self):
		'''
		function to login user
		input: self -> username, password
		output: user.updated.headers and session that can be used to get/ post info

		'''
		print("Starting logging in instragram!")
		
		self.login_post = {
			'username' : self.user_login,
			'password' : self.user_password,
		}

		self.s.headers.update({
            'Accept': '*/*',
            'Accept-Language': self.accept_language,
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Content-Length': '0',
            'Host': 'www.instagram.com',
            'Origin': 'https://www.instagram.com',
            'Referer': 'https://www.instagram.com/',
            'User-Agent': self.user_agent,
            'X-Instagram-AJAX': '1',
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-Requested-With': 'XMLHttpRequest'
        })

		r = self.s.get(self.url)
		self.s.headers.update({'X-CSRFToken': r.cookies['csrftoken']})
		time.sleep(5 * random.random())
		
		login = self.s.post(self.url_login, data = self.login_post, allow_redirects = True)
		self.s.headers.update({'X-CSRFToken': login.cookies['csrftoken']})
		self.csrftoken = login.cookies['csrftoken']
		self.s.cookies['ig_vw'] = '1536'
		self.s.cookies['ig_pr'] = '1.25'
		self.s.cookies['ig_vh'] = '772'
		self.s.cookies['ig_or'] = 'landscape-primary'
		time.sleep(5 * random.random())

		if login.status_code == 200:
			r = self.s.get('https://www.instagram.com/')
			finder = r.text.find(self.user_login)
			# if can find username in page (i.e. finder!=-1), it means successfully login
			if finder != 1:
				self.login_status = True
				print('successful login!')
			else:
				print("Check your data. Wrong in login data!")
		else:
			print('Connection error in login!')


	def get_user_info(self, username):
		'''
		function to extract user information 
		input: username
		output: json_info from ig and user_id
		'''
		time.sleep(2 * random.random())
		url_info = self.url_user_info.format(username)
		info = self.s.get(url_info)
		json_info = json.loads(re.search('window._sharedData = (.*?);</script>', info.text, re.DOTALL).group(1))
		self.test_content = json_info
		id_user = json_info['entry_data']['ProfilePage'][0]['graphql']['user']['id']
		return json_info, id_user

	@staticmethod
	def extract_user_info(user_info):
		'''
		function to slice user json data info useful data
		input: user json data (as generated from get_user_info)
		output: list of item in the following format (title, photo_url, num_like, num_comment, create_time)
		'''
		result_list = []
		info = user_info['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media']['edges']
		for n, item in enumerate(info):
			title = item['node']['edge_media_to_caption']['edges'][0]['node']['text']
			photo_url = item['node']['display_url']
			num_like = item['node']['edge_liked_by']['count']
			num_comment = item['node']['edge_media_to_comment']['count']
			create_time = item['node']['taken_at_timestamp']
			create_time = datetime.fromtimestamp(create_time).strftime("%A, %B %d, %Y %I:%M:%S")
			result_list.append((title, photo_url, num_like, num_comment, create_time))
		return result_list


	@staticmethod
	def data_to_csv(header_list, data_list, csv_file_name):
		'''
		function to use pandas module to turn list of data to dataframe and csv
		input: list of header, list of data_list in tuple and csv filename
		output: a csv file storing the data

		Caution: length of each tuple in header_list and data_list should be the same
		'''
		df = pd.DataFrame(data_list, columns = header_list)
		df.to_csv(csv_file_name + '.csv')






