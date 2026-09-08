const $ = (id) => document.getElementById(id);

function renderReading(data) {
  $("status").textContent = data.machine_status;
  $("temperature").textContent = data.temperature.toFixed(1);
  $("rpm").textContent = data.rpm;
  $("voltage").textContent = data.voltage.toFixed(1);
  $("current").textContent = data.current.toFixed(2);
  $("production").textContent = data.production_count;
  $("timestamp").textContent = `Last update: ${data.timestamp.replace("T", " ")}`;

  const alarm = $("alarm");
  alarm.textContent = data.alarm;
  alarm.className = data.alarm === "NORMAL" ? "alarm normal" : "alarm danger";

  const status = $("status");
  status.className = data.machine_status === "FAULT" ? "danger-text" : "";
}

function renderHistory(rows) {
  $("history").innerHTML = rows.map((row) => `
    <tr>
      <td>${row.timestamp.replace("T", " ")}</td>
      <td>${row.temperature.toFixed(1)}</td>
      <td>${row.rpm}</td>
      <td>${row.voltage.toFixed(1)}</td>
      <td>${row.current.toFixed(2)}</td>
      <td>${row.machine_status}</td>
      <td>${row.alarm}</td>
    </tr>
  `).join("");
}

async function updateDashboard() {
  try {
    const reading = await fetch("/api/reading").then((r) => r.json());
    renderReading(reading);
    $("connection").textContent = "ONLINE";
    $("connection").className = "badge online";

    const history = await fetch("/api/history").then((r) => r.json());
    renderHistory(history);
  } catch (error) {
    $("connection").textContent = "OFFLINE";
    $("connection").className = "badge danger";
    console.error(error);
  }
}

updateDashboard();
setInterval(updateDashboard, 3000);
