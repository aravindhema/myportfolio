#!/usr/bin/env python
# coding: utf-8

# In[15]:


import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np


# In[16]:


#import the api for sec-edgar
from sec_api import QueryApi

queryApi = QueryApi(api_key="#######"
                   )


# In[112]:


#Form 4 filings to be downloaded; query for formtype 4
query = {
    "query": {
        "query_string": {
            "query": "formType:\"4\""
        }
    },
    "from": "0",
    "size": "100",
    "sort": [{ "filedAt": { "order": "desc" } }]
}

filings = queryApi.get_filings(query)
#filings = fullTextSearchApi.get_filings(query)
filings


# In[143]:


#Now that we have the filings from api, open each xml file and get the transaction code and 
#amount values to calculate the purchase amount
import lxml
import requests
#mask requests with a header to prevent 403 error
heads = {'Host': 'www.sec.gov', 'Connection': 'close', 'Accept': 'application/json, text/javascript, /; q=0.01', 'X-Requested-With': 'XMLHttpRequest', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36', }
text1= filings.get('filings') 

issuer = []
urllist = []
amountf = []
counter = 0
for i in range(0,len(text1)):
    url = text1[i].get('linkToFilingDetails')
    r = requests.get(url,headers=heads)
    print(url)
    counter = counter + 1
    print(counter)
    soup = BeautifulSoup(r.content,"lxml")

    print(r)
    rs1 = soup.find_all('table')
    
    #This will get the xml table that has the code, amount, price. 
    rs2 = rs1[12].find_all('td')
    print('rs2 len is ',len(rs2))
    if(len(rs2) != 0):
        #This field will get the issuer name
        rs3 = rs1[4].find_all('td')
    #print(rs3[13].text)
    
        #We need to look for trans code P. Mutiple such entries can be present 
        #so customize the index accoringly to get all the entries 
        pcounter = 11 # index increment counter
        pidx = 3 #this gets the trans code from the xml table
        aidx1 = 5 # This gets the amount from the xml table
        aidx2 = 7 #this gets the price from the xml table
        amount = 0
        count = 0
        while(1):
            count = count + 1
            if(rs2[pidx].text == 'P'): #look only for P
                print('P found')
                amt1 = int(rs2[aidx1].text.replace(',',''))  #convert to numeric  
                amt2 = float(''.join(e for e in rs2[aidx2].text if e in '1234567890.')) #convert to numeric
                amount +=  amt1 * amt2 #purchase amount computation
           
                if(pidx + pcounter) <= len(rs2): #does another entry with P exist
                    pidx += pcounter
                    aidx1 += pcounter
                    aidx2 += pcounter
                else:
                    urllist.append(url) #no more entries so create the dataframe list
                    amountf.append(amount)
                    issuer.append(rs3[13].text)
                    break 
            else:   # no P entries so either loop or exit if all entries covered
                if(count > len(rs2)):
                    break
 


# In[ ]:


import pandas as pd


# In[148]:


#convert the list to a dataframe
df = pd.DataFrame(list(zip(urllist,issuer,amountf)),columns=['URL','Issuer','Purchase Amt'])
df.head()


# In[153]:

#export to csv
df.to_csv('outputedgar.csv')



