import os
import time
import json

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

toaster = None
if os.name == 'nt':
	try:
		from win10toast import ToastNotifier
		toaster = ToastNotifier()
	except:
		print(' ! If you are running on windows and want fancy notifications, please pip install win10toast')

class Driver:
	def obj_init(self):
		if self.obj:
			self.obj.quit()
			self.obj = None

		options = Options()
		# options.add_argument("--headless")
		executable = None	
		if os.name == 'nt':
			executable = 'chromedriver.exe'
		else:
			executable = 'chromedriver'
		path = f"{os.getcwd()}/drivers/{executable}"

		self.obj = webdriver.Chrome(options=options, executable_path=path)

	def get_soup(self):
		self.obj.get(self.url)
		html = self.obj.page_source.encode('utf-8').strip()
		return BeautifulSoup(html, 'lxml')

	def __init__(self):
		self.url = None
		self.obj = None
		self.obj_init()


def parse(from_page,to_page):
	res = []
	base_url = "http://free-proxy.cz/en/proxylist/main/"
	driver = Driver()

	for i in range(from_page, to_page + 1):
		driver.url = base_url + str(i)
		soup = driver.get_soup()
		tbody = soup.select_one('table#proxy_list > tbody')

		if not tbody:
			proxy_out(res)

			print(' ! ' + str(time.time()) + ' - Капча!!!')
			if toaster:
				toaster.show_toast("Free proxy parser","Капча. Капча. Блять", duration=10)

			WebDriverWait(driver.obj, 100000).until(EC.visibility_of_element_located((By.ID, "proxy_list")))

			soup = driver.get_soup()
			tbody = soup.select_one('table#proxy_list > tbody')

		rows = tbody.find_all('tr')
		for row in rows:
			td = row.find_all('td')
			if len(td) == 1:
				continue

			td[0].select('script')[0].extract()
			texts = list(map(lambda x: x.getText(), td))

			res.append({'ip': texts[0],
						'port': int(texts[1]),
						'protocol': texts[2] ,
						'speed': int(texts[7].replace(' ','').replace('kB/s','')),
						'response': int(texts[9].replace(' ','').replace('ms',''))})
	driver.obj.quit()
	proxy_out(res)

def proxy_out(res):
	f = open("parsed.json", "w")
	json.dump(res, f, sort_keys=True, indent=4)
	f.close()
