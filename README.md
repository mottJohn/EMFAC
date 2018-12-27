# EMFAC PROJECT
A python library to transform data into [EMFAC](https://www.epd.gov.hk/epd/english/environmentinhk/air/guide_ref/emfac-hk.html) model input.

The inputs of the library should be in a standard format. Therefore, table schema is defined first, and the logic of generating output tables will be presented.

# Template for Traffic Consultant
Currently, the format of subconsultant's submission is not computer friendly. In fact, there are mutiple tables joined together as one large table.

It is suggested the traffic consultant should follow the format below:
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
    * Direction
    * Design Speed Limit
    * Distance/ Length

2. A table to store hourly information for each Road ID (From traffic consultant)
    * Road ID: Primary Key (problem found: not unique; road id and direction tgt is unique)
    * Direction
    * Year
    * Hour
    * VEH
    * Average Speed
    * vehicle Type Breakdown: 16 columns
    * HV %

    The table format is very important. To reshape the data from consultant, I used 2.5 hours.

3. A table to store vehicle population (From EMFAC)
    * Index (Primary Key)
    * Year
    * Fuel Type
    * Vehicle Type
    * Description of Vechicle Type
    * Age01 to Age45 columns

4. A table to store data from EMFAC (From EMFAC)
    * Year
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

## Hourly total VKT per vehicle type
1. Group Hourly VKT in each road by road type

## Fuel type per all vechile ratio in each type of vehicle per year
1. pivot 1:
    * row: Vehicle Type
    * columns: ['Fuel Type', 'Year']
    * value: sum age01

2. pivot 2:
    * row: Vehicle Type
    * columns: ['Year']
    * value: count index

3. Divde pivot 1 by pivot 2

## Trip/ VKT in each type of vehicle
1. Calculate the percentage share of each type of roads to the toal
2. Multiply Trips in Table 4 by the percentage share
3. Divide the defaulty trip with estimated VKT
4. Get the Max across each year