var canvas = document.querySelector('.main');
var ctx = canvas.getContext('2d');
var w = canvas.width, h = canvas.height;
var mouse = {
    x : 0,
    y : 0
};
var draw = false;
ctx.lineWidth = 40;


canvas.addEventListener('mousedown',function(event)
{
    mouse.x = event.pageX - this.offsetLeft;
    mouse.y = event.pageY - this.offsetTop;
    draw = true;
    ctx.beginPath();
    ctx.moveTo(mouse.x, mouse.y);
});


canvas.addEventListener('mousemove', function(event)
{
    if(draw==true){
        mouse.x = event.pageX - this.offsetLeft;
        mouse.y = event.pageY - this.offsetTop;
        ctx.lineTo(mouse.x, mouse.y);
        ctx.stroke();
    }
});


canvas.addEventListener('mouseup', function(event)
{
    mouse.x = event.pageX - this.offsetLeft;
    mouse.y = event.pageY - this.offsetTop;
    ctx.lineTo(mouse.x, mouse.y);
    ctx.stroke();
    ctx.closePath();
    draw = false;
});


function clearCanvas()
{
    ctx.clearRect(0, 0, w, h)
}


function sendBitmap()
{
    var request = new XMLHttpRequest();
    var data = new FormData;
    var img = canvas.toDataURL();

    request.onreadystatechange = function(){
        if (request.readyState == XMLHttpRequest.DONE) {
            result = request.responseText.split(',')
            alert(`Я думаю это цифра ${result[0]}\nВероятность: ${result[1]}%`);
        }
    }
    request.open('POST', '/detect-int', false);
    data.append('imageBase64', img);
    request.send(data);
}