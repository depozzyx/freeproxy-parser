# import importlib

# from config import *
# import free_proxy_parser
# import proxies_out_unsorted

# pip install win10toast
# pip install selenium
# pip install beautifulsoup4
import json
def sort_proxies_by_criteria(criteria_dict, ip_and_port_to_array_mode = False):
	f = open("parsed.json", "r")
	unsorted = json.loads(f.read())
	f.close()
	# unsorted = proxies_out_unsorted.proxies
	res = []

	for obj in unsorted:
		is_ok = True
		for key in criteria_dict.keys():
			z = str(criteria_dict[key])[0]
			if z in ['>', '<']:
				if isinstance(obj[key], int):
					n = int(str(criteria_dict[key])[1:])
					if z == '>':
						if not (obj[key] > n):
							is_ok = False
					elif z == '<':
						if not (obj[key] < n):
							is_ok = False
				else:
					is_ok = False
			else:
				if obj[key] != criteria_dict[key]:
					is_ok = False

			if not is_ok:
				break

		if is_ok:
			if ip_and_port_to_array_mode:
				res.append(obj['ip']+':'+str(obj['port']))
			else:
				res.append(obj)

	proxy_out(res)

	return 1

def proxy_out(res):
	import json
	
	f = open("sorted.json", "w")
	json.dump(res, f, sort_keys=True, indent=4)
	f.close()

# free_proxy_parser.parse(1, 3)
## от x до y страницы free-proxy.cz, которые нужно спарсить
## тут x = 1; y = 10;

sort_proxies_by_criteria({'protocol':'SOCKS5'}, ip_and_port_to_array_mode = True)
## только protocol SOCKS5
## ip_and_port_to_array_mode = True значит, что в proxies_out.py будет выведен только массив в формате ['ip:port', ... ]

# sort_proxies_by_criteria({'response':'<100'}, ip_and_port_to_array_mode = False)
## ">100" значит, что значение должно быть int который больше 100
## ">" и "<"- единственные знак, которые поддерживаются(Еще есть == если значение записать в конкретном int). Зачем что-то еще?
