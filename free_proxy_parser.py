from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

import os
import time

toaster = None
if os.name == 'nt':
	from win10toast import ToastNotifier
	toaster = ToastNotifier()

def parse(from_page,to_page):
	res = []
	url = "http://free-proxy.cz/en/proxylist/main/"
	# Chromedriver
	options = Options()
	# options.add_argument("--headless")
	path = os.getcwd()
	extra = ''
	if os.name == 'nt':
		extra = '.exe'

	driver = webdriver.Chrome(options=options, executable_path=path+'/drivers/chromedriver'+extra)

	for i in range(from_page,to_page+1):
		driver.get(url+str(i))
		html = driver.page_source.encode('utf-8').strip()
		# html = get_selenium_page(url+str(i))
		# output(str(html))

		soup = BeautifulSoup(html, 'lxml')
		d1 = soup.find_all('tbody')
		if len(d1) == 0:
			proxy_out(res)

			print(' ! ' + str(time.time()) + ' - Капча!!!')

			if toaster:
				toaster.show_toast("Free proxy parser","Капча. Капча. Блять", duration=10)

			element = WebDriverWait(driver, 10000).until(EC.visibility_of_element_located((By.ID, "proxy_list")))
			html = driver.page_source.encode('utf-8').strip()
			soup = BeautifulSoup(html, 'lxml')
			d1 = soup.find_all('tbody')

		head = d1[1].find_all('tr')



		for obj in head:
			td = obj.find_all('td')
			td[0].select('script')[0].extract()
			td[0] = td[0].getText()
			if len(td) == 1:
				continue
			res.append({'ip': td[0],
						'port': int(td[1].getText()),
						'protocol': td[2].getText() ,
						'speed': int(td[7].getText().replace(' ','').replace('kB/s','')),
						'response': int(td[9].getText().replace(' ','').replace('ms',''))})
	proxy_out(res)
	return res

def proxy_out(res):
	import json

	f = open("parsed.json", "w")
	json.dump(res, f, sort_keys=True, indent=4)
	f.close()
# print(proxy_parse(1,2))
