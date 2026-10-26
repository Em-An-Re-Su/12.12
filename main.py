
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

    .description {
        text-align: center;
        color: #b7bdc8;
        margin-bottom: 12px;
    }
</style>
""", unsafe_allow_html=True)

st.markdown(
    "<h1>12.12 : 국회 탈출</h1>",
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="description">
        1979년 12월 12일을 모티브로 한 역사 풍자 아케이드 게임
        <br>
        탱크를 피하고 최대한 오래 살아남아라!
    </div>
    """,
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

#start-screen {
    position: absolute;
    inset: 0;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    background: rgba(10, 15, 25, 0.85);
    text-align: center;
    z-index: 5;
}

#start-screen h2 {
    color: #e8d7b0;
    font-size: 34px;
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

#canvas-container {
    position: relative;
}

@media (max-width: 600px) {
    #info {
        font-size: 13px;
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
            <h2 id="screen-title">12.12 : 국회 탈출</h2>

            <p id="screen-description">
                탱크를 피해 최대한 오래 살아남아라!<br>
                <br>
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

let running = false;
let gameOver = false;

let score = 0;
let best = 0;
let frame = 0;

let tankSpeed = 4;
let tanks = [];
let particles = [];

const player = {
    x: 130,
    y: GROUND - 65,
    w: 42,
    h: 65,
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

function drawBackground() {

    // 하늘
    const sky = ctx.createLinearGradient(0, 0, 0, H);

    sky.addColorStop(0, "#202b3c");
    sky.addColorStop(1, "#647080");

    ctx.fillStyle = sky;
    ctx.fillRect(0, 0, W, H);

    // 달
    ctx.fillStyle = "#d8d3b7";
    ctx.beginPath();
    ctx.arc(760, 70, 28, 0, Math.PI * 2);
    ctx.fill();

    // 국회 건물
    ctx.fillStyle = "#c4c0b3";

    ctx.fillRect(170, 170, 560, 200);

    // 국회 지붕
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

        ctx.fillRect(x, 185, 20, 160);

        ctx.fillStyle = "#8b8b83";

        ctx.fillRect(x + 4, 185, 12, 160);
    }

    // 국회 중앙 입구
    ctx.fillStyle = "#3c4656";

    ctx.fillRect(395, 250, 110, 120);

    // 본회의장 창문
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

    ctx.fillRect(340, 125, 220, 35);

    ctx.fillStyle = "#eee7d7";

    ctx.font = "bold 21px Arial";
    ctx.textAlign = "center";

    ctx.fillText("대한민국 국회", 450, 150);

    // 지면
    ctx.fillStyle = "#323b45";

    ctx.fillRect(0, GROUND, W, H - GROUND);

    // 도로
    ctx.fillStyle = "#252a30";

    ctx.fillRect(0, GROUND + 15, W, 75);

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

    // 지면 장식
    ctx.fillStyle = "#59616a";

    for (let i = 0; i < 15; i++) {

        ctx.fillRect(
            i * 70,
            GROUND + 5,
            35,
            3
        );
    }
}

function drawPlayer() {

    const x = player.x;
    const y = player.y;

    // 그림자
    ctx.fillStyle = "rgba(0,0,0,0.3)";

    ctx.beginPath();

    ctx.ellipse(
        x + player.w / 2,
        GROUND + 5,
        30,
        7,
        0,
        0,
        Math.PI * 2
    );

    ctx.fill();

    // 다리
    ctx.fillStyle = "#303a2b";

    ctx.fillRect(x + 7, y + 45, 12, 20);
    ctx.fillRect(x + 24, y + 45, 12, 20);

    // 군복 몸통
    ctx.fillStyle = "#64734c";

    ctx.fillRect(x + 3, y + 22, 36, 28);

    // 벨트
    ctx.fillStyle = "#343a29";

    ctx.fillRect(x + 3, y + 40, 36, 5);

    // 머리
    ctx.fillStyle = "#d4a17c";

    ctx.fillRect(x + 9, y + 3, 26, 23);

    // 머리카락
    ctx.fillStyle = "#28251f";

    ctx.fillRect(x + 8, y + 1, 28, 8);

    // 눈
    ctx.fillStyle = "#211c18";

    ctx.fillRect(x + 27, y + 12, 3, 3);

    // 군모
    ctx.fillStyle = "#465237";

    ctx.fillRect(x + 6, y - 3, 32, 8);

    ctx.fillRect(x + 9, y - 7, 26, 7);

    // 모자 장식
    ctx.fillStyle = "#d6bd65";

    ctx.fillRect(x + 19, y - 5, 7, 4);

    // 팔
    ctx.fillStyle = "#64734c";

    ctx.fillRect(x + 33, y + 26, 10, 20);
}

function drawTank(tank) {

    const x = tank.x;
    const y = tank.y;

    // 궤도
    ctx.fillStyle = "#242b24";

    ctx.fillRect(x, y + 36, 105, 25);

    // 궤도 바퀴
    ctx.fillStyle = "#65705c";

    for (let i = 0; i < 6; i++) {

        ctx.beginPath();

        ctx.arc(
            x + 12 + i * 16,
            y + 49,
            8,
            0,
            Math.PI * 2
        );

        ctx.fill();
    }

    // 탱크 몸체
    ctx.fillStyle = "#59674a";

    ctx.fillRect(x + 8, y + 15, 90, 30);

    // 포탑
    ctx.fillStyle = "#6b7857";

    ctx.fillRect(x + 30, y + 2, 45, 22);

    // 포신
    ctx.fillStyle = "#434c3a";

    ctx.fillRect(x + 65, y + 8, 55, 9);

    // 포신 끝
    ctx.fillStyle = "#30382b";

    ctx.fillRect(x + 112, y + 6, 12, 13);

    // 탱크 표시
    ctx.fillStyle = "#c5bd8c";

    ctx.fillRect(x + 45, y + 8, 12, 8);
}

function spawnTank() {

    tanks.push({
        x: W + 30,
        y: GROUND - 60,
        w: 125,
        h: 61
    });
}

function updatePlayer() {

    if (keys.left) {
        player.vx = -player.speed;
    }
    else if (keys.right) {
        player.vx = player.speed;
    }
    else {
        player.vx = 0;
    }

    player.x += player.vx;

    player.x = Math.max(
        0,
        Math.min(W - player.w, player.x)
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

function updateTanks() {

    for (let i = tanks.length - 1; i >= 0; i--) {

        const tank = tanks[i];

        tank.x -= tankSpeed;

        if (tank.x + tank.w < 0) {

            tanks.splice(i, 1);

            score += 10;

            continue;
        }

        // 충돌 판정
        const hitbox = {
            x: tank.x + 10,
            y: tank.y + 10,
            w: tank.w - 20,
            h: tank.h - 10
        };

        const playerBox = {
            x: player.x + 5,
            y: player.y + 5,
            w: player.w - 10,
            h: player.h - 10
        };

        const collision =
            playerBox.x < hitbox.x + hitbox.w &&
            playerBox.x + playerBox.w > hitbox.x &&
            playerBox.y < hitbox.y + hitbox.h &&
            playerBox.y + playerBox.h > hitbox.y;

        if (collision) {

            endGame();
        }
    }
}

function update() {

    if (!running) return;

    frame++;

    updatePlayer();

    // 탱크 생성 간격
    const spawnInterval = Math.max(
        55,
        110 - Math.floor(score / 50)
    );

    if (frame % spawnInterval === 0) {

        spawnTank();
    }

    updateTanks();

    // 시간이 지날수록 난이도 증가
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

function draw() {

    ctx.clearRect(0, 0, W, H);

    drawBackground();

    for (const tank of tanks) {

        drawTank(tank);
    }

    drawPlayer();

    if (running) {

        ctx.fillStyle = "rgba(255,255,255,0.8)";

        ctx.font = "16px Arial";

        ctx.textAlign = "left";

        ctx.fillText(
            "생존 시간: " + Math.floor(frame / 60) + "초",
            15,
            30
        );
    }
}

function loop() {

    update();

    draw();

    requestAnimationFrame(loop);
}

function startGame() {

    score = 0;
    frame = 0;

    tankSpeed = 4;

    tanks = [];
    particles = [];

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

    document.getElementById("start-screen").style.display =
        "none";
}

function endGame() {

    running = false;
    gameOver = true;

    best = Math.max(best, score);

    document.getElementById("screen-title").innerText =
        "게임 오버";

    document.getElementById("screen-description").innerHTML =
        "탱크에 충돌했습니다!<br>" +
        "최종 점수: " + score + "<br>" +
        "최고 기록: " + best;

    document.getElementById("start-button").innerText =
        "다시 시작";

    document.getElementById("start-screen").style.display =
        "flex";
}

// 키보드 조작
document.addEventListener("keydown", function(e) {

    if (
        ["ArrowLeft", "ArrowRight", "ArrowUp", " "]
        .includes(e.key)
    ) {
        e.preventDefault();
    }

    if (e.key === "ArrowLeft" || e.key === "a") {
        keys.left = true;
    }

    if (e.key === "ArrowRight" || e.key === "d") {
        keys.right = true;
    }

    if (
        e.key === "ArrowUp" ||
        e.key === " " ||
        e.key === "w"
    ) {
        keys.jump = true;
    }
});

document.addEventListener("keyup", function(e) {

    if (e.key === "ArrowLeft" || e.key === "a") {
        keys.left = false;
    }

    if (e.key === "ArrowRight" || e.key === "d") {
        keys.right = false;
    }

    if (
        e.key === "ArrowUp" ||
        e.key === " " ||
        e.key === "w"
    ) {
        keys.jump = false;
    }
});

// 모바일 버튼
function setupButton(id, key) {

    const button = document.getElementById(id);

    button.addEventListener("pointerdown", function(e) {

        e.preventDefault();

        keys[key] = true;
    });

    button.addEventListener("pointerup", function(e) {

        e.preventDefault();

        keys[key] = false;
    });

    button.addEventListener("pointerleave", function() {

        keys[key] = false;
    });

    button.addEventListener("pointercancel", function() {

        keys[key] = false;
    });
}

setupButton("left", "left");
setupButton("right", "right");
setupButton("jump", "jump");

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
