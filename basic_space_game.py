import pyxel
import random

class Oyun:
    def __init__(self):
        # Oyun penceresi boyutları
        self.genislik = 160
        self.yukseklik = 120
        
        # Oyun değişkenlerini başlat
        self.oyunu_baslat()
        
        # Pyxel başlatma
        pyxel.init(self.genislik, self.yukseklik, title="Uzay Oyunu")
        
        # Sprite'ları oluştur
        self.sprite_olustur()
        
        # Oyun döngüsünü başlat
        pyxel.run(self.guncelle, self.ciz)
    
    def oyunu_baslat(self):
        # Oyuncu gemisi
        self.oyuncu_x = self.genislik // 2
        self.oyuncu_y = self.yukseklik - 20
        self.oyuncu_hiz = 2
        
        # Mermiler
        self.mermiler = []
        
        # Düşmanlar
        self.dusmanlar = []
        self.dusman_olusturma_zamani = 0
        
        # Puan
        self.puan = 0
        
        # Oyun durumu
        self.oyun_aktif = True
    
    def sprite_olustur(self):
        # Oyuncu gemisi sprite'ı
        pyxel.image(0).set(0, 0, [
            "00088000",
            "00888800",
            "08888880",
            "88888888",
            "88888888",
            "88888888",
            "88000088",
            "80000008"
        ])
        
        # Düşman gemisi sprite'ı
        pyxel.image(0).set(8, 0, [
            "00088000",
            "00888800",
            "88888888",
            "88877888",
            "88877888",
            "88888888",
            "08888880",
            "00888800"
        ])
    
    def guncelle(self):
        # Çıkış kontrolü
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        
        if not self.oyun_aktif:
            if pyxel.btnp(pyxel.KEY_R):
                self.oyunu_baslat()
            return
        
        # Oyuncu hareketi
        if pyxel.btn(pyxel.KEY_LEFT) and self.oyuncu_x > 0:
            self.oyuncu_x -= self.oyuncu_hiz
        if pyxel.btn(pyxel.KEY_RIGHT) and self.oyuncu_x < self.genislik - 8:
            self.oyuncu_x += self.oyuncu_hiz
        
        # Ateş etme
        if pyxel.btnp(pyxel.KEY_SPACE):
            self.mermiler.append([self.oyuncu_x + 4, self.oyuncu_y])
        
        # Mermileri güncelleme
        for mermi in self.mermiler[:]:
            mermi[1] -= 4  # Mermi yukarı doğru hareket eder
            if mermi[1] < 0:
                self.mermiler.remove(mermi)
        
        # Düşman oluşturma
        self.dusman_olusturma_zamani += 1
        if self.dusman_olusturma_zamani >= 30:
            self.dusmanlar.append([random.randint(0, self.genislik - 8), 0])
            self.dusman_olusturma_zamani = 0
        
        # Düşmanları güncelleme
        for dusman in self.dusmanlar[:]:
            dusman[1] += 1  # Düşman aşağı doğru hareket eder
            
            # Düşman ekranın altına ulaştı mı?
            if dusman[1] > self.yukseklik:
                self.dusmanlar.remove(dusman)
                continue
            
            # Düşman oyuncuya çarptı mı?
            if (abs(dusman[0] - self.oyuncu_x) < 8 and 
                abs(dusman[1] - self.oyuncu_y) < 8):
                self.oyun_aktif = False
                return
            
            # Düşman mermiye çarptı mı?
            for mermi in self.mermiler[:]:
                if (abs(dusman[0] - mermi[0]) < 8 and 
                    abs(dusman[1] - mermi[1]) < 8):
                    self.dusmanlar.remove(dusman)
                    self.mermiler.remove(mermi)
                    self.puan += 1
                    break
    
    def ciz(self):
        pyxel.cls(0)
        
        if self.oyun_aktif:
            # Oyuncu gemisini çiz
            pyxel.blt(self.oyuncu_x, self.oyuncu_y, 0, 0, 0, 8, 8, 0)
            
            # Mermileri çiz
            for mermi in self.mermiler:
                pyxel.rect(mermi[0], mermi[1], 1, 4, 11)
            
            # Düşmanları çiz
            for dusman in self.dusmanlar:
                pyxel.blt(dusman[0], dusman[1], 0, 8, 0, 8, 8, 0)
            
            # Puanı göster
            pyxel.text(5, 5, f"PUAN: {self.puan}", 7)
        else:
            # Oyun sonu ekranı
            pyxel.text(self.genislik // 2 - 30, self.yukseklik // 2, f"OYUN BITTI! PUAN: {self.puan}", 7)
            pyxel.text(self.genislik // 2 - 40, self.yukseklik // 2 + 10, "TEKRAR BASLAMAK ICIN 'R' TUSUNA BASIN", 7)

# Oyunu başlat
Oyun() 