
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="12.12 : 국회 탈출",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
.stApp {
    background: #10131a;
    color: #f1f1f1;
}
header, footer {
    visibility: hidden;
}
.block-container {
    padding-top: 1rem;
    padding-bottom: 0rem;
    max-width: 1100px;
}
h1 {
    text-align: center;
    color: #e8d7b0;
}
</style>
""", unsafe_allow_html=True)

st.markdown(
    "<h1>12.12 : 국회 탈출</h1>",
    unsafe_allow_html=True
)

st.markdown(
    "<p style='text-align:center;color:#b7bdc8;'>"
    "김대중 캐릭터가 전두환 얼굴 장애물을 피해 살아남는 "
    "역사 풍자 아케이드 게임"
    "</p>",
    unsafe_allow_html=True
)

game_html = r"""
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">

<style>
* {
    box-sizing: border-box;
}

body {
    margin: 0;
    background: #10131a;
    color: white;
    font-family: Arial, sans-serif;
    overflow: hidden;
}

#game-wrapper {
    width: 100%;
    max-width: 1000px;
    margin: auto;
}

canvas {
    width: 100%;
    height: auto;
    display: block;
    border: 2px solid #4b5363;
    border-radius: 8px;
    background: #222;
}

#info {
    display: flex;
    justify-content: space-between;
    padding: 10px 4px;
    font-size: 16px;
    font-weight: bold;
}

#controls {
    display: flex;
    justify-content: center;
    gap: 12px;
    margin-top: 12px;
}

.control-btn {
    width: 75px;
    height: 55px;
    background: #293344;
    color: white;
    border: 1px solid #68758a;
    border-radius: 10px;
    font-size: 24px;
    touch-action: none;
}

.control-btn:active {
    background: #536783;
}

#canvas-container {
    position: relative;
}

#start-screen {
    position: absolute;
    inset: 0;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    background: rgba(10, 15, 25, 0.88);
    text-align: center;
    z-index: 5;
    padding: 15px;
}

#start-screen h2 {
    color: #e8d7b0;
    font-size: 32px;
}

#start-screen p {
    line-height: 1.8;
}

#start-screen button {
    padding: 13px 30px;
    border: none;
    border-radius: 8px;
    background: #b94b42;
    color: white;
    font-size: 18px;
    font-weight: bold;
    cursor: pointer;
}

@media (max-width: 600px) {
    #info {
        font-size: 12px;
    }

    .control-btn {
        width: 65px;
        height: 50px;
    }
}
</style>
</head>

<body>

<div id="game-wrapper">

    <div id="info">
        <span>🏛️ 국회 탈출</span>
        <span id="score">점수: 0</span>
        <span id="best">최고 기록: 0</span>
    </div>

    <div id="canvas-container">

        <canvas id="game" width="900" height="500"></canvas>

        <div id="start-screen">

            <h2 id="screen-title">
                12.12 : 국회 탈출
            </h2>

            <p id="screen-description">
                김대중 캐릭터를 조작해<br>
                전두환 얼굴 장애물을 피해라!<br><br>
                ← → : 이동<br>
                SPACE / ↑ : 점프<br>
                모바일 : 아래 버튼으로 조작
            </p>

            <button id="start-button" onclick="startGame()">
                게임 시작
            </button>

        </div>

    </div>

    <div id="controls">
        <button class="control-btn" id="left">←</button>
        <button class="control-btn" id="jump">↑</button>
        <button class="control-btn" id="right">→</button>
    </div>

</div>

<script>
const canvas = document.getElementById("game");
const ctx = canvas.getContext("2d");

const W = canvas.width;
const H = canvas.height;

const GROUND = 410;

// Wikimedia Commons 이미지
const KIM_IMAGE_URL =
"https://upload.wikimedia.org/wikipedia/commons/thumb/d/d2/Kim_Dae-jung_presidential_portrait.jpg/500px-Kim_Dae-jung_presidential_portrait.jpg";

const CHUN_IMAGE_URL =
"https://upload.wikimedia.org/wikipedia/commons/8/85/Chun_Doo-hwan_%28%EC%A0%84%EB%91%90%ED%99%98%29_Presidential_Portrait_%28cropped%29.jpg";

const kimImage = new Image();
const chunImage = new Image();

kimImage.crossOrigin = "anonymous";
chunImage.crossOrigin = "anonymous";

kimImage.src = KIM_IMAGE_URL;
chunImage.src = CHUN_IMAGE_URL;

let running = false;
let gameOver = false;

let score = 0;
let best = 0;
let frame = 0;

let tankSpeed = 4;
let obstacles = [];

const player = {
    x: 130,
    y: GROUND - 66,
    w: 66,
    h: 66,
    vx: 0,
    vy: 0,
    speed: 5,
    gravity: 0.65,
    jumpPower: -13,
    onGround: true
};

const keys = {
    left: false,
    right: false,
    jump: false
};


// 원형 이미지 그리기
function drawCircularImage(image, x, y, size) {

    ctx.save();

    ctx.beginPath();

    ctx.arc(
        x + size / 2,
        y + size / 2,
        size / 2,
        0,
        Math.PI * 2
    );

    ctx.closePath();
    ctx.clip();

    if (image.complete && image.naturalWidth > 0) {

        const iw = image.naturalWidth;
        const ih = image.naturalHeight;

        // 이미지 중앙을 기준으로 정사각형 크롭
        const cropSize = Math.min(iw, ih);

        const sx = (iw - cropSize) / 2;
        const sy = (ih - cropSize) / 2;

        ctx.drawImage(
            image,
            sx,
            sy,
            cropSize,
            cropSize,
            x,
            y,
            size,
            size
        );

    } else {

        // 이미지 로딩 실패 시 대체 표시
        ctx.fillStyle = "#777";
        ctx.fillRect(x, y, size, size);

        ctx.fillStyle = "#fff";
        ctx.font = "12px Arial";
        ctx.textAlign = "center";

        ctx.fillText(
            "IMAGE",
            x + size / 2,
            y + size / 2
        );
    }

    ctx.restore();

    // 테두리
    ctx.strokeStyle = "#e8d7b0";
    ctx.lineWidth = 3;

    ctx.beginPath();

    ctx.arc(
        x + size / 2,
        y + size / 2,
        size / 2,
        0,
        Math.PI * 2
    );

    ctx.stroke();
}


// 배경
function drawBackground() {

    const sky = ctx.createLinearGradient(
        0, 0, 0, H
    );

    sky.addColorStop(0, "#202b3c");
    sky.addColorStop(1, "#647080");

    ctx.fillStyle = sky;
    ctx.fillRect(0, 0, W, H);

    // 달
    ctx.fillStyle = "#d8d3b7";

    ctx.beginPath();

    ctx.arc(
        760,
        70,
        28,
        0,
        Math.PI * 2
    );

    ctx.fill();

    // 국회 건물
    ctx.fillStyle = "#c4c0b3";

    ctx.fillRect(
        170,
        170,
        560,
        200
    );

    // 지붕
    ctx.fillStyle = "#e2ddcf";

    ctx.beginPath();

    ctx.moveTo(150, 170);
    ctx.lineTo(450, 90);
    ctx.lineTo(750, 170);

    ctx.closePath();
    ctx.fill();

    // 기둥
    for (let i = 0; i < 12; i++) {

        const x = 195 + i * 45;

        ctx.fillStyle = "#e9e4d7";

        ctx.fillRect(
            x,
            185,
            20,
            160
        );
    }

    // 중앙 입구
    ctx.fillStyle = "#3c4656";

    ctx.fillRect(
        395,
        250,
        110,
        120
    );

    // 창문
    ctx.fillStyle = "#697b91";

    for (let i = 0; i < 5; i++) {

        ctx.fillRect(
            220 + i * 95,
            215,
            45,
            35
        );
    }

    // 국회 표지판
    ctx.fillStyle = "#1d2938";

    ctx.fillRect(
        340,
        125,
        220,
        35
    );

    ctx.fillStyle = "#eee7d7";

    ctx.font = "bold 21px Arial";
    ctx.textAlign = "center";

    ctx.fillText(
        "대한민국 국회",
        450,
        150
    );

    // 지면
    ctx.fillStyle = "#323b45";

    ctx.fillRect(
        0,
        GROUND,
        W,
        H - GROUND
    );

    // 도로
    ctx.fillStyle = "#252a30";

    ctx.fillRect(
        0,
        GROUND + 15,
        W,
        75
    );

    // 도로 차선
    ctx.fillStyle = "#c7b88b";

    for (let i = 0; i < 10; i++) {

        ctx.fillRect(
            i * 120 - (frame * 2 % 120),
            GROUND + 48,
            60,
            5
        );
    }
}


// 플레이어 - 김대중 얼굴
function drawPlayer() {

    const x = player.x;
    const y = player.y;

    // 그림자
    ctx.fillStyle = "rgba(0,0,0,0.35)";

    ctx.beginPath();

    ctx.ellipse(
        x + player.w / 2,
        GROUND + 5,
        32,
        7,
        0,
        0,
        Math.PI * 2
    );

    ctx.fill();

    // 정장 몸통
    ctx.fillStyle = "#242b38";

    ctx.beginPath();

    ctx.moveTo(x + 4, y + 50);
    ctx.lineTo(x + 14, y + 40);
    ctx.lineTo(x + 52, y + 40);
    ctx.lineTo(x + 62, y + 50);
    ctx.lineTo(x + 62, y + 66);
    ctx.lineTo(x + 4, y + 66);

    ctx.closePath();
    ctx.fill();

    // 셔츠
    ctx.fillStyle = "#f2f0e8";

    ctx.beginPath();

    ctx.moveTo(x + 22, y + 42);
    ctx.lineTo(x + 44, y + 42);
    ctx.lineTo(x + 34, y + 66);

    ctx.closePath();
    ctx.fill();

    // 넥타이
    ctx.fillStyle = "#8c3030";

    ctx.beginPath();

    ctx.moveTo(x + 31, y + 44);
    ctx.lineTo(x + 37, y + 44);
    ctx.lineTo(x + 35, y + 59);
    ctx.lineTo(x + 34, y + 63);
    ctx.lineTo(x + 32, y + 59);

    ctx.closePath();
    ctx.fill();

    // 김대중 얼굴 이미지
    drawCircularImage(
        kimImage,
        x,
        y,
        player.w
    );
}


// 장애물 - 전두환 얼굴
function drawObstacle(obstacle) {

    const x = obstacle.x;
    const y = obstacle.y;

    // 그림자
    ctx.fillStyle = "rgba(0,0,0,0.35)";

    ctx.beginPath();

    ctx.ellipse(
        x + obstacle.w / 2,
        GROUND + 5,
        obstacle.w / 2,
        8,
        0,
        0,
        Math.PI * 2
    );

    ctx.fill();

    // 얼굴
    drawCircularImage(
        chunImage,
        x,
        y,
        obstacle.w
    );

    // 이름 표시
    ctx.fillStyle = "#f3e7c7";

    ctx.font = "bold 14px Arial";
    ctx.textAlign = "center";

    ctx.fillText(
        "전두환",
        x + obstacle.w / 2,
        y + obstacle.h + 18
    );
}


// 장애물 생성
function spawnObstacle() {

    obstacles.push({

        x: W + 30,

        y: GROUND - 75,

        w: 75,

        h: 75

    });
}


// 플레이어 업데이트
function updatePlayer() {

    if (keys.left) {

        player.vx = -player.speed;

    } else if (keys.right) {

        player.vx = player.speed;

    } else {

        player.vx = 0;
    }

    player.x += player.vx;

    player.x = Math.max(
        0,
        Math.min(
            W - player.w,
            player.x
        )
    );

    if (keys.jump && player.onGround) {

        player.vy = player.jumpPower;

        player.onGround = false;
    }

    player.vy += player.gravity;

    player.y += player.vy;

    if (player.y + player.h >= GROUND) {

        player.y = GROUND - player.h;

        player.vy = 0;

        player.onGround = true;
    }
}


// 장애물 업데이트 및 충돌 판정
function updateObstacles() {

    for (
        let i = obstacles.length - 1;
        i >= 0;
        i--
    ) {

        const obstacle = obstacles[i];

        obstacle.x -= tankSpeed;

        // 화면 밖으로 나간 장애물
        if (obstacle.x + obstacle.w < 0) {

            obstacles.splice(i, 1);

            score += 10;

            continue;
        }

        // 충돌 판정
        const padding = 10;

        const playerBox = {

            x: player.x + padding,

            y: player.y + padding,

            w: player.w - padding * 2,

            h: player.h - padding * 2

        };

        const obstacleBox = {

            x: obstacle.x + padding,

            y: obstacle.y + padding,

            w: obstacle.w - padding * 2,

            h: obstacle.h - padding * 2

        };

        const collision =

            playerBox.x <
                obstacleBox.x + obstacleBox.w &&

            playerBox.x + playerBox.w >
                obstacleBox.x &&

            playerBox.y <
                obstacleBox.y + obstacleBox.h &&

            playerBox.y + playerBox.h >
                obstacleBox.y;

        if (collision) {

            endGame();

            return;
        }
    }
}


// 게임 업데이트
function update() {

    if (!running) return;

    frame++;

    updatePlayer();

    const spawnInterval = Math.max(
        55,
        110 - Math.floor(score / 50)
    );

    if (frame % spawnInterval === 0) {

        spawnObstacle();
    }

    updateObstacles();

    // 난이도 증가
    tankSpeed = Math.min(
        9,
        4 + score / 250
    );

    // 생존 점수
    if (frame % 10 === 0) {

        score++;
    }

    document.getElementById("score").innerText =
        "점수: " + score;

    document.getElementById("best").innerText =
        "최고 기록: " + best;
}


// 화면 그리기
function draw() {

    ctx.clearRect(
        0,
        0,
        W,
        H
    );

    drawBackground();

    for (const obstacle of obstacles) {

        drawObstacle(obstacle);
    }

    drawPlayer();

    if (running) {

        ctx.fillStyle = "rgba(255,255,255,0.8)";

        ctx.font = "16px Arial";

        ctx.textAlign = "left";

        ctx.fillText(
            "생존 시간: " +
            Math.floor(frame / 60) +
            "초",
            15,
            30
        );
    }
}


// 게임 루프
function loop() {

    update();

    draw();

    requestAnimationFrame(loop);
}


// 게임 시작
function startGame() {

    score = 0;

    frame = 0;

    tankSpeed = 4;

    obstacles = [];

    player.x = 130;

    player.y = GROUND - player.h;

    player.vx = 0;

    player.vy = 0;

    player.onGround = true;

    keys.left = false;

    keys.right = false;

    keys.jump = false;

    running = true;

    gameOver = false;

    document.getElementById(
        "start-screen"
    ).style.display = "none";
}


// 게임 종료
function endGame() {

    running = false;

    gameOver = true;

    best = Math.max(
        best,
        score
    );

    document.getElementById(
        "screen-title"
    ).innerText = "게임 오버";

    document.getElementById(
        "screen-description"
    ).innerHTML =
        "전두환 얼굴 장애물에 충돌했습니다!<br>" +
        "최종 점수: " + score + "<br>" +
        "최고 기록: " + best;

    document.getElementById(
        "start-button"
    ).innerText = "다시 시작";

    document.getElementById(
        "start-screen"
    ).style.display = "flex";
}


// 키보드 조작
document.addEventListener(
    "keydown",
    function(e) {

        if (
            [
                "ArrowLeft",
                "ArrowRight",
                "ArrowUp",
                " "
            ].includes(e.key)
        ) {

            e.preventDefault();
        }

        if (
            e.key === "ArrowLeft" ||
            e.key === "a"
        ) {

            keys.left = true;
        }

        if (
            e.key === "ArrowRight" ||
            e.key === "d"
        ) {

            keys.right = true;
        }

        if (
            e.key === "ArrowUp" ||
            e.key === " " ||
            e.key === "w"
        ) {

            keys.jump = true;
        }
    }
);


document.addEventListener(
    "keyup",
    function(e) {

        if (
            e.key === "ArrowLeft" ||
            e.key === "a"
        ) {

            keys.left = false;
        }

        if (
            e.key === "ArrowRight" ||
            e.key === "d"
        ) {

            keys.right = false;
        }

        if (
            e.key === "ArrowUp" ||
            e.key === " " ||
            e.key === "w"
        ) {

            keys.jump = false;
        }
    }
);


// 모바일 조작
function setupButton(id, key) {

    const button = document.getElementById(id);

    button.addEventListener(
        "pointerdown",
        function(e) {

            e.preventDefault();

            keys[key] = true;
        }
    );

    button.addEventListener(
        "pointerup",
        function(e) {

            e.preventDefault();

            keys[key] = false;
        }
    );

    button.addEventListener(
        "pointerleave",
        function() {

            keys[key] = false;
        }
    );

    button.addEventListener(
        "pointercancel",
        function() {

            keys[key] = false;
        }
    );
}


setupButton("left", "left");

setupButton("right", "right");

setupButton("jump", "jump");


// 이미지 로딩 후 다시 그리기
kimImage.onload = draw;

chunImage.onload = draw;

loop();

</script>

</body>
</html>
"""

components.html(
    game_html,
    height=650,
    scrolling=False
)
