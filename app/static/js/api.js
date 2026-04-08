import { escapeHtml } from "./utils.js";

export async function refreshPeople(peopleBody) {
  const r = await fetch("/api/people");
  const data = await r.json();

  peopleBody.innerHTML = (data.people || [])
    .map(p => `<tr><td>${escapeHtml(p.name)}</td><td>${p.samples}</td></tr>`)
    .join("");
}

export async function enrollPerson(form) {
  const fd = new FormData(form);
  const r = await fetch("/api/enroll", { method: "POST", body: fd });
  const data = await r.json();

  return { ok: r.ok, data };
}

export async function recognizeFrame(blob) {
  const fd = new FormData();
  fd.append("file", blob, "frame.jpg");

  const r = await fetch("/api/recognize_frame", {
    method: "POST",
    body: fd
  });

  return { ok: r.ok, data: await r.json() };
}