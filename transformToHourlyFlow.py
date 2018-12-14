import pandas as pd 

xls = pd.ExcelFile('forTransformation.xlsx')

vehicleBreakdown = xls.parse('vehicleBreakdown')
averageSpeed = xls.parse('averageSpeed', header=[0,1], index_col=[0])
VEH = xls.parse('VEH', header=[0,1], index_col=[0])
HV = xls.parse('HV')

vehicleBreakdown = vehicleBreakdown.fillna(method='ffill')
averageSpeed = averageSpeed.fillna(method='ffill')
VEH = VEH.fillna(method='ffill')
HV = HV.fillna(method='ffill')

#print(averageSpeed)
averageSpeed = averageSpeed.stack().reset_index()
averageSpeed.columns = ['Road ID', 'Year', 'Average Speed']

VEH = VEH.stack().reset_index()
VEH.columns = ['Road ID', 'Year', '2 Way VEH']

df_1 = pd.concat([averageSpeed, VEH['2 Way VEH']], axis = 1)
df_1 = df_1.sort_values(['Road ID', 'Year'])

df_2 = pd.concat([vehicleBreakdown, HV], axis = 1)
df_2 = pd.concat([df_2]*4)

df_1.reset_index(drop=True, inplace=True)
df_2.reset_index(drop=True, inplace=True)

result = pd.concat([df_1, df_2], axis = 1)
result = result.T.drop_duplicates().T

cols = ['Road ID', 'Year', 'Hour', '2 Way VEH', 'Average Speed', 'Taxi, LGV3, LGV4, LGV6, HGV7, HGV8, PLB, PV4, PV5, NFB6, NFB7, NFB8, FBSD, FBDD, MC, HV%']


result.to_csv('hourlyVehicleFlow_transformed.csv', index = False)




