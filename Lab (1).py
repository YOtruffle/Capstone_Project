#!/usr/bin/env python
# coding: utf-8

# # Neighborhood Clustering

# ## Part 1

# In[22]:


import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from urllib.request import urlopen

data = urlopen('https://en.wikipedia.org/wiki/List_of_postal_codes_of_Canada:_M')
content = BeautifulSoup(data, 'html.parser')
table = content.find('table')
print(table.prettify())


# In[23]:


data = []
for tr in table.find_all('tr')[1:]:
    row_data = tr.find_all('td')
    data.append([cell.text for cell in row_data])
    
need = pd.DataFrame(data, columns = ['Post Code', 'Borough', 'Neighborhood'])
need.head(5)


# In[33]:


need['Neighborhood'] = need['Neighborhood'].str.split('\n', expand = True)[0]
need['Borough'] = need['Borough'].str.split('\n', expand = True)[0]
need['Post Code'] = need['Post Code'].str.split('\n', expand = True)[0]
need.loc[need['Neighborhood'] == 'Not assigned', 'Neighborhood'] = need.loc[need['Neighborhood'] == 'Not assigned', 'Borough']

need = need[need['Borough'] != 'Not assigned']
need.reset_index(drop = True, inplace = True)
need.head()


# In[30]:


need.to_csv('need.csv', index = False)
print("Dataset shape: {}".format(need.shape))
need.head()


# ## Part 2

# In[34]:


location = pd.read_csv(filepath_or_buffer = 'https://cocl.us/Geospatial_data')
location.head()


# In[42]:


location = location.sort_values(by =['Postal Code'])
need = need.sort_values(by = ['Post Code'])
location = location.drop(['Postal Code'], axis = 1)


# In[53]:


full = pd.concat([need, location], axis =1)
full = full.sort_values(by = ['Neighborhood'])
full.head(100)


# ## Part 3

# In[54]:


from sklearn.cluster import KMeans

kclusters = 7
kmeans = KMeans(n_clusters=kclusters, random_state=0).fit(full)


# In[ ]:




