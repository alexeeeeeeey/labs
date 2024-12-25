// Получаем доступ к canvas и его контексту
const canvas = document.createElement('canvas');
const ctx = canvas.getContext('2d');
document.body.appendChild(canvas);
canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

// Переменные для игрока и врагов
const player = {
  x: canvas.width / 2,
  y: canvas.height - 50,
  width: 30,
  height: 30,
  color: 'blue',
  speed: 5,
  alive: true
};

const enemies = [];
const bullets = [];
let score = 0;
let enemySpawnRate = 1000;
let lastSpawnTime = 0;
let bulletSpeed = 7;
let bulletCooldown = 500;
let lastBulletTime = 0;
let konamiActivated = false;

// Конами-код
const konamiCode = [
  'ArrowUp', 'ArrowUp', 'ArrowDown', 'ArrowDown',
  'ArrowLeft', 'ArrowRight', 'ArrowLeft', 'ArrowRight',
  'KeyB', 'KeyA'
];
let konamiIndex = 0;

document.addEventListener('keydown', (key) => {
  if (key.code === konamiCode[konamiIndex]) {
    konamiIndex++;
    if (konamiIndex === konamiCode.length) {
      activateKonami();
      konamiIndex = 0;
    }
  } else {
    konamiIndex = 0;
  }
});

function activateKonami() {
    if (konamiActivated) return;
    konamiActivated = true;
    bulletSpeed = 10;
    bulletCooldown = 0;
    enemySpawnRate = 0;
    player.speed = 20;
    console.log('Konami code activated!');
}

// Создаем врагов
function spawnEnemy() {
  const enemy = {
    x: Math.random() * (canvas.width - 30),
    y: -30,
    width: 30,
    height: 30,
    color: 'red',
    speed: Math.random() * 2 + 1 + score * 0.05
  };
  enemies.push(enemy);
}

// Рисование элементов
function drawRect(obj) {
  ctx.fillStyle = obj.color;
  ctx.fillRect(obj.x, obj.y, obj.width, obj.height);
}

// Управление игроком
const keys = {};
document.addEventListener('keydown', (key) => keys[key.code] = true);
document.addEventListener('keyup', (key) => keys[key.code] = false);

function movePlayer() {
  if (!player.alive) return;
  if (keys['ArrowLeft'] && player.x > 0) player.x -= player.speed;
  if (keys['ArrowRight'] && player.x + player.width < canvas.width) player.x += player.speed;
  if (keys['Space']) shoot();
}

// Стрельба
function shoot() {
  if (!player.alive) return;
  const now = performance.now();
  if (now - lastBulletTime < bulletCooldown) return;
  lastBulletTime = now;

  const bullet = {
    x: player.x + player.width / 2 - 5,
    y: player.y,
    width: 5,
    height: 10,
    color: 'yellow',
    speed: bulletSpeed
  };
  bullets.push(bullet);
}

// Обновление положения врагов и пуль
function updateEnemies() {
  for (let i = enemies.length - 1; i >= 0; i--) {
    enemies[i].y += enemies[i].speed;

    // Проверка столкновения с игроком
    if (
      enemies[i].x < player.x + player.width &&
      enemies[i].x + enemies[i].width > player.x &&
      enemies[i].y < player.y + player.height &&
      enemies[i].y + enemies[i].height > player.y
    ) {
      player.alive = false;
    }

    if (enemies[i].y > canvas.height) {
      enemies.splice(i, 1);
      if (!konamiActivated)
        score--;
    }
  }
}

function updateBullets() {
  for (let i = bullets.length - 1; i >= 0; i--) {
    bullets[i].y -= bullets[i].speed;
    if (bullets[i].y + bullets[i].height < 0) {
      bullets.splice(i, 1);
    }
  }
}

// Проверка столкновений
function checkCollisions() {
  for (let i = enemies.length - 1; i >= 0; i--) {
    for (let j = bullets.length - 1; j >= 0; j--) {
      if (
        bullets[j].x < enemies[i].x + enemies[i].width &&
        bullets[j].x + bullets[j].width > enemies[i].x &&
        bullets[j].y < enemies[i].y + enemies[i].height &&
        bullets[j].y + bullets[j].height > enemies[i].y
      ) {
        enemies.splice(i, 1);
        bullets.splice(j, 1);
        score++;
        break;
      }
    }
  }
}

// Игровой цикл
function gameLoop(timestamp) {
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  if (!player.alive || score < 0) {
    ctx.fillStyle = 'white';
    ctx.font = '40px Arial';
    ctx.fillText('Game Over!', canvas.width / 2 - 100, canvas.height / 2);
    ctx.font = '20px Arial';
    ctx.fillText(`Final Score: ${score}`, canvas.width / 2 - 70, canvas.height / 2 + 40);
    return;
  }

  // Увеличение сложности
  if (timestamp - lastSpawnTime > enemySpawnRate) {
    spawnEnemy();
    lastSpawnTime = timestamp;
  }

  // Движение и рисование
  movePlayer();
  updateEnemies();
  updateBullets();
  checkCollisions();

  drawRect(player);
  enemies.forEach(drawRect);
  bullets.forEach(drawRect);

  // Отображение счета
  ctx.fillStyle = 'white';
  ctx.font = '20px Arial';
  ctx.fillText(`Score: ${score}`, 10, 30);

  requestAnimationFrame(gameLoop);
}

// Запуск игры
gameLoop();