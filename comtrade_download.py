import pandas as pd
import os
import json
from urllib.request import urlopen
import time
import csv

print(os.getcwd())
os.chdir('.')  # set your current directory

# create a directory where to save downloaded data
if not os.path.exists('data'):
    os.makedirs('data')

# ************************************************************************
# Obtain Comtrade country codes
# ************************************************************************
url = urlopen('http://comtrade.un.org/data/cache/partnerAreas.json')
country_code = json.loads(url.read().decode())
url.close()
country_code = pd.DataFrame(country_code['results'])

# Clean up country codes a bit
# drop 'all' and 'world'
country_code = country_code.drop([0, 1])
# drop areas that are "nes" or "Fmr"
country_code = country_code[~country_code['text'].str.contains(', nes|Fmr')]
# drop some specific countries
country_code = country_code[country_code['text'] != 'Czechoslovakia']
country_code = country_code[country_code['text'] != 'East and West Pakistan']
country_code = country_code[country_code['text'] != 'Fr. South Antarctic Terr.']
country_code = country_code[country_code['text'] != 'Free Zones']
country_code = country_code[country_code['text'] != 'Belgium-Luxembourg']
country_code = country_code[country_code['text'] != 'Antarctica']
country_code = country_code[country_code['text'] != 'Br. Antarctic Terr.']
country_code = country_code[country_code['text'] != 'Br. Indian Ocean Terr.']
country_code = country_code[country_code['text'] != 'India, excl. Sikkim']
country_code = country_code[country_code['text'] != 'Peninsula Malaysia']
country_code = country_code[country_code['text'] != 'Ryukyu Isd']
country_code = country_code[country_code['text'] != 'Sabah']
country_code = country_code[country_code['text'] != 'Sarawak']
country_code = country_code[country_code['text'] != 'Sikkim']
country_code = country_code[country_code['text'] != 'So. African Customs Union']
country_code = country_code[country_code['text'] != 'Special Categories']
country_code = country_code[country_code['text'] != 'USA (before 1981)']
country_code = country_code[country_code['text'] != 'Serbia and Montenegro']


# ************************************************************************
# Error log file
# ************************************************************************
if os.path.isfile('log.csv'):  # if file exists, open to append
    csv_file = open('log.csv', 'a', newline='')
    error_log = csv.writer(csv_file, delimiter=',', quotechar='"')
else:  # else if file does not exist, create it
    csv_file = open('log.csv', 'w', newline='')
    error_log = csv.writer(csv_file, delimiter=',', quotechar='"')
    error_log.writerow(['reporter_id', 'reporter', 'trade_flow', 'status', 'message', 'time'])

# ************************************************************************
# Imports and exports of ice cream
# ************************************************************************

for rg in [1, 2]:  # 1 for imports, 2 for exports
    for i in country_code['id']:  # loop over all countries
        time.sleep(45)  # due to limits on public API (100 calls/hour), wait for 45 seconds

        try:
            url = urlopen('http://comtrade.un.org/api/get?px=HS&cc=AG6&r=' + str(i) + '&rg=' + str(rg) + '&p=0&freq=A&ps=2015&fmt=json')
            raw = json.loads(url.read().decode())
            url.close()
        except:  # if did not load, try again
            try:
                url = urlopen('http://comtrade.un.org/api/get?px=HS&cc=AG6&r=' + str(i) + '&rg=' + str(rg) + '&p=0&freq=A&ps=2015&fmt=json')
                raw = json.loads(url.read().decode())
                url.close()
            except:  # if did not load again, move on to the next country in the loop
                error_log.writerow([country_code[country_code['id'] == str(i)]['text'].tolist()[0], i, rg, 'Fail', raw['validation']['message'], time.ctime()])
                print('Fail: country ' + str(i) + ', direction ' + str(rg) + '. Message: ' + str(raw['validation']['message']))
                continue

        # if no data was downloaded, move to next country
        if len(raw['dataset']) == 0:
            error_log.writerow([country_code[country_code['id'] == str(i)]['text'].tolist()[0], i, rg, 'No data', raw['validation']['message'], time.ctime()])
            print('No data: country ' + str(i) + ', direction ' + str(rg) + '. Message: ' + str(raw['validation']['message']))
            continue

        # Keep only ice cream
        data = pd.DataFrame(raw['dataset'])
        data = data.loc[data['cmdCode'] == '210500', :]

        # Save if there is data for ice cream
        if len(data) != 0:
            data.to_csv('data/' + str(i) + '_' + str(rg) + '.csv', index=False)
            error_log.writerow([country_code[country_code['id'] == str(i)]['text'].tolist()[0], i, rg, 'Success', raw['validation']['message'], time.ctime()])
            print('Success: country ' + str(i) + ', direction ' + str(rg))
        else:
            error_log.writerow([country_code[country_code['id'] == str(i)]['text'].tolist()[0], i, rg, 'Success, but no ice cream', raw['validation']['message'], time.ctime()])
            print('Success, but no ice cream: country ' + str(i) + ', direction ' + str(rg))

csv_file.close()
