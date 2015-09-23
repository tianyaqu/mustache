function getStyle(x, styleProp) {
     if (x.currentStyle) var y = x.currentStyle[styleProp];
     else if (window.getComputedStyle) var y = document.defaultView.getComputedStyle(x, null).getPropertyValue(styleProp);
     return y;
}

(function() {
  var canvas, ctx, onError, onSuccess, update, video, ws;
  var openCvCoords;
  var mustache_style = '0';

  onError = function(e) {
    return console.log("Rejected", e);
  };

  onSuccess = function(localMediaStream) {
    video.src = URL.createObjectURL(localMediaStream);
    return setInterval(update, 300);
  };


  update = function() {
    ctx.drawImage(video, 0, 0, 320, 240);

    if(canvas.toBlob){
        canvas.toBlob(function(blob) {
            ws.send(blob);
        }, 'image/jpeg');
    }

    if(typeof(openCvCoords) != "undefined")
    {
        if(openCvCoords[0] != -1)
        {
            ctx.drawImage(mustache,openCvCoords[0], openCvCoords[1], openCvCoords[2], openCvCoords[3]);
        }
    }
  };

  video = document.querySelector('video');

  canvas = document.querySelector('canvas');

  //var id = "label_huzi"+ (x - '0' + 1);
  //var ele = document.getElementById(id);
  //var url = getStyle(ele, 'background-image');
  var mustache = new Image();  
  //default mustache
  mustache.src = '/static/img/huzi' + (mustache_style - '0' + 1) + '.png';

  ctx = canvas.getContext('2d');

  ws = new WebSocket("ws://" + location.host + "/detector");

  ws.onopen = function() {
    return console.log("Opened websocket");
  };

  ws.onmessage = function(e) {
    openCvCoords = JSON.parse(e.data);
    mustache_style = $("input[name='mustache']:checked").val();
    mustache.src = '/static/img/huzi' + (mustache_style - '0' + 1) + '.png';
  };

  navigator.webkitGetUserMedia({
    'video': true,
    'audio': false
  }, onSuccess, onError);

}).call(this);
