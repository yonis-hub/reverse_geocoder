import os
import csv 
import json
import time
from numpy.lib.npyio import loadtxt
import requests
import pandas as pd

#load cvs into pandas df
sites_pd = pd.read_csv("../Resources/test1.csv")
# print(sites_pd)

#clean the table
clean_sites_pd = sites_pd.drop(['name'], axis=1)
print(clean_sites_pd)


#reverse geocoder
class ReverseGeocoder:
    #base url
    base_url = 'https://nominatim.openstreetmap.org/reverse'

    #store results
    state_names = []
    latx = []
    lngy = []

    def fetch(self, lat, lon):
        #headers user-agent of the browser
        headers = {
            'user-agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'
        }

        #parameters
        params = {
            'format' : 'geocodejson',
            'lat' : lat,
            'lon' : lon
        }

        #HTTP GET request 
        res = requests.get(url=self.base_url, params=params, headers=headers)
        print('HTTP GET request to URL: %s | Status code: %s' % (res.url, res.status_code))

        if res.status_code == 200:
            return res
        else:
            return None

    def parse(self, res):
        # get the data
        # self.latx.append(res['features'][0]['geometry']['coordinates'][1])
        # self.lngy.append(res['features'][0]['geometry']['coordinates'][0])
        # self.state_names.append(res['features'][0]['properties']['geocoding']['admin']['level4'])
        x = res['features'][0]['properties']['geocoding']['admin']['level4']
        print(x)
        # print(json.dumps(latx, indent=2))
        # print(json.dumps(lngy, indent=2))
        # print(json.dumps(state_names, indent=2))

        df = pd.DataFrame({'State Name': self.state_name, 'lat': self.latx, 'lon': self.lngy})
        print(df)

        #combine state names with lat n lon
        # frames = [clean_sites_pd,df]
        # combine = pd.concat(frames)
        # print(combine)
        # print(clean_sites_pd)
        # print(df)
    
    #save the results
    def store_results(self):

        # df.to_csv("test.csv", encoding="utf-8", index=False, header=True)
        pass

        #example
        # with open('results.json', 'w') as f:
        #     f.write(json.dumps(self.results, indent=2))
       
    def run(self):
       
        for index, row in clean_sites_pd.iterrows():

            try:
                # extract lat and lon
                lat = row['lat']
                lon = row['lng']
                # print(lat)
                # print("-------------------")
                # print(lon)
                #make HTTP resquest to Nominatim API
                res = self.fetch(lat, lon)
                self.parse(res.json())

                #time out
                time.sleep(1)

            except:
                pass
            #store results
            self.store_results()

    
        
#main driver 
if __name__ == '__main__':
    reverse_geocoder = ReverseGeocoder()
    reverse_geocoder.run()
    