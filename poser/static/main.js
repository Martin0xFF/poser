/*
 *  Copyright (c) 2015 The WebRTC project authors. All Rights Reserved.
 *
 *  Use of this source code is governed by a BSD-style license
 *  that can be found in the LICENSE file in the root of the source
 *  tree.
 */
'use strict';

// Put variables in global scope to make them available to the browser console.
const constraints = window.constraints = {
  audio: false,
  video: true
};

function sleep(milliseconds) {
  const date = Date.now();
  let currentDate = null;
  do {
    currentDate = Date.now();
  } while (currentDate - date < milliseconds);
}



window.onload = window.onresize = function() {
  var canvas = document.getElementById('canvas');
  canvas.width = window.innerWidth * 0.8;
  canvas.height = window.innerHeight * 0.8;
}


function takepicture() {
  const video = document.querySelector('#user'); // User video
  const tar_video = document.querySelector('#target');
  var canvas = document.getElementById('canvas');
  var context = canvas.getContext('2d');
  var xhr = new XMLHttpRequest();

      if (canvas.width && canvas.height) {


        canvas.width = tar_video.videoWidth*0.5;
        canvas.height = tar_video.videoHeight*0.5;
        context.drawImage(tar_video, 0, 0, canvas.width, canvas.height);
        var tar_data = canvas.toDataURL('image/png');

        context.drawImage(video, 0, 0, canvas.width, canvas.height);
        /*
        canvas.toBlob(function(blob){
          var a = document.createElement("a");
          document.body.appendChild(a);
          a.style = "display: none";
          a.href = url;
          a.download =_generateGuid();
          a.click();
          window.URL.revokeObjectURL(url);
        });
        */
        //canvas.style = "display:none"
        var data = canvas.toDataURL('image/png');

        // Now target


        //var photo = document.getElementById('photo');
        //photo.setAttribute('src', data);
        photo.style = "display:none";
        xhr.open("POST", "/video/update/", true);
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.send(JSON.stringify({
            value: data,
            tar_value: tar_data
        }));
        xhr.open("GET", "/video/collect/", false);
        xhr.send();
        var resp = JSON.parse(xhr.responseText)
        console.log(resp)

        if ("score" in resp){
          console.log(resp);
        }
        }
}


function handleSuccess(stream) {
  const video = document.querySelector('#user');
  const videoTracks = stream.getVideoTracks();
  const tar_video = document.querySelector('#target');
  tar_video.src = document.querySelector('#showVideo').getAttribute("data-video-url");
  tar_video.load();
  console.log('Got stream with constraints:', constraints);
  console.log(`Using video device: ${videoTracks[0].label}`);
  window.stream = stream; // make variable available to browser console
  video.srcObject = stream;
  video.style = "display:none;"
  tar_video.play();
  setInterval(() => { takepicture(); }, 1000/10);
}

function handleError(error) {
  if (error.name === 'ConstraintNotSatisfiedError') {
    const v = constraints.video;
    errorMsg(`The resolution ${v.width.exact}x${v.height.exact} px is not supported by your device.`);
  } else if (error.name === 'PermissionDeniedError') {
    errorMsg('Permissions have not been granted to use your camera and ' +
      'microphone, you need to allow the page access to your devices in ' +
      'order for the demo to work.');
  }
  errorMsg(`getUserMedia error: ${error.name}`, error);
}

function errorMsg(msg, error) {
  const errorElement = document.querySelector('#errorMsg');
  errorElement.innerHTML += `<p>${msg}</p>`;
  if (typeof error !== 'undefined') {
    console.error(error);
  }
}

async function init(e) {
  try {
    const stream = await navigator.mediaDevices.getUserMedia(constraints);
    handleSuccess(stream);
    e.target.disabled = true;
  } catch (e) {
    handleError(e);
  }
}

document.querySelector('#showVideo').addEventListener('click', e => init(e));