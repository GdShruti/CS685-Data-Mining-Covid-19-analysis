#!/usr/bin/env python
# coding: utf-8

# In[25]:


import json
import pandas as pd

neighbor_mod_json = json.load(open("neighbor-districts-modified.json"))


# In[ ]:





# In[26]:


d={}
id=101
for x in sorted(neighbor_mod_json):
    d[x]={'id':id , 'neighbors': sorted(neighbor_mod_json[x])}
    id += 1


# In[ ]:





# In[28]:


json_object = json.dumps(d, indent = 4) 
with open("neighbor-districts-modified.json", "w") as outfile: 
    outfile.write(json_object) 


# In[ ]:




