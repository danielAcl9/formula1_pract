import fastf1 as ff1
import pandas as pd
from fastf1.ergast import Ergast

# Create the dataframe
ergast = Ergast()
df = pd.DataFrame()

# Inputs for year and race
num_year = input("Insert season year: ")
num_race = input("Insert race number: ")

# Load race information 
race = ff1.get_session(int(num_year), int(num_race), 'R')
race.load(weather = True)
laps = race.laps

res = race.results

# Asign driver name, abbreviation and team name
df['driver_name'] = res.BroadcastName
df['driver_abb'] = res.Abbreviation
df['team_name'] = res.TeamName

# Get circuit data, name and country
grand_prix = ergast.get_circuits(season = num_year, round = num_race)

# Convert value to string and then truncate
gp_circuit = str(grand_prix['circuitName'])
gp_country = str(grand_prix['country'])

cir_name = gp_circuit.rsplit('\n', 3)[0]
coun_name = gp_country.rsplit('\n', 3)[0]
cir_name2 = cir_name[5:]
coun_name2 = coun_name[5:]

df['circuit_name'] = cir_name2
df['circuit_country'] = coun_name2

# Get race weather data
weather = race.weather_data

temp = weather['AirTemp'].mean()
humi = weather['Humidity'].mean()
rain = weather['Rainfall'].mean()

# Add Weather Data
df['circuit_temp'] = temp
df['circuit_humi'] = humi
df['circuit_rain'] = rain

# Load Quali
quali = ff1.get_session(int(num_year), int(num_race), 'Q')
quali.load()
res_Q = quali.results

# Add quali data, and replace the empty values with the last registered time
q_laptime = pd.Series(res_Q['Q3'])
q_laptime = q_laptime.fillna(res_Q['Q2'])
q_laptime = q_laptime.fillna(res_Q['Q1'])

# Transform from datetime64 to total seconds in their quali best laptime
q_laptime = q_laptime.dt.total_seconds()

# Add Quali final position and best laptime
df['quali_pos'] = res_Q['Position']
df['quali_laptime'] = q_laptime

# Add position change from race, considering starting grid position vs final position
df['race_pos_change'] = res.GridPosition - res.Position
df['race_pos'] = res.Position

# Create a list with the race time
race_time1 = []
race_time1 = res.Time.dt.total_seconds()

# Transform each time to a total time for each driver
race_timeF = []
x = 0
race_timeF.append(race_time1[0])

for i in range(1, 20):
    x = race_time1[0] + race_time1[i]
    race_timeF.append(x)

# Add racetime
df['race_time'] = race_timeF
# Replace empty values
df['race_time'] = df['race_time'].fillna(0)

# Fill empty values in final dataset
df = df.fillna(0)

#Print data set
print(df)

#Function to export as a CSV
def ToCSV(data):
    data.to_csv(f'df_{num_year}{coun_name2}.csv', encoding='utf-8')

ToCSV(df)