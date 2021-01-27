from bs4 import BeautifulSoup
import requests
import pandas as pd
from openpyxl.workbook import Workbook
from openpyxl.writer.excel import ExcelWriter


url = "https://www.cisco.com/c/en/us/td/docs/switches/datacenter/aci/apic/sw/all/syslog/guide/b_ACI_System_Messages_Guide/m-aci-f{}x-messages.html"
output = pd.DataFrame(columns=['SN', 'Name', 'Serverity', 'Explanation', 'ReconmandAction'])
count = 0

for url_num in range(10):
    print(url_num)
    response = requests.get(url.format(url_num))
    soup = BeautifulSoup(response.text, 'html.parser')
    b = soup.find_all("section", "section")

    for i in b:
        
        data = {}
        
        Title = i.h3.text
        data['SN'] = Title.split(': ')[0] 
        data['Name'] = Title.split(':')[1]
        
        p = i.find_all('p')
        data['Severity'] = p[0].text.split(':')[1]
        try:
            data['Explanation'] = p[1].text.split(':')[1]
        except:
            data['Explanation'] = ''
        try:
            data['ReconmandAction'] = i.section.text.split(':')[1]
        except:
            data['ReconmandAction'] = ''
            
        if 'critical' in data['Severity']:
            print(data)
            count += 1
            output = output.append(data, ignore_index = True)

print(output)
