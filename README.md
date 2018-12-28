# EMFAC PROJECT
A python library to transform data into [EMFAC](https://www.epd.gov.hk/epd/english/environmentinhk/air/guide_ref/emfac-hk.html) model input.

The inputs of the library should be in a standard format. Therefore, table schema is defined first, and the logic of generating output tables will be presented.

# Get Started
1. Git clone or download the zip to your local directory

2. Modify the user inputs section in functions.py (You can use the sample files in sample folder)

3. Run the functions.py (e.g. In anaconda prompt, navigate to the directory, and type python functions.py)

4. Output files will be generated within the same directory

5. If you need to transform the data (See below section for details), use transformToHourlyFlow.py

# Template for Traffic Consultant
Currently, the format of subconsultant's submission is not computer friendly. In fact, there are mutiple tables joined together as one large table.

The table format is very important. To reshape the data from consultant, I used 2.5 hours.

It is suggested the traffic consultant should follow Table Schema 1 and 2 (You can find the sample in Samples/hourlyVehicleFlow_transformed.csv), or the schema below(You can find the sameple in Samples/hourlyVehicleFlow.xlsx).

If you follow the table schema below, you can use transformToHourlyFlow.py to transform the data to suitable format. If you use the table schema in Table Schema Section, you don't need to transform anyting.

1. A table to store vehicle breakdown in Percent (The assuption of such table is vehice breakdown is a variable of time and road id only)
    * Road ID
    * Hour
    * Vehicle breakdown for each vehicle types

2. A table to store average speed (The assumption of such table is vehicle breadown is a variable of time and road id only)
    * Road ID
    * Hour
    * Year in multiindex (After flattening should be Year and average speed in column)

3. A table to store VEH (The assumption of such table is VEH is a variable of road id, hour, year, and direction only)
    * Road ID
    * Hour
    * Year, and direction in multiindex (after flatterning should be Year, and direction, and VEH in columns)

4. A table to store HV (HV is a variable to Road ID and Hour only)
    * Road ID
    * Hour
    * HV%

# Table Schema

1. A table to store basic road information (From traffic consultant)
    * Road ID : Primary Key (problem found: not unique; road id and direction tgt is unique)
    * Road Name
    * Road Section
    * Road Type (Speed Limit)
    * Road Type (Major or Minor)
    * Direction [NB, SB, EB, WB, Bothbound]
    * Design Speed Limit [km/h]
    * Distance/ Length [meters]

2. A table to store hourly information for each Road ID (From traffic consultant)
    * Road ID: Primary Key (problem found: not unique; road id and direction tgt is unique)
    * Direction [NB, SB, EB, WB, Bothbound]
    * Year [YYYY]
    * Hour [0-23]
    * VEH 
    * Average Speed [km/h]
    * vehicle Type Breakdown: 16 columns [%]
    * HV %

3. A table to store vehicle population (From EMFAC)
    * Index (Primary Key)
    * Year [YYYY]
    * Fuel Type
    * Vehicle Type
    * Description of Vechicle Type
    * Age01 to Age45 columns

4. A table to store data from EMFAC (From EMFAC)
    * Year [YYYY]
    * Vehicle Type
    * Description of Vechicle Type
    * Trips
    * VKT

5. A table to store Road Type code with description which is standard from Emfac
    * Code
    * Description

# Output Tables

## Hourly vehicle count in each road per year
1. Table 2['2 Way VEH'] * (Vehicle Type Breakdown)
2. Merge with Table 1 to get basic information
3. Sort by hour and generate excel with 24 hours tabs

## Hourly VKT in each road per year
1. Mutiply Hourly vehicle count in each road by road length

## Hourly total VKT per vehicle type grouped by road type
1. Group Hourly VKT in each road by road type

## Fuel type per all vehicle ratio in each type of vehicle per year
1. pivot 1:
    * row: Vehicle Type
    * columns: ['Year', 'Fuel Type]
    * value: sum age01-45

2. Sum pivot 1 across columns to get total number of vehicle

3. Divide pivot 1 with the sum to get fuel type per all vehicle ratio

## Trip/ VKT in each type of vehicle
1. Trips per estimated VKT = Trips/(VKT*percent of VKT)
2. Get the Max across each year

## Input files for EMFAC
1. Trips per fuel type per road type
2. VKT per fuel type per road type

# In short, what are we doing here?
We are just modified the assumptions in Emfac Model to the project area instead of using the data for Hong Kong as a whole provided by EPD.