const $ = (id) => document.getElementById(id);

function renderReading(data) {
  if (!data.temperature) return;
  $("status").textContent = data.machine_status;
  $("temperature").textContent = Number(data.temperature).toFixed(1);
  $("rpm").textContent = data.rpm;
  $("voltage").textContent = Number(data.voltage).toFixed(1);
  $("current").textContent = Number(data.current).toFixed(2);
  $("production").textContent = data.production_count;
  $("timestamp").textContent = `Last update: ${data.timestamp.replace("T", " ")}`;
  $("source").textContent = `SOURCE: ${data.source || "SIMULATOR"}`;

  const alarm = $("alarm");
  alarm.textContent = data.alarm;
  alarm.className = data.alarm === "NORMAL" ? "alarm normal" : "alarm danger";
  $("status").className = data.machine_status === "FAULT" ? "danger-text" : "good-text";
  $("health").textContent = `${data.health_score ?? "—"}/100`;
}

function renderHistory(rows) {
  $("history").innerHTML = rows.map((row) => `
    <tr>
      <td>${row.timestamp.replace("T", " ")}</td>
      <td>${Number(row.temperature).toFixed(1)}</td>
      <td>${row.rpm}</td>
      <td>${Number(row.voltage).toFixed(1)}</td>
      <td>${Number(row.current).toFixed(2)}</td>
      <td>${row.machine_status}</td>
      <td>${row.alarm}</td>
      <td>${row.source || "SIMULATOR"}</td>
    </tr>
  `).join("");
}

function renderAnalytics(data) {
  const oee = data.oee;
  $("oee").textContent = `${oee.oee}%`;
  $("oeeBar").style.width = `${Math.min(100, oee.oee)}%`;
  $("availability").textContent = `${oee.availability}%`;
  $("performance").textContent = `${oee.performance}%`;
  $("quality").textContent = `${oee.quality}%`;
  $("avgTemp").textContent = `${data.trend.avg_temperature} °C`;
  $("maxTemp").textContent = `${data.trend.max_temperature} °C`;
  $("maxCurrent").textContent = `${data.trend.max_current} A`;
}

function renderAlarms(rows) {
  $("alarmList").innerHTML = rows.length ? rows.slice(0, 5).map((row) => `
    <div class="alarm-item"><b>${row.alarm}</b><span>${row.timestamp.replace("T", " ")}</span></div>
  `).join("") : '<span class="muted">No alarms recorded.</span>';
}

async function updateDashboard() {
  try {
    const reading = await fetch("/api/reading").then((r) => r.json());
    renderReading(reading);
    $("connection").textContent = "ONLINE";
    $("connection").className = "badge online";

    const [history, analytics, alarms] = await Promise.all([
      fetch("/api/history").then((r) => r.json()),
      fetch("/api/analytics").then((r) => r.json()),
      fetch("/api/alarms").then((r) => r.json()),
    ]);
    renderHistory(history);
    renderAnalytics(analytics);
    renderAlarms(alarms);
  } catch (error) {
    $("connection").textContent = "OFFLINE";
    $("connection").className = "badge danger";
    console.error(error);
  }
}

updateDashboard();
setInterval(updateDashboard, 3000);
