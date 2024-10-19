import mysql.connector
import pandas as pd
from datetime import datetime

class Spotify_Proje:
    def __init__(self, db_isim, db_user, db_sifre, db_host="localhost", ilk_defa_giris=False):
        self.db_isim = db_isim
        self.db_user = db_user
        self.db_sifre = db_sifre
        self.db_host = db_host
        self.mydb = None
        self.mycursor = None
        self.ilk_defa_giris = ilk_defa_giris

    def sunucu_baglan(self):
        self.mydb = mysql.connector.connect(
            host=self.db_host,
            user=self.db_user,
            password=self.db_sifre,
        )
        self.mycursor = self.mydb.cursor()

    def database_olustur(self):
        self.mycursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.db_isim}")
        self.mycursor.execute(f"USE {self.db_isim}")

    def table_olustur(self):
        self.mycursor.execute('''
            CREATE TABLE IF NOT EXISTS top_charts (
                id INT PRIMARY KEY AUTO_INCREMENT,
                title VARCHAR(500),
                region VARCHAR(80),
                date DATE,
                position INT
            )
        ''')
        self.mycursor.execute('''
            CREATE TABLE IF NOT EXISTS songs (
                id INT PRIMARY KEY AUTO_INCREMENT,
                title VARCHAR(500),
                artist VARCHAR(255),
                spotify_streams BIGINT,
                youtube_views BIGINT,
                tiktok_views BIGINT
            )
        ''')
        self.mycursor.execute('''
            CREATE TABLE IF NOT EXISTS lyrics (
                id INT PRIMARY KEY AUTO_INCREMENT,
                title VARCHAR(500),
                lyrics TEXT
            )
        ''')

    def csv_veri_aktar(self, csv_dosyasi, tablo_adi):
        """
        Verilen CSV dosyasındaki verileri belirtilen tabloya aktarır.
        """
        df = pd.read_csv(csv_dosyasi, encoding='latin1')

        # Spotify Streams, YouTube Views, TikTok Views için virgülleri temizle
        if 'Spotify Streams' in df.columns:
            df['Spotify Streams'] = df['Spotify Streams'].replace({',': ''}, regex=True).astype(float)  
            df['YouTube Views'] = df['YouTube Views'].replace({',': ''}, regex=True).astype(float)
            df['TikTok Views'] = df['TikTok Views'].replace({',': ''}, regex=True).astype(float)  
        
        # NaN olan hücreleri None yap (MySQL'e NULL olarak aktarılacak)
        df = df.where(pd.notnull(df), None)

        if tablo_adi == 'songs':
            for index, row in df.iterrows():
                sql = '''
                INSERT INTO songs (title, artist, spotify_streams, youtube_views, tiktok_views)
                VALUES (%s, %s, %s, %s, %s)
                '''
                values = (
                    row['Track'], 
                    row['Artist'], 
                    row['Spotify Streams'] if pd.notna(row['Spotify Streams']) else None,
                    row['YouTube Views'] if pd.notna(row['YouTube Views']) else None,
                    row['TikTok Views'] if pd.notna(row['TikTok Views']) else None
                )
                self.mycursor.execute(sql, values)


        elif tablo_adi == 'lyrics':
            for index, row in df.iterrows():
                sql = '''
                INSERT INTO lyrics (title, lyrics)
                VALUES (%s, %s)
                '''
                values = (row['song'], row['text'])
                self.mycursor.execute(sql, values)

        elif tablo_adi == 'top_charts':
            for index, row in df.iterrows():
                # Tarih formatı kontrolü ve dönüşümü
                if row['album_release_date'] is not None:
                    try:
                        row['album_release_date'] = datetime.strptime(row['album_release_date'], '%Y-%m-%d').strftime('%Y-%m-%d')
                    except ValueError:
                        print(f"Tarih formatı hatalı: {row['album_release_date']}")
                        continue
                else:
                    row['album_release_date'] = None  # None olanları doğrudan NULL olarak işaretle

                sql = '''
                INSERT INTO top_charts (title, region, date, position)
                VALUES (%s, %s, %s, %s)
                '''
                values = (row['name'], row['country'], row['album_release_date'], row['daily_rank'])
                self.mycursor.execute(sql, values)

        self.mydb.commit()

    def main(self):
        self.sunucu_baglan()
        self.database_olustur()
        if self.ilk_defa_giris:
            self.table_olustur()

        self.csv_veri_aktar('songs.csv', 'songs')
        self.csv_veri_aktar('lyrics.csv', 'lyrics')
        self.csv_veri_aktar('top_charts.csv', 'top_charts')


if __name__ == "__main__":
    db = Spotify_Proje(db_isim="spotify_proje", db_user="root", db_sifre="VuiZen8395", ilk_defa_giris=True)
    db.main()
