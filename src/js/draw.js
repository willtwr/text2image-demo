const canvas = document.getElementById('myCanvas');
const ctx = canvas.getContext('2d');
ctx.lineWidth = 5;
let isDrawing = false;
function startDrawing(event) {
    isDrawing = true;
    draw(event);
}
function draw(event) {
    if (!isDrawing) return;
    let x, y;
    if (event.type.startsWith('touch')) {
        const touch = event.touches[0];
        x = touch.clientX - canvas.offsetLeft;
        y = touch.clientY - canvas.offsetTop;
    } else {
        x = event.clientX - canvas.offsetLeft;
        y = event.clientY - canvas.offsetTop;
    }
    ctx.lineTo(x, y);
    ctx.stroke();
}
function stopDrawing() {
    isDrawing = false;
    ctx.beginPath();
}
// Prevent scrolling when touching the canvas
document.body.addEventListener("touchstart", function (e) {
    if (e.target == canvas) {
    e.preventDefault();
    }
}, { passive: false });
document.body.addEventListener("touchend", function (e) {
    if (e.target == canvas) {
    e.preventDefault();
    }
}, { passive: false });
document.body.addEventListener("touchmove", function (e) {
    if (e.target == canvas) {
    e.preventDefault();
    }
}, { passive: false });
canvas.addEventListener("mousedown", startDrawing);
canvas.addEventListener("mousemove", draw);
canvas.addEventListener("mouseup", stopDrawing);
canvas.addEventListener("mouseout", stopDrawing);
canvas.addEventListener("touchstart", startDrawing, { passive: false });
canvas.addEventListener("touchmove", draw, { passive: false });
canvas.addEventListener("touchend", stopDrawing);
canvas.addEventListener("touchcancel", stopDrawing);