class DersBilgisi:
    def __init__(self, ders_adi, ders_agirlik, vize_notu=0, final_notu=0):
        self.ders_adi = ders_adi
        self.ders_agirlik = ders_agirlik
        self.vize_notu = vize_notu
        self.final_notu = final_notu
        self.ders_ortalama = (vize_notu * 0.4) + (final_notu * 0.6)
        self.gecme_durumu = self.hesapla_gecti(self.ders_ortalama)

    @staticmethod
    def hesapla_can_sistemi(dersler):
        toplam_ortalama = sum(ders.ders_ortalama for ders in dersler)
        ogrenci_sayisi = len(dersler)
        return toplam_ortalama / ogrenci_sayisi if ogrenci_sayisi > 0 else 0

    def hesapla_gecti(self, ders_can_sistemi_ortalamasi):
        return self.ders_ortalama >= 30 and self.final_notu >= 40 and self.ders_ortalama >= ders_can_sistemi_ortalamasi

    def gecme_durumu_metni(self, ders_can_sistemi_ortalamasi):
        return "Geçti" if self.hesapla_gecti(ders_can_sistemi_ortalamasi) else "Kaldı"


class Ogrenci:
    def __init__(self, ad, soyad, ders_bilgileri):
        self.ad = ad
        self.soyad = soyad
        self.ders_bilgileri = ders_bilgileri
        self.gano = self.hesapla_gano()

    def hesapla_gano(self):
        toplam_agirlikli_not = 0
        toplam_ders_agirlik = 0

        for ders in self.ders_bilgileri:
            toplam_agirlikli_not += ders.ders_agirlik * ders.ders_ortalama
            toplam_ders_agirlik += ders.ders_agirlik

        return (toplam_agirlikli_not / toplam_ders_agirlik) / 4 if toplam_ders_agirlik > 0 else 0


class Dugum:
    def __init__(self, veri):
        self.veri = veri
        self.sonraki = None


class OgrenciListesi:
    def __init__(self):
        self.bas = None
        self.ders_bilgileri = []

    def ogrenci_ekle(self, ad, soyad):
        ogrenci_ders_bilgileri = []
        for ders in self.ders_bilgileri:
            vize_notu = float(input(f"{ders.ders_adi} Vize Notu: "))
            final_notu = float(input(f"{ders.ders_adi} Final Notu: "))
            ogrenci_ders_bilgileri.append(DersBilgisi(ders.ders_adi, ders.ders_agirlik, vize_notu, final_notu))

        yeni_ogrenci = Ogrenci(ad, soyad, ogrenci_ders_bilgileri)
        yeni_dugum = Dugum(yeni_ogrenci)
        yeni_dugum.sonraki = self.bas
        self.bas = yeni_dugum

    def ogrenci_sil(self, silinecek_ad, silinecek_soyad):
        current = self.bas
        onceki = None

        while current:
            if current.veri.ad == silinecek_ad and current.veri.soyad == silinecek_soyad:
                if onceki:
                    onceki.sonraki = current.sonraki
                else:
                    self.bas = current.sonraki
                print(f"{silinecek_ad} {silinecek_soyad} adlı öğrenci silindi.")
                self.guncelle()  # Güncelleme metodu çağrıldı
                break
            onceki = current
            current = current.sonraki

    def ogrencileri_listele(self):
        current = self.bas
        ders_can_sistemi_ortalamasi = self.hesapla_can_sistemi(self.ders_bilgileri)
        while current:
            print(f"Ad: {current.veri.ad}, Soyad: {current.veri.soyad}")
            for ders in current.veri.ders_bilgileri:
                print(
                    f"  {ders.ders_adi}:Vize: {ders.vize_notu}, Final: {ders.final_notu}, Ortalama: {ders.ders_ortalama}, Geçme Durumu: {ders.gecme_durumu_metni(ders_can_sistemi_ortalamasi)}")
            current = current.sonraki

    def hesapla_can_sistemi(self, ders_bilgileri):
        toplam_ortalama = sum(ders.ders_ortalama for ders in ders_bilgileri)
        ogrenci_sayisi = len(ders_bilgileri)
        return toplam_ortalama / ogrenci_sayisi if ogrenci_sayisi > 0 else 0
    def guncelle(self):
        ders_can_sistemi_ortalamasi = self.hesapla_can_sistemi(self.ders_bilgileri)
        current = self.bas
        while current:
            for ders in current.veri.ders_bilgileri:
                ders.ders_ortalama = (ders.vize_notu * 0.4) + (ders.final_notu * 0.6)
                ders.gecme_durumu = ders.hesapla_gecti(ders_can_sistemi_ortalamasi)
            current = current.sonraki


# Ana uygulama döngüsü
ogrenci_listesi = OgrenciListesi()

ders_bilgileri = [
    DersBilgisi("veri_yapıları", 5),
    DersBilgisi("elektrik", 3),
    DersBilgisi("ayrık_matematik", 4),
    DersBilgisi("object_oriented_programming", 6),
    DersBilgisi("yöneylem", 5),
    DersBilgisi("mantık_devreleri", 5)
]

ogrenci_listesi.ders_bilgileri = ders_bilgileri  # Ders bilgilerini liste üzerinde saklayın

while True:
    print("\n1. Öğrenci Ekle")
    print("2. Öğrenci Sil")
    print("3. Öğrenci Bilgisi Görüntüle")
    print("4. Çıkış")

    secim = input("Yapmak istediğiniz işlemi seçin (1-4): ")

    if secim == "1":
        ad = input("Öğrenci Adı: ")
        soyad = input("Öğrenci Soyadı: ")
        ogrenci_listesi.ogrenci_ekle(ad, soyad)
    elif secim == "2":
        ad = input("Silinecek Öğrenci Adı: ")
        soyad = input("Silinecek Öğrenci Soyadı: ")
        ogrenci_listesi.ogrenci_sil(ad, soyad)
    elif secim == "3":
        ogrenci_listesi.ogrencileri_listele()
    elif secim == "4":
        print("Programdan çıkılıyor.")
        break
    else:
        print("Geçersiz seçenek. Lütfen tekrar deneyin.")
