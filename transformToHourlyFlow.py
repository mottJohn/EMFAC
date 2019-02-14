import pandas as pd 

year = 2023 #the year of concerned
path_basicInfo = r"C:\Users\CHA82870\OneDrive - Mott MacDonald\Documents\EMFAC\roadBasicInfo.xlsx"
path_hourlyData = r"C:\Users\CHA82870\OneDrive - Mott MacDonald\Documents\EMFAC\hourlyVehicleFlow_transformed.csv"

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

#############################################
# For EPD template
############################################

basicInfo = pd.read_excel(path_basicInfo)
hourlyData = pd.read_csv(path_hourlyData)
Data = hourlyData.merge(basicInfo, on = ['Road ID', 'Direction']) #fiat and clean input format (inner join)

Data = Data[['Year','Road Name', 'Road ID', 'Direction', 'Road Type', 'Road Type (Major Minor)', 'Design Speed Limit', 'Hour', 'PC', 'Taxi', 'LGV3', 'LGV4', 'LGV6', 'HGV7', 'HGV8', 'PLB', 'PV4', 'PV5',
       'NFB6', 'NFB7', 'NFB8', 'FBSD', 'FBDD', 'MC']]

#print(Data.columns)

Data.to_csv("hourlyVehicleFlow_transformed_EPD.csv", index=False)

######################
# For EPD template
######################
Data_2 = Data.groupby(['Year','Road Name', 'Road ID', 'Direction', 'Road Type', 'Road Type (Major Minor)', 'Design Speed Limit','Hour']).sum()
#print(Data_2)
Data_2 = Data_2.sort_values(by = ['Year','Hour'])
Data_2.to_csv('hourlyVehicleFlow_transformed_EPD_2.csv')