# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %% [markdown]
# # Main Program

# %%
from bs4 import BeautifulSoup
import requests
import pandas as pd


# %%
url = "https://www.cisco.com/c/en/us/td/docs/switches/datacenter/aci/apic/sw/all/syslog/guide/b_ACI_System_Messages_Guide/m-aci-f{}x-messages.html"
output = pd.DataFrame()
count = 0

def f(a):
    a = a.lstrip()
    if "If you see this fault, take the following actions:" in a :
        a = a.split('If you see this fault, take the following actions:')[1].lstrip()
    return a


# %%
for url_num in range(10):
    #url_num = 9
    print("start at page {}".format(url_num))

    response = requests.get(url.format(url_num))
    soup = BeautifulSoup(response.text, 'html.parser')
    b = soup.find_all("section", "section")

    for i in b:
        
        data = {}
        
        Title = i.h3.text
        data['SN'] = Title.split(': ')[0] 
        data['Name'] = Title.split(':')[1]
        
        p = i.find_all('p')
        data['Serverity'] = p[0].text.split(':')[1].lstrip()
        try:
            data['Explanation'] = p[1].text.split('Explanation:')[1].lstrip()
        except:
            data['Explanation'] = 'This Fault does not have it'
        
        try: 
            flag = 0
            R = p[2].text.split('Recommended Action:')[1].lstrip()
            data['ReconmandAction'] = f(R)
            
        except:
            flag = 1
        
        if flag == 1:
            try:
                R = i.section.text.split('Recommended Action:')[1].lstrip()
                data['ReconmandAction'] = f(R)
            except:
                data['ReconmandAction'] = 'This Fault does not have it'
            
        output = output.append(data, ignore_index = True)


# %%
output = output.reindex(columns = ['SN', 'Name', 'Serverity', 'Explanation', 'ReconmandAction'])
output


# %%
output.to_excel('test.xlsx')

# %% [markdown]
# ## END

