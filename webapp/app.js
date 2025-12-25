const API_URL = "https://lens-mate-api.onrender.com/calculate";

async function calculate() {

  const body = {
    focal_length: Number(document.getElementById("focal").value),
    aperture: Number(document.getElementById("aperture").value),
    focus_distance: 2,
    sensor_width: 22.3,
    sensor_height: 14.8,
    coc: 0.019
  };

  const res = await fetch(API_URL, {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify(body)
  });

  const data = await res.json();
  drawPlot(data);
}

function drawPlot(data) {

  const trace = {
    x: [data.near, data.focus_distance, data.far],
    y: [1, 1, 1],
    mode: "markers",
    name: "DoF"
  };

  Plotly.newPlot("plot", [trace], {
    title: "Depth of Field",
    xaxis: {title: "Distanza (m)"}
  }, {responsive: true});
}
