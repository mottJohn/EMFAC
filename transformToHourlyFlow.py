import pandas as pd 

xls = pd.ExcelFile('forTransformation.xlsx')

vehicleBreakdown = xls.parse('vehicleBreakdown')
averageSpeed = xls.parse('averageSpeed', header=[0,1], index_col=[0])
VEH = xls.parse('VEH', header=[0,1,2], index_col = [0])
HV = xls.parse('HV')

vehicleBreakdown = vehicleBreakdown.fillna(method='ffill')
averageSpeed = averageSpeed.fillna(method='ffill')
VEH = VEH.fillna(method='ffill')
HV = HV.fillna(method='ffill')

#print(averageSpeed)
averageSpeed = averageSpeed.stack().reset_index()
averageSpeed.columns = ['Road ID', 'Year', 'Average Speed']
averageSpeed = pd.concat([averageSpeed]*3)
averageSpeed = averageSpeed.reset_index(drop = True)
averageSpeed = averageSpeed.sort_values(['Road ID', 'Year'])

vehicleBreakdown = pd.concat([vehicleBreakdown]*3)
vehicleBreakdown = vehicleBreakdown.reset_index(drop = True)

HV = pd.concat([HV]*3)
HV = HV.reset_index(drop = True)

VEH = VEH.stack([0,1,2]).reset_index()
VEH = VEH.drop(columns = ['level_1'])

VEH.columns = ['Road ID', 'Year', 'Direction', 'VEH']
VEH['Direction'] = pd.Categorical(VEH['Direction'], ['Bothbound', 'NB', 'SB'])
VEH = VEH.sort_values(['Road ID', 'Direction'])
VEH = VEH.reset_index(drop = True)

df_1 = pd.concat([averageSpeed, VEH.drop(columns = ['Road ID', 'Year'])], axis = 1)
df_1 = df_1.reset_index(drop = True)

df_2 = pd.concat([vehicleBreakdown, HV], axis = 1)
df_2 = pd.concat([df_2]*4)

df_1.reset_index(drop=True, inplace=True)
df_2.reset_index(drop=True, inplace=True)

result = pd.concat([df_1, df_2], axis = 1)
result = result.loc[:, ~result.columns.duplicated()]

cols = ['Road ID', 'Direction', 'Year', 'Hour', 'VEH', 'Average Speed', 'Taxi', 'LGV3', 'LGV4', 'LGV6', 'HGV7', 'HGV8', 'PLB','PV4', 'PV5', 'NFB6', 'NFB7', 'NFB8', 'FBSD', 'FBDD', 'MC', 'HV%']


result.to_csv('hourlyVehicleFlow_transformed.csv', index = False)

print(df_1)



