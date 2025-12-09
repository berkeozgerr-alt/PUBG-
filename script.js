const canvas = document.getElementById('game-canvas');
const ctx = canvas.getContext('2d');
let allEntities = {}; // Tüm botların ve oyuncuların güncel durumu

// Haritayı çizmek ve botları konumlandırmak için ana döngü
function drawGame() {
    // 1. Ekranı Temizle
    ctx.fillStyle = '#0a1a0a'; // Harita rengi
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    // 2. Tüm Botları ve Oyuncuları Çiz
    for (const id in allEntities) {
        const entity = allEntities[id];
        
        // Basit çizim: Botları kırmızı, oyuncuyu yeşil kare yapalım
        ctx.fillStyle = id.startsWith('BOT') ? 'red' : 'green';
        
        // Pozisyon ve boyutu ayarla
        ctx.fillRect(entity.x, entity.y, 10, 10);
        
        // HP çubuğunu çiz (PUBG benzeri bir kalite için gerekli)
        ctx.fillStyle = 'white';
        ctx.fillText(entity.hp, entity.x, entity.y - 5);
    }
    
    // Tarayıcının sonraki kareyi çizmesini iste
    requestAnimationFrame(drawGame); 
}

// Sunucudan (Python) gelen verileri alma
socket.on('game_update', (updatedEntities) => {
    // Sunucudan gelen tüm güncel konumları listeye kaydet
    updatedEntities.forEach(entity => {
        allEntities[entity.id] = entity;
    });
});

// Oyunu Başlat
// drawGame(); // İlk çizim döngüsünü başlat
