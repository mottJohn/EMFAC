import pandas as pd 
import numpy as np
from pandas import ExcelWriter

xls = pd.ExcelFile('forTransformation_speedFraction.xlsx')

sheets = xls.sheet_names

result = pd.DataFrame()
for sheet in sheets:
    data = xls.parse(sheet)
    data['Hour'] = data['Hour'].fillna(method = 'ffill')
    idx = pd.MultiIndex.from_arrays([data['Hour'],data['Speed Fractions Range']])
    data = data.set_index(idx)
    data = data.drop(columns = ['Hour', 'Speed Fractions Range'])
    data = data.stack(0,1)
    data = data.reset_index()
    data.columns = ['Hour', 'Speed Fractions Range', 'Vehicle Type', 'Speed Fraction']
    data['Road Type'] = sheet

    try:
        result = pd.concat([data, result])
    except:
        result = data

cols = result.columns.tolist()
cols = cols[-1:] + cols[:-1]
result = result[cols]
result = result.sort_values(['Road Type', 'Hour'])
result.to_csv('speedFraction.csv', index=False)

#############################################
# For EPD template
############################################
writer = ExcelWriter("speedFraction_EPD.xlsx")

for vehicleType in result['Vehicle Type'].unique():
    data = pd.pivot_table(result, values= 'Speed Fraction', index= ['Speed Fractions Range'], columns= ['Hour'], aggfunc = np.sum)
    #print(data)
    data.to_excel(writer,'{}'.format(vehicleType))