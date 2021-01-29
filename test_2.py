# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %% [markdown]
# # Generate Final Result
# %% [markdown]
# ## Program Logic:
# 
# ```pseudocode
# 
# open("dest_excel")
# DataFrame(open("data_source"))
# 
# for line in dest_excel:
#     target = specialtreat(line)
#     if  (target in data_source.xlsx) :
#         insert data_source[target] to dest_excel
#     else :
#         insert "not found" to dest_excel
# 
# ```

# %%
import pandas as pd
import openpyxl

output  = pd.DataFrame()


# %%
source = pd.read_excel('test.xlsx')   # fault list from web 
dest = pd.read_excel('dest.xlsx')   #customer fault list


# %%
source


# %%
dest


# %%
dest['Alarms'] = dest['Alarms'].apply(lambda x: x.split('\xa0')[-1])
source['Name'] = source['Name'].apply(lambda x: x.split()[-1])


# %%
dest = dest.rename(columns = {'Alarms':'Name'})
dest = dest.reindex(columns = ['Name','SN', 'Serverity', 'Explanation', 'ReconmandAction'])


# %%
for i in range(1404):
    s = source[source.Name == dest.loc[i].Name]
    try:
        dest.loc[i, 'SN'] = list(s.SN)[0]
    except:
        dest.loc[i, 'SN'] = 'None'
    try:
        dest.loc[i, 'Serverity'] = list(s.Serverity)[0]
    except:
        dest.loc[i, 'Serverity'] = 'None'
    try:
        dest.loc[i, 'Explanation'] = list(s.Explanation)[0]
    except:
        dest.loc[i, 'Explanation'] = 'None'
    try:
        dest.loc[i, 'ReconmandAction'] = list(s.ReconmandAction)[0]
    except:
        dest.loc[i, 'ReconmandAction'] = 'None'
    


# %%
dest.to_excel('result.xlsx')


# %%
dest


# %%
not_found = dest[dest.SN == 'None']


# %%
not_found.to_excel('not_found.xlsx')

# %% [markdown]
# ## END

