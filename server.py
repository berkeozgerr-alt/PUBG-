# Savaş Alanı Ayarları
ARENA_WIDTH = 1000
ARENA_HEIGHT = 1000

# Oyuncular ve Botlar
players = {} # İnsan oyuncular
bots = {}    # 100 Botun tamamı

# Bot Sınıfı: Her bir botun durumunu tutar
class Bot:
    def __init__(self, bot_id, x, y):
        self.id = bot_id
        self.x = x
        self.y = y
        self.hp = 100
        self.target = None # Hedef (başka bir oyuncu/bot)
        self.speed = 2
        
    def think_and_move(self, players, bots):
        """Botun yapay zeka mantığı: Hareket edecek, hedef seçecek ve ateş edecek."""
        
        # 1. Hedef Belirleme (En yakın düşmanı seç)
        if self.target is None or self.target not in players and self.target not in bots:
            # Yeni en yakın hedefi bulma mantığı buraya gelir
            pass 
        
        # 2. Hareketi Hesaplama (Hedefe doğru ilerleme)
        # Basitçe hedefe doğru X ve Y koordinatlarını değiştirir.
        if self.target:
             target_obj = players.get(self.target) or bots.get(self.target)
             if target_obj:
                 # Basit takip kodu
                 if self.x < target_obj.x: self.x += self.speed
                 if self.x > target_obj.x: self.x -= self.speed
                 if self.y < target_obj.y: self.y += self.speed
                 if self.y > target_obj.y: self.y -= self.speed

        # 3. Sınırları Kontrol Etme
        self.x = max(0, min(self.x, ARENA_WIDTH))
        self.y = max(0, min(self.y, ARENA_HEIGHT))
        
        # 4. Ateş Etme (Çok yakınsa ateş eder)
        # Bu kısım çarpışma tespiti ve mermi yönetimi gerektirir.
        
        return {'id': self.id, 'x': self.x, 'y': self.y, 'hp': self.hp}


# Botları Başlatma İşlevi
def initialize_bots():
    for i in range(1, 101):
        bot_id = f"BOT_{i}"
        # Botları haritanın rastgele bir yerine koy
        bots[bot_id] = Bot(bot_id, random.randint(0, ARENA_WIDTH), random.randint(0, ARENA_HEIGHT))

# --- ANA SİMÜLASYON DÖNGÜSÜ ---
# Simülasyonu 20 FPS hızında çalıştırmak için Python'da Threading kullanılır.

@socketio.on('start_simulation')
def start_simulation_thread():
    initialize_bots()
    # Bu döngü, arka planda sürekli çalışmalıdır
    while True:
        updated_bots_data = []
        for bot in bots.values():
            # Her botun düşünmesini ve hareket etmesini sağla
            updated_data = bot.think_and_move(players, bots)
            updated_bots_data.append(updated_data)
            
        # Tüm istemcilere güncel pozisyonları gönder (Yayma/Broadcast)
        socketio.emit('game_update', updated_bots_data, broadcast=True)
        
        time.sleep(1/20) # Saniyede 20 kez güncelleme (50ms bekleme)
