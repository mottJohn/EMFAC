###############################
#USER INPUTS
###############################
year = 2023 #the year of concerned
percentOfVKT = 12.6/100
factor = 100
path_basicInfo = r"C:\Users\CHA82870\OneDrive - Mott MacDonald\Documents\EMFAC\roadBasicInfo.xlsx"
path_hourlyData = r"C:\Users\CHA82870\OneDrive - Mott MacDonald\Documents\EMFAC\hourlyVehicleFlow_transformed.csv"
path_population = r"C:\Users\CHA82870\OneDrive - Mott MacDonald\Documents\EMFAC\populationData.xlsx"
path_emfac = r"C:\Users\CHA82870\OneDrive - Mott MacDonald\Documents\EMFAC\tripsVKT_emfac.xlsx"
path_standard_index = r"C:\Users\CHA82870\OneDrive - Mott MacDonald\Documents\EMFAC\Road Type Code.xlsx"

###############################
#CODES DO NOT MODIFY
###############################
import numpy as np
import pandas as pd
from pandas import ExcelWriter

basicInfo = pd.read_excel(path_basicInfo)
hourlyData = pd.read_csv(path_hourlyData)
population = pd.read_excel(path_population)
Data = hourlyData.merge(basicInfo, on = ['Road ID', 'Direction']) #fiat and clean input format
emfac = pd.read_excel(path_emfac)
standard_index = pd.read_excel(path_standard_index)

# cols with vehicle type (should be expanded if new types are added)
cols_vehicle = ['PC', 'Taxi', 'LGV3', 'LGV4', 'LGV6', 'HGV7', 'HGV8', 'PLB', 'PV4', 'PV5', 'NFB6', 'NFB7', 'NFB8', 'FBSD', 'FBDD','MC']

Trips = Data.copy() #create a copy of "Data"
VKT = Data.copy() #create a copy of "Data"

for col in cols_vehicle:
    Trips[col] = Data['VEH']*(Data[col]/100) #Trips equal to VEH*vehicleType(%)
    VKT[col]= Trips[col]* Trips['Length']/1000 #VKT equal to Trips * length in km

hour = Data['Hour'].unique() #get unique hours, from 0 - 23

#######
# codes for generating hourly summary tables in excel tabs
#######

"""
result = []
writer = ExcelWriter("hourly trips and VKT.xlsx")
writer_2 = ExcelWriter("VKT.xlsx")

cols = [x + '_VKT' for x in cols]

for hr in hour:
    df = Data[(Data['Hour'] == hr) & (Data['Year'] == year)]
    df.to_excel(writer,'Hour {}'.format(hr), index = False)
    df_2 = df.groupby('Road Type (Speed Limit)').sum()
    df_2 = df_2[cols]
    df_2.to_excel(writer_2,'Hour {}'.format(hr))


writer.save()
writer_2.save()
"""
hourly_VKT = pd.DataFrame() #empty dataframe to store hourly VKT
for hr in hour:
    df = VKT[(VKT['Hour'] == hr) & (VKT['Year'] == year)] #filter hr and year
    df_2 = df.groupby('Road Type (Speed Limit)').sum() #groupby road type and sum the VKT 
    df_2 = df_2[cols_vehicle] #select columns of concern
    df_2['Hour'] = hr # add the hour back for later use

    try:
        hourly_VKT = pd.concat([hourly_VKT, df_2])
    except:
        hourly_VKT = df_2

cols = population.columns.tolist()[-45:]
population['Total'] = population[cols].sum(axis = 1)
per_fuelType = pd.pivot_table(population, values = 'Total', index=['Vehicle Type'], columns = ['Year','Fuel Type'], aggfunc= np.sum)

total= per_fuelType.sum(axis = 1)
#print(per_fuelType)
fuelRatio = per_fuelType.div(total, axis = 'index')
#print(fuelRatio[2023]['Petrol'])

emfac['Trips per Estimated VKT'] = emfac['Trips']/(emfac['VKT']*percentOfVKT)
tripsPerVKT = emfac.groupby('Vehicle Type').max()['Trips per Estimated VKT']

for col_fuel in fuelRatio[year].columns:
    VKT_fuel = hourly_VKT.groupby(['Hour',hourly_VKT.index]).sum()*fuelRatio[year][col_fuel]
    Trips_fuel = VKT_fuel*tripsPerVKT

    for i in VKT['Road Type (Speed Limit)'].unique():
        output = Trips_fuel[Trips_fuel.index.get_level_values(1).isin([i])].T*factor
        output = pd.merge(standard_index, output, left_on='Code', right_index=True, how='left')
        output = output.fillna(0)
        output.to_csv('Trips_{}_Type{}.csv'.format(col_fuel, i))

        output = VKT_fuel[VKT_fuel.index.get_level_values(1).isin([i])].T*factor
        output = pd.merge(standard_index, output, left_on='Code', right_index=True, how='left')
        output = output.fillna(0)
        output.to_csv('VKT_{}_Type{}.csv'.format(col_fuel, i))