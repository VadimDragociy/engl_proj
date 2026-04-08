import { refreshPeople, enrollPerson } from "./api.js";
import { createCameraController } from "./camera.js";

const enrollForm = document.getElementById("enrollForm");
const enrollResult = document.getElementById("enrollResult");
const peopleBody = document.getElementById("peopleBody");
const video = document.getElementById("video");
const overlay = document.getElementById("overlay");
const liveStatus = document.getElementById("liveStatus");
const startBtn = document.getElementById("startBtn");
const stopBtn = document.getElementById("stopBtn");

const camera = createCameraController({
  video,
  overlay,
  liveStatus
});

enrollForm.addEventListener("submit", async (e) => {
  e.preventDefault();

  const { ok, data } = await enrollPerson(enrollForm);

  if (!ok) {
    enrollResult.textContent = "Error: " + (data.detail || "unknown");
    return;
  }

  enrollResult.textContent = `Ready: ${data.added} added. Skipped: ${data.skipped}.`;
  enrollForm.reset();
  await refreshPeople(peopleBody);
});

startBtn.addEventListener("click", camera.startCamera);
stopBtn.addEventListener("click", camera.stopCamera);

refreshPeople(peopleBody);