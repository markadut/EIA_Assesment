#importing necessary libraries
import pandas as pd
import requests
from datetime import date
import matplotlib.pyplot as plt

#calling the api key to connect to EIA API
api_key = 'e1d99ebe2979507b12f16080b8acfb6d'

#setting colnames for pandas dataframe to ease data ordering and manipulation
colnames = ['NY_Mwh', 'MA_Mwh', 'NH_Mwh', 'ME_Mwh', 'CT_Mwh', 'RI_Mwh', 'VT_Mwh']

#entering all of the Series IDs here separated by commas
series_IDS = ["ELEC.GEN.HYC-NY-99.M",
              "ELEC.GEN.HYC-MA-99.M ",
              "ELEC.GEN.HYC-NH-99.M",
              "ELEC.GEN.HYC-ME-99.M",
              "ELEC.GEN.HYC-CT-99.M",
              "ELEC.GEN.HYC-RI-99.M",
              "ELEC.GEN.HYC-VT-99.M"]

#creating an empty list to later append the extracted EIA data.
conv_hydro_data = []

#setting the 2010 through 2019 interval
start_date = '2010-01-01'
end_date = '2019-12-01'

#pulling the data

for i in range(len(series_IDS)):
    url = "http://api.eia.gov/series/?api_key=" + api_key + "&series_id=" + series_IDS[i]
    r = requests.get(url)
    json_data = r.json()

    if r.status_code == 200:
        print('Succesfully Pulled Data!')
    else:
        print('Error')

    df = pd.DataFrame(json_data.get('series')[0].get('data'),
                      columns = ['Date', colnames[i]])
    df.set_index('Date', drop=True, inplace=True)
    conv_hydro_data.append(df)

# print(conv_hydro_data)


#cleaning and aggregating the datasets by changing EIA date format to datetime
#combining the two datasets (NEW, NY) into one by calling concat
conv_hydro = pd.concat(conv_hydro_data, axis=1)

#creating date as datetype datatype
conv_hydro['Year'] = conv_hydro.index.astype(str).str[:4] # indexing year out of EIA date format
conv_hydro['Month'] = conv_hydro.index.astype(str).str[4:] # indexing year out of EIA date format
conv_hydro['Day'] = 1 # setting the day to first day of month for simplicity, conversion to datetime format
# conv_hydro['Date'] = pd.to_datetime([[conv_hydro.index.astype(str).str[:4], conv_hydro.index.astype(str).str[4:], 1]])
conv_hydro['Date'] = pd.to_datetime(conv_hydro[['Year','Month','Day']])

conv_hydro.set_index('Date',drop=False,inplace=True)
conv_hydro.sort_index(inplace=True)
conv_hydro = conv_hydro[start_date:end_date]

#converting units of conventional hydroelectric production from thousand megawatthours to megawatthours
for col in colnames:
  conv_hydro[col] *= 1000

#return the statistical summary of the data to check consistency
conv_hydro.describe()

#creating variables with state names to ease generation of visualizations etc.
# New_York = conv_hydro["NY_Mwh"]
# Massachusetts = conv_hydro["MA_Mwh"]
# New_Hamsphire = conv_hydro["NH_Mwh"]
# Maine = conv_hydro["ME_Mwh"]
# Connecticut = conv_hydro["CT_Mwh"]
# Rhode_Island = conv_hydro["RI_Mwh"]
# Vermont = conv_hydro["VT_Mwh"]

del conv_hydro['Year']
del conv_hydro['Month']
del conv_hydro['Day']

conv_hydro.head(120) # view/print datafrme

# visualizing the data
plot = conv_hydro.plot(figsize=(12,8),
                  linewidth=2,
                  legend=True)

plot.set_xlabel('Year')
plot.set_ylabel('Conventional Hydro (Mwh)')

plot.grid(color='#eeefff')
