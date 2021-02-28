import json

def sort_proxies_by_criteria(criteria_dict, ip_and_port_to_array_mode = False):
	f = open("parsed.json", "r")
	unsorted = json.loads(f.read())
	f.close()
	
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
	f = open("sorted.json", "w")
	json.dump(res, f, sort_keys=True, indent=4)
	f.close()
