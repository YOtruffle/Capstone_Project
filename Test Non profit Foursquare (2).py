#!/usr/bin/env python
# coding: utf-8

# # Capstone Project

# ## Business Problem

# Fitness is a growing trend, especially across the Middle East. The combination of having to constantly look good on social media and the healthy revolution has led to a significant increase in the number of those joining gyms, many of whom would not traditionally do so. In addition as COVID-19 linked lockdowns begin to ease, people are likely to flock to gyms and fitness centres to shed the pounds gained while stuck at home. Location is central to which gym people choose, nobody wants a half-hour commute for a workout. As of such I will leverage Foursquare API data to find the areas in Beirut, the capital of Lebanon, that are most underserved with fitness centres and use that as a proxy for where the optimal location for a new gym would be. 

# ## Data 

# Complete data on Lebanon is scarce; few people collect or update it. As of such my ability to work with the Foursquare API is limited as many locations do not have a category or are missing some other entry. That said, the most complete list I could find was that of gyms and fitness centres and hence that is what data I will use.

# ## Process

# To figure out which areas in Beirut are most underserved I'll first plot all fitness centres on a map and use such to qualitatively figure out which areas would be best served by a new gym. 

# In[45]:


import requests # library to handle requests
import pandas as pd # library for data analsysis
import numpy as np # library to handle data in a vectorized manner
import random # library for random number generation

get_ipython().system('conda install -c conda-forge geopy --yes ')
from geopy.geocoders import Nominatim # module to convert an address into latitude and longitude values

# libraries for displaying images
from IPython.display import Image 
from IPython.core.display import HTML 
    
# tranforming json file into a pandas dataframe library
from pandas.io.json import json_normalize

get_ipython().system('conda install -c conda-forge folium=0.5.0 --yes')
import folium # plotting library

print('Folium installed')
print('Libraries imported.')


# In[46]:


CLIENT_ID = 'ZF1BTD4OS3INYB1FQLKAK53W1S0SFVVCGZIPNKEHGQ1OHVME' # your Foursquare ID
CLIENT_SECRET = '3QVK0RDV12UMU3RX3BOXUYC0OTB2HXOB3OWNETO3ET0OK43N' # your Foursquare Secret
VERSION = '20200000'
LIMIT = 30
print('Your credentails:')
print('CLIENT_ID: ' + CLIENT_ID)
print('CLIENT_SECRET:' + CLIENT_SECRET)


# In[47]:


address = 'Mar Antonios Street, Beirut'

geolocator = Nominatim(user_agent="foursquare_agent")
location = geolocator.geocode(address)
latitude = location.latitude
longitude = location.longitude
print(latitude, longitude)


# In[48]:


search_query = 'Fitness'
radius = 10000000
print(search_query + ' .... OK!')


# In[49]:


url = 'https://api.foursquare.com/v2/venues/search?client_id={}&client_secret={}&ll={},{}&v={}&query={}&radius={}&limit={}'.format(CLIENT_ID, CLIENT_SECRET, latitude, longitude, VERSION, search_query, radius, LIMIT)
url


# In[50]:


results = requests.get(url).json()
results


# In[51]:


# assign relevant part of JSON to venues
venues = results['response']['venues']

# tranform venues into a dataframe
dataframe = json_normalize(venues).head(100)


# In[52]:


filtered_columns = ['name', 'categories'] + [col for col in dataframe.columns if col.startswith('location.')] + ['id']
dataframe_filtered = dataframe.loc[:, filtered_columns]

# function that extracts the category of the venue
def get_category_type(row):
    try:
        categories_list = row['categories']
    except:
        categories_list = row['venue.categories']
        
    if len(categories_list) == 0:
        return None
    else:
        return categories_list[0]['name']

# filter the category for each row
dataframe_filtered['categories'] = dataframe_filtered.apply(get_category_type, axis=1)

# clean column names by keeping only last term
dataframe_filtered.columns = [column.split('.')[-1] for column in dataframe_filtered.columns]

dataframe_filtered.head(100)


# In[53]:


venues_map = folium.Map(location=[latitude, longitude], zoom_start=13) # generate map centred around the my address

# add the fitness centres as blue circle markers
for lat, lng, label in zip(dataframe_filtered.lat, dataframe_filtered.lng, dataframe_filtered.categories):
    folium.features.CircleMarker(
        [lat, lng],
        radius=5,
        color='blue',
        popup=label,
        fill = True,
        fill_color='blue',
        fill_opacity=0.6
    ).add_to(venues_map)

# display map
venues_map


# In[54]:


dataframe_filtered['categories'].value_counts()


# ## Results

# As is clear in the above dataframe, Beirut has approximately 25 fitness centres. There is a clear correlation between the number of gyms in and the level of poverty in the said area. Unfortunately data for poverty levels by area is unavailable, but the areas with the least number of gyms, Chiyah, Ghobeiry, Sin el Fil, and Corniche el Mazraa clearly have very few gyms.

# ## Discussion

# There is the obvious issue that many of these areas are poorly served by Foursquare data collectors. It is likely that gyms do exist in these regions, but are simply not listed. However, if we use listing on Foursquare as a proxy for the quality of the gym, the conclusion can be made that the areas listed above are the most underserved of quality gyms. 
# 
# It can thus be concluded that if a high-quality gym was set up in one of those areas with a buisiness model that properly targets the residents of that area, it would be a s
# uccess.

# ## Conclusion

# In conclusion, I used the Foursquare API to see which areas of Beirut have the least number of fitness centres and hence recommend potential locations for a new gym. 
