# Get the current UV index in Sydney
# https://www.arpansa.gov.au/our-services/monitoring/ultraviolet-radiation-monitoring/ultraviolet-radation-data-information

from urllib.request import urlopen
import xmltodict

def display_info(text):
	print("="*len(text))
	print(text)
	print("="*len(text))


file = urlopen('https://uvdata.arpansa.gov.au/xml/uvvalues.xml')
data = file.read()
file.close()

data = xmltodict.parse(data)

cities_data = data['stations']['location']
for city in cities_data:
	if city['@id'].startswith('Syd'):
		if city['status'] == 'ok':
			display_text = f"Current UV Index at {city['@id']}: {city['index']} | {city['date']}, {city['time']}"
		else:
			display_text = f"Current UV Index at {city['@id']}: not available."

		display_info(display_text)
		break

