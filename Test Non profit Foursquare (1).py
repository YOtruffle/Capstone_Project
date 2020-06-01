#!/usr/bin/env python
# coding: utf-8

# # Capstone Project

# ## Business Problem

# Fitness is a growing trend, especially across the Middle East. The combination of having to constantly look good on social media and the healthy revolution has led to a significant increase in the number of those joining gyms, many of whom would not traditionally do so. In addition as COVID-19 linked lockdowns begin to ease, people are likely to flock to gyms and fitness centres to shed the pounds gained while stuck at home. Location is central to which gym people choose, nobody wants a half-hour commute for a workout. As of such I will leverage Foursquare API data to find the areas in Beirut, the capital of Lebanon, that are most underserved with fitness centres and use that as a proxy for where the optimal location for a new gym would be. 

# ## Data 

# Complete data on Lebanon is scarce; few people collect or update it. As of such my ability to work with the Foursquare API is limited as many locations do not have a category or are missing some other entry. That said, the most complete list I could find was that of gyms and fitness centres and hence that is what data I will use.

# In[19]:


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


# In[20]:


CLIENT_ID = 'ZF1BTD4OS3INYB1FQLKAK53W1S0SFVVCGZIPNKEHGQ1OHVME' # your Foursquare ID
CLIENT_SECRET = '3QVK0RDV12UMU3RX3BOXUYC0OTB2HXOB3OWNETO3ET0OK43N' # your Foursquare Secret
VERSION = '20200000'
LIMIT = 30
print('Your credentails:')
print('CLIENT_ID: ' + CLIENT_ID)
print('CLIENT_SECRET:' + CLIENT_SECRET)


# In[21]:


address = 'Mar Antonios Street, Beirut'

geolocator = Nominatim(user_agent="foursquare_agent")
location = geolocator.geocode(address)
latitude = location.latitude
longitude = location.longitude
print(latitude, longitude)


# In[28]:


search_query = 'Fitness'
radius = 10000000
print(search_query + ' .... OK!')


# In[29]:


url = 'https://api.foursquare.com/v2/venues/search?client_id={}&client_secret={}&ll={},{}&v={}&query={}&radius={}&limit={}'.format(CLIENT_ID, CLIENT_SECRET, latitude, longitude, VERSION, search_query, radius, LIMIT)
url


# In[30]:


results = requests.get(url).json()
results


# In[31]:


# assign relevant part of JSON to venues
venues = results['response']['venues']

# tranform venues into a dataframe
dataframe = json_normalize(venues).head(100)


# In[32]:


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


# In[33]:


venues_map = folium.Map(location=[latitude, longitude], zoom_start=13) # generate map centred around the Conrad Hotel

# add a red circle marker to represent the Conrad Hotel
folium.features.CircleMarker(
    [latitude, longitude],
    radius=10,
    color='red',
    popup='Conrad Hotel',
    fill = True,
    fill_color = 'red',
    fill_opacity = 0.6
).add_to(venues_map)

# add the Italian restaurants as blue circle markers
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


# In[ ]:


dataframe_filtered['categories'].value_counts()


# ## Trending

# In[ ]:


# define URL
url = 'https://api.foursquare.com/v2/venues/trending?client_id={}&client_secret={}&ll={},{}&v={}'.format(CLIENT_ID, CLIENT_SECRET, latitude, longitude, VERSION)

# send GET request and get trending venues
results = requests.get(url).json()
results


# In[ ]:


if len(results['response']['venues']) == 0:
    trending_venues_df = 'No trending venues are available at the moment!'
    
else:
    trending_venues = results['response']['venues']
    trending_venues_df = json_normalize(trending_venues)

    # filter columns
    columns_filtered = ['name', 'categories'] + ['location.distance', 'location.city', 'location.postalCode', 'location.state', 'location.country', 'location.lat', 'location.lng']
    trending_venues_df = trending_venues_df.loc[:, columns_filtered]

    # filter the category for each row
    trending_venues_df['categories'] = trending_venues_df.apply(get_category_type, axis=1)


# In[ ]:


trending_venues_df


# In[ ]:




