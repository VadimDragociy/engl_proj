import { PREVIEW_W } from "./config.js";
import { recognizeFrame } from "./api.js";

export function createCameraController({
  video,
  overlay,
  liveStatus
}) {
  const ctx = overlay.getContext("2d");
  const offscreen = document.createElement("canvas");
  const offCtx = offscreen.getContext("2d");

  let stream = null;
  let timer = null;
  let running = false;
  let sessionId = 0;
  let mySession = 0;
  let lastRequest = 0;

  async function startCamera() {
    sessionId += 1;
    mySession = sessionId;

    if (stream) return;

    stream = await navigator.mediaDevices.getUserMedia({
      video: true,
      audio: false
    });

    video.srcObject = stream;

    await new Promise(resolve => {
      video.onloadedmetadata = () => resolve();
    });

    overlay.width = video.videoWidth;
    overlay.height = video.videoHeight;

    offscreen.width = PREVIEW_W;
    offscreen.height = Math.round(video.videoHeight * (PREVIEW_W / video.videoWidth));

    running = true;
    liveStatus.textContent = "Camera on";
    loop();
  }

  function stopCamera() {
    running = false;
    sessionId += 1;

    if (timer) clearTimeout(timer);
    timer = null;

    if (stream) {
      stream.getTracks().forEach(t => t.stop());
      stream = null;
    }

    ctx.clearRect(0, 0, overlay.width, overlay.height);
    liveStatus.textContent = "Camera off";
  }

  function drawBoxes(frameCanvas, faces) {
    if (!running || mySession !== sessionId) return;

    ctx.clearRect(0, 0, overlay.width, overlay.height);
    ctx.drawImage(frameCanvas, 0, 0, overlay.width, overlay.height);

    const scaleX = overlay.width / offscreen.width;
    const scaleY = overlay.height / offscreen.height;

    ctx.lineWidth = 3;
    ctx.font = "16px Arial";

    faces.forEach(f => {
      const [x1, y1, x2, y2] = f.bbox;

      const x = x1 * scaleX;
      const y = y1 * scaleY;
      const w = (x2 - x1) * scaleX;
      const h = (y2 - y1) * scaleY;

      ctx.strokeStyle = "#00ff88";
      ctx.strokeRect(x, y, w, h);

      const label = `${f.name} ${(f.score * 100).toFixed(1)}%`;

      ctx.fillStyle = "rgba(0,0,0,0.6)";
      ctx.fillRect(x, y - 20, ctx.measureText(label).width + 10, 20);

      ctx.fillStyle = "white";
      ctx.fillText(label, x + 5, y - 5);
    });
  }

  async function loop() {
    if (!running || mySession !== sessionId) return;

    if (video.videoWidth > 0 && video.videoHeight > 0) {
      if (!running || mySession !== sessionId) return;

      offCtx.drawImage(video, 0, 0, offscreen.width, offscreen.height);

      const blob = await new Promise(resolve =>
        offscreen.toBlob(resolve, "image/jpeg", 0.8)
      );

      if (!running || mySession !== sessionId || !blob) return;

      const now = Date.now();
      if (now - lastRequest > 10) {
        lastRequest = now;

        try {
          const { ok, data } = await recognizeFrame(blob);
          if (!running || mySession !== sessionId) return;

          if (!ok) {
            liveStatus.textContent = data.detail || "Recognition error";
          } else {
            drawBoxes(offscreen, data.faces || []);
            liveStatus.textContent = data.faces?.length
              ? `Found faces: ${data.faces.length}`
              : "Face not found";
          }
        } catch (err) {
          liveStatus.textContent = String(err);
        }
      }
    }

    if (running && mySession === sessionId) {
      timer = setTimeout(loop, 50);
    }
  }

  return { startCamera, stopCamera };
}