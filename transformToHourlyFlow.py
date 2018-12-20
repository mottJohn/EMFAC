import pandas as pd 

xls = pd.ExcelFile('forTransformation.xlsx')

vehicleBreakdown = xls.parse('vehicleBreakdown')
averageSpeed = xls.parse('averageSpeed', header=[0,1], index_col=[0,1])
VEH = xls.parse('VEH', header=[0,1,2], index_col = [0,1])
HV = xls.parse('HV')

vehicleBreakdown = vehicleBreakdown.fillna(method='ffill')
averageSpeed = averageSpeed.fillna(method='ffill')
VEH = VEH.fillna(method='ffill')
HV = HV.fillna(method='ffill')

averageSpeed = averageSpeed.stack().reset_index()
averageSpeed.columns = ['Road ID', 'Hour', 'Year', 'Average Speed']

VEH = VEH.stack([0,1,2]).reset_index()

VEH = VEH.drop(columns = ['level_2'])
VEH.columns = ['Road ID', 'Hour', 'Year', 'Direction', 'VEH']

#print(averageSpeed)
VEH_Break = VEH.merge(vehicleBreakdown, on = ['Road ID', 'Hour'])
VEH_Break_HV = VEH_Break.merge(HV, on =  ['Road ID', 'Hour'])
VEH_Break_HV_Hour = VEH_Break_HV.merge(averageSpeed, on = ['Road ID', 'Year', 'Hour'])

cols = ['Road ID', 'Direction', 'Year', 'Hour', 'VEH', 'Average Speed', 'PC', 'Taxi', 'LGV3', 'LGV4', 'LGV6', 'HGV7', 'HGV8', 'PLB','PV4', 'PV5', 'NFB6', 'NFB7', 'NFB8', 'FBSD', 'FBDD', 'MC', 'HV%']

VEH_Break_HV_Hour = VEH_Break_HV_Hour[cols]
VEH_Break_HV_Hour.to_csv('hourlyVehicleFlow_transformed.csv', index = False)
