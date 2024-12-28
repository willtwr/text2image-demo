function getPosition(event){
    coord.x = event.clientX - canvas.offsetLeft;
    coord.y = event.clientY - canvas.offsetTop;
};
function startPainting(event){
    paint = true;
    getPosition(event);
};
function stopPainting(){
    paint = false;
};
function sketch(event){
    if (!paint) return;
    ctx.beginPath();
        
    ctx.lineWidth = 5;

    // Sets the end of the lines drawn
    // to a round shape.
    ctx.lineCap = 'round';
        
    ctx.strokeStyle = 'green';
        
    // The cursor to start drawing
    // moves to this coordinate
    ctx.moveTo(coord.x, coord.y);

    // The position of the cursor
    // gets updated as we move the
    // mouse around.
    getPosition(event);

    // A line is traced from start
    // coordinate to this coordinate
    ctx.lineTo(coord.x , coord.y);
        
    // Draws the line.
    ctx.stroke();
};

const canvas = document.getElementById('<canvasid>');
const ctx = canvas.getContext('2d');
let coord = {x:0 , y:0};
let paint = false;

canvas.addEventListener('mousedown', startPainting);
canvas.addEventListener('mouseup', stopPainting);
canvas.addEventListener('mousemove', sketch);