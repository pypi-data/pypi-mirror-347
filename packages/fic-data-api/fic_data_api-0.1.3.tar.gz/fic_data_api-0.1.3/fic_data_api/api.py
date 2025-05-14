"""
 * @Author：cyg
 * @Package：api
 * @Project：Default (Template) Project
 * @name：api
 * @Date：2025/5/8 09:52
 * @Filename：api
"""

import requests


class FicDataApi:
	def __init__(self, token):
		self.api_url = "http://10.8.23.90:5001"
		self.token = token
	
	def get_data(self, dataName, where=""):
		if not self.token:
			raise ValueError("Token has not been set")
		
		url = f"{self.api_url}/data/get_data"
		headers = {"token": f"{self.token}"}
		params = {"dataName": dataName, "where": where}
		response = requests.get(url, headers=headers, params=params)
		
		if response.status_code == 200:
			return response.json()
		else:
			print(f"Failed : {response.status_code}")
			return None
