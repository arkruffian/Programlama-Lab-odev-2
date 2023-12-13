import csv

class TIR:
    def __init__(self, plaka, ulke, konteyner_20, konteyner_30, yuk_miktari, yuk_maliyeti):
        self.plaka = plaka
        self.ulke = ulke
        self.konteyner_20 = konteyner_20
        self.konteyner_30 = konteyner_30
        self.yuk_miktari = yuk_miktari
        self.yuk_maliyeti = yuk_maliyeti

    def yukleri_indir(self):
        if self.konteyner_20 > 0:
            print(f"{self.plaka} plakalı TIR'dan 20 tonluk konteynerler indiriliyor...")
            self.konteyner_20 = 0
        if self.konteyner_30 > 0:
            print(f"{self.plaka} plakalı TIR'dan 30 tonluk konteynerler indiriliyor...")
            self.konteyner_30 = 0

class Gemi:
    def __init__(self, gemi_adi, kapasite, gidecek_ulke):
        self.gemi_adi = gemi_adi
        self.kapasite = kapasite
        self.gidecek_ulke = gidecek_ulke
        self.yuk_miktari = 0

    def yukleri_yukle(self, yuk):
        if self.yuk_miktari + yuk <= self.kapasite:
            self.yuk_miktari += yuk
            print(f"{yuk} ton yük gemiye yüklendi.")
        else:
            print(f"Gemi kapasitesi aşıldı, {yuk} ton yük yüklenemedi.")

class Liman:
    def __init__(self):
        self.tir_listesi = []
        self.gemi_listesi = []
        self.istif_alani_1 = []
        self.istif_alani_2 = []
        self.vinc_islemleri = 0

    def olaylar_csv_oku(self, dosya_adı):
        try:
            with open(dosya_adı, 'r', newline='') as dosya:
                csv_okuyucu = csv.reader(dosya)
                next(csv_okuyucu)
                for satir in csv_okuyucu:
                    geliş_zamanı = satir[0]
                    tır_plakası = satir[1]
                    ülke = satir[2]  # Burada ülke adı olduğunu varsayalım
                    konteyner_20 = int(satir[3])
                    konteyner_30 = int(satir[4])
                    yuk_miktari = int(satir[5])
                    maliyet = float(satir[6])

                    yeni_tir = TIR(tır_plakası, ülke, konteyner_20, konteyner_30, yuk_miktari, maliyet)
                    self.tir_listesi.append(yeni_tir)

        except FileNotFoundError:
            print(f"{dosya_adı} bulunamadı!")

    def gemiler_csv_oku(self, dosya_adı):
        try:
            with open(dosya_adı, 'r', newline='') as dosya:
                csv_okuyucu = csv.reader(dosya)
                next(csv_okuyucu) 
                for satir in csv_okuyucu:
                    gemi_adı = satir[0]
                    kapasite = int(satir[1])
                    gidecek_ulke = satir[2]

                    yeni_gemi = Gemi(gemi_adı, kapasite, gidecek_ulke)
                    self.gemi_listesi.append(yeni_gemi)

        except FileNotFoundError:
            print(f"{dosya_adı} bulunamadı!")

    def liman_islemleri(self):
        for anlik_zaman in range(0, 100):  
            for tir in self.tir_listesi:
                tir.yukleri_indir()  
            for gemi in self.gemi_listesi:
                self.gemiye_yukle(gemi, 50)  
            self.vinc_islemleri = 0  
            self.vinc_islemleri_gerceklestir()  

    def vinc_islemleri_gerceklestir(self):
        while self.vinc_islemleri < 20:  
            if self.istif_alani_1 or self.istif_alani_2:  
                self.vinc_islemleri += 1  
                self.yuk_transferi()  
            else:
                print("İstif alanları boş, işlem tamamlandı.")
                break

    def yuk_transferi(self):
        if self.istif_alani_1:  
            yuk = self.istif_alani_1.pop()  
            print(f"Yük {yuk} istif alanından kaldırıldı ve gemiye yüklendi.")
          
        elif self.istif_alani_2:  
            yuk = self.istif_alani_2.pop()  
            print(f"Yük {yuk} istif alanından kaldırıldı ve gemiye yüklendi.")
            

    def gemiye_yukle(self, gemi, yuk):
        if gemi.yuk_miktari + yuk <= gemi.kapasite:
            gemi.yukleri_yukle(yuk)
        else:
            print(f"Yük {yuk} yüklenecek uygun gemi bulunamadı.")

if __name__ == "__main__":
    liman = Liman()

    liman.olaylar_csv_oku('olaylar.csv')
    liman.gemiler_csv_oku('gemiler.csv')

    liman.liman_islemleri()
