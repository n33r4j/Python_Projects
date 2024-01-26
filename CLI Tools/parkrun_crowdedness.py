# Parkrun Crowdedness Sydney
# [!] Click on a line plot to highlight it

import requests
# from bs4 import BeautifulSoup
import pandas as pd
from io import StringIO
import matplotlib.pyplot as plt
import datetime as dt
from mplcursors import cursor


url_prefix = 'https://www.parkrun.com.au/'
url_suffix = '/results/eventhistory/'

parkruns = ['northsydney',
			'centennial',
			'stpeters',
			'dollspoint',
			'rhodes',
			'kamay',
			'wentworthcommon',
			'cooksriver',
			'greenway',
			'willoughby',
			'parramatta',
			'panania',
			'chippingnorton',
			'casula',
			'menai',
			'cronulla',
			'rootyhill',
			'mosman',
			'curlcurl',
			'wildflower',
			'theponds',
			'rousehill',
]

parkrun_data = {}
fig, ax = plt.subplots()
start_point = 40 # Only plots last 40

def on_hover_highlight(event):
	# print('Other event')
	if event.name == 'pick_event':
		line = event.artist
		w = line.get_linewidth()
		if w > 1:
			line.set_linewidth(1)
		else:
			line.set_linewidth(3)
		fig.canvas.draw()
		# print("Pick event")

# debug_counter = 0

for p in parkruns:
	# response = requests.get(url_prefix + p + url_suffix)

	# if response.status_code != 200:
		# print("Error fetching page")
		# exit()
	# else:
		# content = response.content
	
	# We need this since it gives us a 403 Error otherwise
	header = {
		"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
	  "X-Requested-With": "XMLHttpRequest"
	} # How does this even work?
	
	page_url = url_prefix + p + url_suffix
	# print(page_url)
	r = requests.get(page_url, headers=header)
	page_table = pd.read_html(StringIO(str(r.text)))
	# print(list(page_table[0].columns.values))
	# print(type(page_table[0]))
	# print(page_table[0].shape)
	# print(list(page_table[0]['Date']))
	try:
		finishers_history = [int(fin.split('f')[0]) for fin in list(page_table[0]['Date/First Finishers'])]
		dates = [dt.datetime.strptime(d[:10], '%d/%m/%Y').date() for d in list(page_table[0]['Date'])]
		# for i in range(len(finishers_history)):
			# print(dates[i], finishers_history[i])
	
		parkrun_data[p] = [dates, finishers_history]
		print(f'{p:<20} done {"[O]":>4}')
		x = parkrun_data[p][0]
		y = parkrun_data[p][1]
		# Reverse the order
		x = x[len(x)-1::-1]
		y = y[len(y)-1::-1]
		# Take only last few start_point
		x = x[-start_point:]
		y = y[-start_point:]
		# print(len(x),len(y))
		
		ax.plot(x, y, marker='.', lw=1, label=p, picker=True)
		d = ([0]*len(y))[-start_point:]
		# ax.fill_between(x, y, where=y>=d, interpolate=True, color='blue')

		# if debug_counter > 1:
			# break
		# else:
			# debug_counter += 1
		
	except KeyError:
		print(f'{p:<17} skipped {"[X]":>4}')
		continue

fig.canvas.mpl_connect('pick_event', on_hover_highlight)
cursor(hover=True) # For annotations when hovering
plt.legend(loc="upper right")
plt.legend().set_draggable(True)
plt.title("Sydney Parkrun Crowdedness")
plt.xlabel("Date")
plt.ylabel("No. of Finishers")
plt.show()
