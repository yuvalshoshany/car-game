// Constants
const WINDOW_WIDTH = 800;
const WINDOW_HEIGHT = 600;
const FPS = 60;

// Colors
const WHITE = '#FFFFFF';
const BLACK = '#000000';
const RED = '#FF0000';
const GREEN = '#00FF00';
const BLUE = '#0000FF';
const GRAY = '#808080';
const DARK_GRAY = '#404040';
const ROAD_GRAY = '#282828';
const YELLOW = '#FFFF00';
const BROWN = '#8B4513';
const PURPLE = '#800080';

// Car dimensions
const CAR_WIDTH = 40;
const CAR_HEIGHT = 80;

// Parking spot dimensions
const PARKING_WIDTH = 60;
const PARKING_HEIGHT = 100;

class Car {
    constructor(x, y) {
        this.x = x;
        this.y = y;
        this.angle = 0;
        this.speed = 0;
        this.acceleration = 0.2;
        this.max_speed = 3;
        this.turn_speed = 2;
        this.width = CAR_WIDTH;
        this.height = CAR_HEIGHT;
        this.friction = 0.95;
        this.velocityX = 0;
        this.velocityY = 0;
    }

    move() {
        // Convert angle to radians
        const rad = this.angle * Math.PI / 180;
        
        // Calculate velocity based on speed and angle
        this.velocityX = Math.sin(rad) * this.speed;
        this.velocityY = -Math.cos(rad) * this.speed;
        
        // Apply velocity to position
        this.x += this.velocityX;
        this.y += this.velocityY;
        
        // Apply friction
        this.speed *= this.friction;
        
        // Keep car within screen bounds
        this.x = Math.max(this.width/2, Math.min(this.x, WINDOW_WIDTH - this.width/2));
        this.y = Math.max(this.height/2, Math.min(this.y, WINDOW_HEIGHT - this.height/2));
    }

    rotate(direction) {
        this.angle += direction * this.turn_speed;
        this.angle %= 360;
    }

    accelerate() {
        this.speed = Math.min(this.speed + this.acceleration, this.max_speed);
    }

    brake() {
        this.speed = Math.max(this.speed - this.acceleration, -this.max_speed/2);
    }

    draw(ctx) {
        ctx.save();
        ctx.translate(this.x, this.y);
        ctx.rotate(this.angle * Math.PI / 180);
        
        // Draw car body
        ctx.fillStyle = BLUE;
        ctx.fillRect(-this.width/2, -this.height/2, this.width, this.height);
        
        // Draw roof
        const roofWidth = this.width * 0.8;
        const roofHeight = this.height * 0.4;
        ctx.fillRect(-roofWidth/2, -this.height/2 + this.height * 0.1, roofWidth, roofHeight);
        
        // Draw windows
        ctx.fillStyle = GRAY;
        const windowWidth = this.width * 0.6;
        const windowHeight = this.height * 0.25;
        ctx.fillRect(-windowWidth/2, -this.height/2 + this.height * 0.15, windowWidth, windowHeight);
        
        // Draw headlights
        ctx.fillStyle = YELLOW;
        const headlightWidth = this.width * 0.15;
        const headlightHeight = this.height * 0.1;
        ctx.fillRect(-this.width/2, -this.height/2, headlightWidth, headlightHeight);
        ctx.fillRect(this.width/2 - headlightWidth, -this.height/2, headlightWidth, headlightHeight);
        
        // Draw wheels
        ctx.fillStyle = BLACK;
        const wheelWidth = this.width * 0.25;
        const wheelHeight = this.height * 0.2;
        ctx.fillRect(-this.width/2, -this.height/2, wheelWidth, wheelHeight);
        ctx.fillRect(this.width/2 - wheelWidth, -this.height/2, wheelWidth, wheelHeight);
        ctx.fillRect(-this.width/2, this.height/2 - wheelHeight, wheelWidth, wheelHeight);
        ctx.fillRect(this.width/2 - wheelWidth, this.height/2 - wheelHeight, wheelWidth, wheelHeight);
        
        // Draw wheel rims
        ctx.fillStyle = GRAY;
        const rimWidth = wheelWidth * 0.6;
        const rimHeight = wheelHeight * 0.6;
        ctx.fillRect(-this.width/2 + wheelWidth * 0.2, -this.height/2 + wheelHeight * 0.2, rimWidth, rimHeight);
        ctx.fillRect(this.width/2 - wheelWidth + wheelWidth * 0.2, -this.height/2 + wheelHeight * 0.2, rimWidth, rimHeight);
        ctx.fillRect(-this.width/2 + wheelWidth * 0.2, this.height/2 - wheelHeight + wheelHeight * 0.2, rimWidth, rimHeight);
        ctx.fillRect(this.width/2 - wheelWidth + wheelWidth * 0.2, this.height/2 - wheelHeight + wheelHeight * 0.2, rimWidth, rimHeight);
        
        ctx.restore();
    }

    getRect() {
        return {
            x: this.x - this.width/2,
            y: this.y - this.height/2,
            width: this.width,
            height: this.height
        };
    }
}

class ObstacleCar {
    constructor(x, y, color) {
        this.x = x;
        this.y = y;
        this.color = color;
        this.width = CAR_HEIGHT;
        this.height = CAR_WIDTH;
        this.speed = Math.random() * 2 + 2;
        this.direction = 1;
    }

    move() {
        this.x += this.speed * this.direction;
        if (this.x <= 50 || this.x >= WINDOW_WIDTH - this.width - 50) {
            this.direction *= -1;
            this.x = Math.max(50, Math.min(this.x, WINDOW_WIDTH - this.width - 50));
        }
    }

    draw(ctx) {
        // Draw car body
        ctx.fillStyle = this.color;
        ctx.fillRect(this.x, this.y, this.width, this.height);
        
        // Draw roof
        const roofWidth = this.width * 0.4;
        const roofHeight = this.height * 0.8;
        ctx.fillRect(this.x + this.width * 0.1, this.y + (this.height - roofHeight) / 2, roofWidth, roofHeight);
        
        // Draw windows
        ctx.fillStyle = GRAY;
        const windowWidth = this.width * 0.25;
        const windowHeight = this.height * 0.6;
        ctx.fillRect(this.x + this.width * 0.15, this.y + (this.height - windowHeight) / 2, windowWidth, windowHeight);
        
        // Draw headlights
        ctx.fillStyle = YELLOW;
        const headlightWidth = this.height * 0.15;
        const headlightHeight = this.height * 0.1;
        ctx.fillRect(this.x, this.y + (this.height - headlightHeight) / 2, headlightWidth, headlightHeight);
        ctx.fillRect(this.x + this.width - headlightWidth, this.y + (this.height - headlightHeight) / 2, headlightWidth, headlightHeight);
        
        // Draw wheels
        ctx.fillStyle = BLACK;
        const wheelWidth = this.height * 0.25;
        const wheelHeight = this.height * 0.2;
        ctx.fillRect(this.x, this.y, wheelWidth, wheelHeight);
        ctx.fillRect(this.x, this.y + this.height - wheelHeight, wheelWidth, wheelHeight);
        ctx.fillRect(this.x + this.width - wheelWidth, this.y, wheelWidth, wheelHeight);
        ctx.fillRect(this.x + this.width - wheelWidth, this.y + this.height - wheelHeight, wheelWidth, wheelHeight);
        
        // Draw wheel rims
        ctx.fillStyle = GRAY;
        const rimWidth = wheelWidth * 0.6;
        const rimHeight = wheelHeight * 0.6;
        ctx.fillRect(this.x + wheelWidth * 0.2, this.y + wheelHeight * 0.2, rimWidth, rimHeight);
        ctx.fillRect(this.x + wheelWidth * 0.2, this.y + this.height - wheelHeight + wheelHeight * 0.2, rimWidth, rimHeight);
        ctx.fillRect(this.x + this.width - wheelWidth + wheelWidth * 0.2, this.y + wheelHeight * 0.2, rimWidth, rimHeight);
        ctx.fillRect(this.x + this.width - wheelWidth + wheelWidth * 0.2, this.y + this.height - wheelHeight + wheelHeight * 0.2, rimWidth, rimHeight);
    }

    getRect() {
        return {
            x: this.x,
            y: this.y,
            width: this.width,
            height: this.height
        };
    }
}

class Game {
    constructor() {
        this.canvas = document.getElementById('gameCanvas');
        this.ctx = this.canvas.getContext('2d');
        this.score = 0;
        this.gameOver = false;
        this.keys = {};
        
        this.resetGame();
        this.setupEventListeners();
        this.gameLoop();
    }

    resetGame() {
        this.car = new Car(WINDOW_WIDTH / 2, WINDOW_HEIGHT - 100);
        this.parkingSpot = {
            x: WINDOW_WIDTH / 2 - PARKING_WIDTH / 2,
            y: 50,
            width: PARKING_WIDTH,
            height: PARKING_HEIGHT
        };
        this.obstacles = [];
        this.generateObstacles();
        this.gameOver = false;
        document.getElementById('game-over').style.display = 'none';
    }

    generateObstacles() {
        const obstacleColors = [BROWN, YELLOW, GREEN, PURPLE];
        for (let i = 0; i < 3 + Math.floor(Math.random() * 2); i++) {
            let attempts = 0;
            while (attempts < 100) {
                const x = Math.random() * (WINDOW_WIDTH - CAR_HEIGHT - 200) + 100;
                const y = Math.random() * (WINDOW_HEIGHT - 250) + 150;
                const color = obstacleColors[Math.floor(Math.random() * obstacleColors.length)];
                const obstacle = new ObstacleCar(x, y, color);
                
                if (!this.checkCollision(obstacle.getRect(), this.parkingSpot)) {
                    const carRect = this.car.getRect();
                    if (!this.checkCollision(obstacle.getRect(), carRect)) {
                        let overlap = false;
                        for (const existingObstacle of this.obstacles) {
                            if (this.checkCollision(obstacle.getRect(), existingObstacle.getRect())) {
                                overlap = true;
                                break;
                            }
                        }
                        if (!overlap) {
                            this.obstacles.push(obstacle);
                            break;
                        }
                    }
                }
                attempts++;
            }
        }
    }

    checkCollision(rect1, rect2) {
        return rect1.x < rect2.x + rect2.width &&
               rect1.x + rect1.width > rect2.x &&
               rect1.y < rect2.y + rect2.height &&
               rect1.y + rect1.height > rect2.y;
    }

    setupEventListeners() {
        window.addEventListener('keydown', (e) => this.keys[e.key] = true);
        window.addEventListener('keyup', (e) => this.keys[e.key] = false);
    }

    handleInput() {
        // Support both WASD and arrow keys
        if (this.keys['ArrowLeft'] || this.keys['a']) this.car.rotate(-1);
        if (this.keys['ArrowRight'] || this.keys['d']) this.car.rotate(1);
        if (this.keys['ArrowUp'] || this.keys['w']) this.car.accelerate();
        if (this.keys['ArrowDown'] || this.keys['s']) this.car.brake();
        if (this.keys['r'] && this.gameOver) {
            this.score = 0;
            this.resetGame();
        }
    }

    update() {
        if (this.gameOver) return;

        this.car.move();
        for (const obstacle of this.obstacles) {
            obstacle.move();
        }

        // Check collisions
        const carRect = this.car.getRect();
        
        // Check collision with obstacles
        for (const obstacle of this.obstacles) {
            if (this.checkCollision(carRect, obstacle.getRect())) {
                this.gameOver = true;
                document.getElementById('game-over').style.display = 'block';
                return;
            }
        }

        // Check if car is parked correctly
        if (this.checkCollision(carRect, this.parkingSpot)) {
            if (Math.abs(this.car.angle) < 10 || Math.abs(this.car.angle - 360) < 10) {
                this.score++;
                document.getElementById('score').textContent = `Score: ${this.score}`;
                this.resetGame();
            }
        }
    }

    draw() {
        // Clear canvas
        this.ctx.fillStyle = ROAD_GRAY;
        this.ctx.fillRect(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT);
        
        // Draw road lines
        this.ctx.strokeStyle = WHITE;
        this.ctx.lineWidth = 3;
        const roadDashLength = 30;
        const roadDashSpace = 40;
        for (let i = 0; i < WINDOW_WIDTH; i += roadDashLength + roadDashSpace) {
            this.ctx.beginPath();
            this.ctx.moveTo(i, WINDOW_HEIGHT / 2);
            this.ctx.lineTo(Math.min(i + roadDashLength, WINDOW_WIDTH), WINDOW_HEIGHT / 2);
            this.ctx.stroke();
        }
        
        // Draw side lines
        this.ctx.lineWidth = 5;
        this.ctx.beginPath();
        this.ctx.moveTo(0, 0);
        this.ctx.lineTo(0, WINDOW_HEIGHT);
        this.ctx.moveTo(WINDOW_WIDTH, 0);
        this.ctx.lineTo(WINDOW_WIDTH, WINDOW_HEIGHT);
        this.ctx.stroke();
        
        // Draw parking spot
        this.ctx.strokeStyle = GREEN;
        this.ctx.lineWidth = 2;
        this.ctx.strokeRect(this.parkingSpot.x, this.parkingSpot.y, this.parkingSpot.width, this.parkingSpot.height);
        
        // Draw dashed lines for parking spot
        const parkingDashLength = 10;
        const parkingDashSpace = 5;
        for (let i = 0; i < this.parkingSpot.width; i += parkingDashLength + parkingDashSpace) {
            this.ctx.beginPath();
            this.ctx.moveTo(this.parkingSpot.x + i, this.parkingSpot.y);
            this.ctx.lineTo(this.parkingSpot.x + Math.min(i + parkingDashLength, this.parkingSpot.width), this.parkingSpot.y);
            this.ctx.stroke();
        }
        
        // Draw obstacles
        for (const obstacle of this.obstacles) {
            obstacle.draw(this.ctx);
        }
        
        // Draw car
        this.car.draw(this.ctx);
    }

    gameLoop() {
        this.handleInput();
        this.update();
        this.draw();
        requestAnimationFrame(() => this.gameLoop());
    }
}

// Start the game when the page loads
window.onload = () => {
    new Game();
}; 