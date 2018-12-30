from login import InstagramBot
import json

username = '<your_username>'
password = '<your_password>'

user = InstagramBot(username, password)
user.login()
user_json_info, id = user.get_user_info('apple')
data_list = user.extract_user_info(user_json_info)
header_list = ['title', 'photo_url', 'num_like', 'num_comment', 'create_time']
user.data_to_csv(header_list, data_list, 'ig_apple_data')


