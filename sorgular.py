import mysql.connector
import time
import datetime

class Spotify_Sorgular:
    def __init__(self, db_isim, db_user, db_sifre, db_host="localhost"):
        self.db_isim = db_isim
        self.db_user = db_user
        self.db_sifre = db_sifre
        self.db_host = db_host
        self.mydb = None
        self.mycursor = None

    def sunucu_baglan(self):
        self.mydb = mysql.connector.connect(
            host=self.db_host,
            user=self.db_user,
            password=self.db_sifre,
            database=self.db_isim,
            charset='utf8mb4' 
        )
        self.mycursor = self.mydb.cursor()

    def sarkilarda_sozcuk_sayisi(self, aranan_sozcuk):
        print(f"'{aranan_sozcuk}' geçen şarki sayisi:")
        sql = f"SELECT COUNT(*) FROM lyrics WHERE lyrics LIKE '%{aranan_sozcuk}%'"
        self.mycursor.execute(sql)
        sarki_sayisi = self.mycursor.fetchone()
        print(sarki_sayisi[0])


    def istenen_sozcuk_top_5(self, aranan_sozcuk):
        print("\nEn çok dinlenen 5 şarki ve sözleri:")
        sql = f'''
        SELECT s.title, l.lyrics
        FROM songs s
        JOIN lyrics l ON s.title = l.title
        WHERE l.lyrics LIKE '%{aranan_sozcuk}%'
        ORDER BY s.spotify_streams DESC
        LIMIT 5;
        '''
        self.mycursor.execute(sql)
        results = self.mycursor.fetchall()

        for row in results:
            print(f"Şarki: {row[0]}, Sarki sözleri: \n{row[1]}")


    def top_5_sarki(self):
        print("\nEn çok dinlenen 5 şarki:")
        sql = '''
        SELECT s.title, MAX(s.spotify_streams) AS spotify_streams
        FROM songs s
        GROUP BY s.title
        ORDER BY spotify_streams DESC
        LIMIT 5;
        '''
        self.mycursor.execute(sql)
        results = self.mycursor.fetchall()

        for row in results:
            print(f"Şarki: {row[0]}, Spotify Dinlenme: {row[1]}")

    def kac_tanesi_top_listede(self):
        print("\nEn çok dinlenen 5 şarkidan top listede olan sayisi:")
        sql = '''
        WITH top_songs AS (
            SELECT DISTINCT s.title, s.spotify_streams
            FROM songs s
            ORDER BY s.spotify_streams DESC
            LIMIT 5
        )
        SELECT COUNT(DISTINCT t.title) AS top_listede_olan_sarki_sayisi
        FROM top_songs ts
        JOIN top_charts t ON ts.title = t.title;
        '''
        self.mycursor.execute(sql)
        result = self.mycursor.fetchone()
        print(result[0])

    def sarkilarin_sanatcilari(self):
        print("\nEn çok dinlenen 5 şarkinin sanatçilari:")
        sql = '''
            SELECT s.artist, SUM(s.spotify_streams)
            FROM songs s
            GROUP BY s.artist
            ORDER BY SUM(s.spotify_streams) DESC    
            LIMIT 5
        '''
        self.mycursor.execute(sql)
        results = self.mycursor.fetchall()
        for row in results:
            print(f"Sanatçi: {row[0]}")

    def ulkede_gunluk_top_liste(self, ulke):
        print(f"\n{ulke}'de top listede olan şarkilar ")
        sql = f'''
        SELECT t.title
        FROM top_charts t
        WHERE t.region = '{ulke}'
        GROUP BY t.title
        LIMIT 5;
        '''
        self.mycursor.execute(sql)
        results = self.mycursor.fetchall()
        for row in results:
            print(f"Şarki: {row[0]}")

    def main(self):
        a = time.perf_counter()
        self.sunucu_baglan()

        self.sarkilarda_sozcuk_sayisi('love')
        print()
        self.top_5_sarki()
        print()
        self.kac_tanesi_top_listede()
        print()
        self.istenen_sozcuk_top_5('love')
        print()
        self.sarkilarin_sanatcilari()
        print()
        self.ulkede_gunluk_top_liste('TR')  
        b = time.perf_counter()-a
        print(b)

if __name__ == "__main__":
    db = Spotify_Sorgular(db_isim="spotify_proje", db_user="root", db_sifre="VuiZen8395")
    db.main()
