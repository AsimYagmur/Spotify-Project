# import pandas as pd

# pd.set_option('display.max_columns', None)  
# pd.set_option('display.max_rows', None)     

# # CSV dosyalarının yüklenmesi
# songs_df = pd.read_csv('songs.csv', encoding='latin1')
# top_charts_df = pd.read_csv('top_charts.csv', encoding='latin1')
# lyrics_df = pd.read_csv('lyrics.csv', encoding='latin1')

# print("Songs.csv ilk 5 satır:")
# print(songs_df.head())  

# print("\nTop_charts.csv ilk 5 satır:")
# print(top_charts_df.head())  

# print("\nLyrics.csv ilk 5 satır:")
# print(lyrics_df.head())  

# ##################################################
# import pandas as pd

# CSV dosyalarının yüklenmesi
# songs_df = pd.read_csv('songs.csv', encoding='latin1')
# top_charts_df = pd.read_csv('top_charts.csv', encoding='latin1')
# lyrics_df = pd.read_csv('lyrics.csv', encoding='latin1')

# # Belirli sütunları seçmek için sütun isimlerini liste olarak belirt
# print("Songs.csv belirli sütunlar:")
# print(songs_df[['Track', 'Artist', 'Spotify Streams']].head())  # Sadece 'Track Name', 'Artist' ve 'Streams' sütunlarını görüntüle

# print("\nTop_charts.csv belirli sütunlar:")
# print(top_charts_df[['Track Name', 'Region', 'Position']].head())  # Sadece 'Track Name', 'Region', 'Position' sütunlarını görüntüle

# print("\nLyrics.csv belirli sütunlar:")
# print(lyrics_df[['song', 'text']].head())  # Sadece 'track_id' ve 'lyrics' sütunlarını görüntüle


##################################################


import mysql.connector
import time
from datetime import datetime


# Veritabanına bağlan
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="VuiZen8395"
    
)

mycursor = mydb.cursor(
     
)

mycursor.execute("USE spotify_proje")

mycursor.execute("DROP TABLE IF EXISTS top_charts")

mycursor.execute("DROP TABLE IF EXISTS songs ")

mycursor.execute("DROP TABLE IF EXISTS lyrics")
mydb.commit()



