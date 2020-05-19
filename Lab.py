#!/usr/bin/env python
# coding: utf-8

# In[53]:


import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from urllib.request import urlopen

data = urlopen('https://en.wikipedia.org/wiki/List_of_postal_codes_of_Canada:_M')
content = BeautifulSoup(data, 'html.parser')
table = content.find('table')
print(table.prettify())


# In[54]:


data = []
for tr in table.find_all('tr')[1:]:
    row_data = tr.find_all('td')
    data.append([cell.text for cell in row_data])
    
need = pd.DataFrame(data, columns = ['Post Code', 'Borough', 'Neighborhood'])
need.head(5)


# In[55]:


need = need[need['Borough'] != 'Not assigned']
need.reset_index(drop = True, inplace = True)


# In[56]:


need['Neighborhood'] = need['Neighborhood'].str.split('\n', expand = True)[0]
need.loc[need['Neighborhood'] == 'Not assigned', 'Neighborhood'] = need.loc[need['Neighborhood'] == 'Not assigned', 'Borough']


# In[57]:


need = need.groupby(['Post Code', 'Borough'])['Neighborhood'].apply(', '.join).reset_index()


# In[58]:


need.to_csv('need.csv', index = False)
print("Dataset shape: {}".format(need.shape))


# In[ ]:





# In[ ]:




