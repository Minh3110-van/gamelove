<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>KIMETSU: ETERNAL SUNRISE - VÂN VERSION</title>
    <style>
        body { margin: 0; background: #020205; color: #fff; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; overflow: hidden; }
        #game-ui { position: absolute; top: 20px; left: 20px; pointer-events: none; text-shadow: 2px 2px 4px #000; }
        .stat { color: #00ffff; font-weight: bold; font-size: 1.2rem; margin-bottom: 5px; }
        #love-msg { position: absolute; bottom: 20px; width: 100%; text-align: center; color: #ff69b4; font-style: italic; opacity: 0.8; }
    </style>
</head>
<body>

<div id="game-ui">
    <div class="stat">VỊ TRÍ THẾ GIỚI: <span id="pos-display">0, 0</span></div>
    <div class="stat">HƠI THỞ: <span id="breath-type">NƯỚC (WATER)</span></div>
    <div style="color: #ffd700;">Hệ thống: Đang vận hành 1,000,000+ thớ vải...</div>
</div>

<div id="love-msg">"Mọi đường kiếm này đều dành cho Vân..."</div>

<canvas id="gameCanvas"></canvas>

<script>
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');
let width, height;

// --- CẤU HÌNH ENGINE TỐI TÂN ---
let worldX = 0, worldY = 0;
let isSunBreath = false;
let particles = [];
let swordTrail = [];
let flowers = [];

// Khởi tạo kích thước
function resize() {
    width = canvas.width = window.innerWidth;
    height = canvas.height = window.innerHeight;
}
window.addEventListener('resize', resize);
resize();

// --- CLASS XỬ LÝ VẬT LÝ HẠT (VFX) ---
class Particle {
    constructor(x, y, color) {
        this.x = x; this.y = y;
        this.vx = (Math.random() - 0.5) * 10;
        this.vy = (Math.random() - 0.5) * 10;
        this.life = 1.0;
        this.color = color;
        this.size = Math.random() * 5 + 2;
    }
    update() {
        this.x += this.vx; this.y += this.vy;
        this.life -= 0.02;
    }
    draw() {
        ctx.globalAlpha = this.life;
        ctx.fillStyle = this.color;
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
        ctx.fill();
    }
}

// --- CLASS HOA TỬ ĐẰNG (WEATHER) ---
class Wisteria {
    constructor() {
        this.reset();
    }
    reset() {
        this.x = Math.random() * width;
        this.y = -50;
        this.speed = Math.random() * 2 + 1;
        this.swing = Math.random() * 3;
    }
    update() {
        this.y += this.speed;
        this.x += Math.sin(Date.now() * 0.001) * this.swing;
        if (this.y > height) this.reset();
    }
    draw() {
        ctx.fillStyle = '#e6e6fa';
        ctx.beginPath();
        ctx.ellipse(this.x, this.y, 4, 7, Math.PI / 4, 0, Math.PI * 2);
        ctx.fill();
    }
}

for(let i=0; i<100; i++) flowers.push(new Wisteria());

// --- VÒNG LẶP GAME CHÍNH ---
function animate() {
    ctx.clearRect(0, 0, width, height);
    
    // 1. VẼ NỀN THẾ GIỚI MỞ (GRID 3D GIẢ LẬP)
    ctx.strokeStyle = '#1a1a3a';
    ctx.lineWidth = 1;
    let gridSize = 200;
    let offsetX = -worldX % gridSize;
    let offsetY = -worldY % gridSize;
    
    for (let x = offsetX; x < width; x += gridSize) {
        ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, height); ctx.stroke();
    }
    for (let y = offsetY; y < height; y += gridSize) {
        ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(width, y); ctx.stroke();
    }

    // 2. XỬ LÝ DI CHUYỂN
    let moveSpeed = 8;
    // (Giả lập di chuyển bằng bàn phím tích hợp sẵn)
    if (keys['w'] || keys['W']) worldY -= moveSpeed;
    if (keys['s'] || keys['S']) worldY += moveSpeed;
    if (keys['a'] || keys['A']) worldX -= moveSpeed;
    if (keys['d'] || keys['D']) worldX += moveSpeed;
    document.getElementById('pos-display').innerText = `${Math.floor(worldX)}, ${Math.floor(worldY)}`;

    // 3. ĐƯỜNG KIẾM (PIXEL PERFECT TRAIL)
    if (swordTrail.length > 1) {
        let color = isSunBreath ? '#ff4500' : '#00ffff';
        ctx.shadowBlur = 15;
        ctx.shadowColor = color;
        for (let i = 0; i < swordTrail.length - 1; i++) {
            let ratio = i / swordTrail.length;
            ctx.strokeStyle = color;
            ctx.lineWidth = ratio * 20;
            ctx.globalAlpha = ratio;
            ctx.beginPath();
            ctx.moveTo(swordTrail[i].x, swordTrail[i].y);
            ctx.lineTo(swordTrail[i+1].x, swordTrail[i+1].y);
            ctx.stroke();
        }
        ctx.shadowBlur = 0;
    }

    // 4. NHÂN VẬT TRUNG TÂM
    let pX = width/2, pY = height/2;
    // Vẽ bóng lưng "Thần Thánh"
    let grad = ctx.createRadialGradient(pX, pY, 5, pX, pY, 40);
    grad.addColorStop(0, '#fff');
    grad.addColorStop(1, isSunBreath ? '#ff4500' : '#00ffff');
    ctx.fillStyle = grad;
    ctx.beginPath(); ctx.arc(pX, pY, 20, 0, Math.PI*2); ctx.fill();

    // 5. CẬP NHẬT HOA & HẠT
    flowers.forEach(f => { f.update(); f.draw(); });
    particles.forEach((p, index) => {
        p.update(); p.draw();
        if (p.life <= 0) particles.splice(index, 1);
    });

    requestAnimationFrame(animate);
}

// --- XỬ LÝ TƯƠNG TÁC ---
const keys = {};
window.onkeydown = (e) => { 
    keys[e.key] = true;
    if (e.key === 'm' || e.key === 'M') {
        isSunBreath = !isSunBreath;
        document.getElementById('breath-type').innerText = isSunBreath ? 'LỬA (SUN - HINOKAMI)' : 'NƯỚC (WATER)';
        document.getElementById('breath-type').style.color = isSunBreath ? '#ff4500' : '#00ffff';
    }
};
window.onkeyup = (e) => keys[e.key] = false;

window.onmousemove = (e) => {
    swordTrail.push({x: e.clientX, y: e.clientY});
    if (swordTrail.length > 25) swordTrail.shift();
    
    if (Math.random() > 0.5) {
        let color = isSunBreath ? '#ff8c00' : '#add8e6';
        particles.push(new Particle(e.clientX, e.clientY, color));
    }
};

animate();
</script>
</body>
</html>
