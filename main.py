# Remarks:
# Git remote respository doesn't contain CVS folders: Mono_BLOS_19_all_in_one-main_ael/ and cemeouhf__ael/ You can find them on Google Drive https://drive.google.com/drive/folders/1VwieRbJuh2ZwxqC4sYGRUO-VsWpSQx9H

import plotly.express as px
import pandas as pd
from pathlib import Path

# Selections:
#terminal_to_satellite_ael = 'Place-POL_Mid-To-Satellite-1s' # 4 satelity konstelacji MEO z próbkowaniem 1s
terminal_to_satellite_ael = 'Place-CEMID-Sensor-Sensor1-To-Satellite-POLMEO' # 12 satelitów MEO konstaleacji Central European

# ael_folder = Path ( 'Mono_BLOS_19_all_in_one-main_ael' )
ael_folder = Path ( 'cemeouhf_ael' )

df = pd.DataFrame ()  # Inicjalizacja głównego DataFrame, który będzie zawierał wszystkie dane

for child in ael_folder.iterdir () :
    if child.is_file () and child.suffix == '.csv' and child.name.startswith ( terminal_to_satellite_ael ) :
        print ( child.name )
        df_ael = pd.read_csv ( child , on_bad_lines = 'skip' , delimiter = ',' )
        df_ael['To satellite'] = child.stem.split('-')[-1].split('_')[0]
        df_ael['From terminal'] = child.stem.split('-')[1].split('-')[0]

        # Convert values, forcing errors to NaN
        df_ael['Time (UTCG)'] = pd.to_datetime ( df_ael['Time (UTCG)'] , errors='coerce' )
        df_ael['Azimuth (deg)'] = pd.to_numeric ( df_ael['Azimuth (deg)'] , errors='coerce' )
        df_ael['Elevation (deg)'] = pd.to_numeric ( df_ael['Elevation (deg)'] , errors='coerce' )
        df_ael['Range (km)'] = pd.to_numeric ( df_ael['Range (km)'] , errors='coerce' )

        # Drop rows where value is NaN
        #df_ael = df_ael.dropna ( subset = ['Time (UTCG)'] )
        #df_ael = df_ael.dropna ( subset = ['Azimuth (deg)'] )
        #df_ael = df_ael.dropna ( subset = ['Elevation (deg)'] )
        #df_ael = df_ael.dropna ( subset = ['Range (km)'] )
        # Usuwanie wierszy z wartościami NaN w interesujących nas kolumnach
        df_ael.dropna ( subset = ['Time (UTCG)' , 'Azimuth (deg)' , 'Elevation (deg)' , 'Range (km)'] , inplace = True )

        # Dodawanie danych z aktualnego pliku do głównego DataFrame
        df = pd.concat ( [df , df_ael] , ignore_index = True )
        # print ( df )      

max_elevation = df['Elevation (deg)'].max ()
# Find the row number where the maximum elevation value is located
max_elevation_row = df[df['Elevation (deg)'] == max_elevation].index[0]
print ( df.loc[df['Elevation (deg)'] == max_elevation] , 'Time (UTCG)' )

#print ( "Maximum Elevation POLMEO1:", max_elevation )
#print ( "Row Number :", max_elevation_row )
#print ( df.head () )

#print ( df.loc[df['Elevation (deg)'] == max_elevation ] )

# print ( df.sort_values ( by = 'Elevation (deg)' , ascending = False ) )

df_filtered = df[ df.groupby ( 'Time (UTCG)' )[ 'Time (UTCG)' ].transform ( 'size' ) > 1 ]
# print ( df_filtered )
# print ( df )
# df.to_csv('results/df.csv', index = false )

# Ustawienie dłuższego wykresu (panoramicznego)
# Filtracja danych dla okresu styczeń 2000
start_date = pd.to_datetime ( '2000-01-01' )
end_date = pd.to_datetime ( '2000-01-31' )
df_january = df[ ( df[ 'Time (UTCG)' ] >= start_date ) & ( df[ 'Time (UTCG)' ] <= end_date ) ]

# Dane tylko dla max elevation
max_elev = df_january[ 'Elevation (deg)' ].max ()
df_max_elev = df_january[ df_january['Elevation (deg)' ] == max_elev ]

# Tworzenie interaktywnego wykresu za pomocą Plotly
fig1 = px.line ( df_january , x = 'Time (UTCG)' , y = 'Elevation (deg)' , color = 'To satellite' , title = 'Elewacja satelitów w styczniu 2000' )
fig1.update_xaxes ( rangeslider_visible = True )
fig1.update_layout ( autosize = True , width = 1200 , height = 600 )
fig1.show ()

fig2 = px.scatter ( df_january , x = 'Time (UTCG)' , y = 'Elevation (deg)' , color = 'To satellite' , title = 'Max elewacja satelitów w styczniu 2000' )
fig2.update_xaxes ( rangeslider_visible = True )
fig2.update_layout ( autosize = True , width = 1200 , height = 600 )
fig2.show ()
