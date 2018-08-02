import json
import requests
from termcolor import colored


def init(domain):
	CRT = []

	print colored("[*]-Searching CRT...", 'yellow')

	parameters = {'q': '%.{}'.format(domain), 'output': 'json'}
	headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:52.0) Gecko/20100101 Firefox/52.0', 'content-type': 'application/json'}

	try:
		response = requests.get("https://crt.sh/?", params=parameters, headers=headers)

		if response.status_code == 200:
			content = response.content.decode('utf-8')
			data = json.loads("[{}]".format(content.replace('}{', '},{')))

			for d in data:
				if not ''.join(d['name_value']).startswith('*'):
					CRT.append(d['name_value'])

		CRT = set(CRT)

		print "  \__", colored("Unique subdomains found:", 'cyan'), colored(len(CRT), 'yellow')
		return CRT

	except requests.exceptions.RequestException as err:
		print "  \__", colored(err, 'red')
		return []

	except requests.exceptions.HTTPError as errh:
		print "  \__", colored(errh, 'red')
		return []

	except requests.exceptions.ConnectionError as errc:
		print "  \__", colored(errc, 'red')
		return []

	except requests.exceptions.Timeout as errt:
		print "  \__", colored(errt, 'red')
		return []
