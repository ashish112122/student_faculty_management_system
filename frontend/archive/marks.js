/**
 * Member 2 - Faculty & Marks Module
 * frontend/marks.js
 */

var barChart   = null;
var curveChart = null;
var gradeChart = null;

document.addEventListener("DOMContentLoaded", function() {
  var addForm = document.getElementById("add-marks-form");
  if (addForm) addForm.addEventListener("submit", handleAddMarks);

  var updForm = document.getElementById("update-marks-form");
  if (updForm) updForm.addEventListener("submit", handleUpdateMarks);

  var loadBtn = document.getElementById("load-report-btn");
  if (loadBtn) loadBtn.addEventListener("click", handleLoadReport);
});

// ---------------------------------------------------------------------------
// Add marks
// ---------------------------------------------------------------------------
async function handleAddMarks(e) {
  e.preventDefault();
  hide("add-error");

  var payload = {
    student_id:     parseInt(document.getElementById("add-student-id").value, 10),
    subject_id:     parseInt(document.getElementById("add-subject-id").value, 10),
    marks_obtained: parseFloat(document.getElementById("add-marks-obtained").value),
    exam_type:      document.getElementById("add-exam-type").value
  };

  try {
    var res  = await fetch("/marks/add", { method:"POST", headers:{"Content-Type":"application/json"}, body:JSON.stringify(payload) });
    var data = await res.json();
    if (res.status === 201) {
      showToast("Marks added (ID: " + data.marks_id + ")", "bg-success");
      e.target.reset();
    } else {
      showInline("add-error", data.error);
    }
  } catch(err) { showToast("Network error", "bg-danger"); }
}

// ---------------------------------------------------------------------------
// Update marks
// ---------------------------------------------------------------------------
async function handleUpdateMarks(e) {
  e.preventDefault();
  hide("upd-error"); hide("upd-success");

  var marksId      = parseInt(document.getElementById("upd-marks-id").value, 10);
  var marksObtained = parseFloat(document.getElementById("upd-marks-obtained").value);

  try {
    var res  = await fetch("/marks/update/" + marksId, { method:"PUT", headers:{"Content-Type":"application/json"}, body:JSON.stringify({marks_obtained: marksObtained}) });
    var data = await res.json();
    if (res.ok) { showInline("upd-success", "Updated. New grade: " + data.grade); }
    else        { showInline("upd-error",   data.error); }
  } catch(err) { showToast("Network error", "bg-danger"); }
}

// ---------------------------------------------------------------------------
// Load report
// ---------------------------------------------------------------------------
async function handleLoadReport() {
  var subjectId = document.getElementById("filter-subject-id").value.trim();
  var examType  = document.getElementById("filter-exam-type").value;

  if (!subjectId || !examType) { showToast("Please select subject ID and exam type", "bg-warning"); return; }

  hide("no-data-msg"); hide("results-section");

  try {
    var res  = await fetch("/marks/analytics?subject_id=" + subjectId + "&exam_type=" + encodeURIComponent(examType));
    var data = await res.json();

    if (!res.ok) {
      if (res.status === 404) { show("no-data-msg"); }
      else { showToast(data.error || "Failed to load", "bg-danger"); }
      return;
    }

    // Stats
    document.getElementById("stat-avg").textContent    = data.stats.average;
    document.getElementById("stat-median").textContent = data.stats.median;
    document.getElementById("stat-high").textContent   = data.stats.highest;
    document.getElementById("stat-low").textContent    = data.stats.lowest;
    document.getElementById("stat-total").textContent  = data.stats.total;

    // Tables
    renderTable("tbody-all",  data.students,       false);
    renderTable("tbody-top",  data.top_performers, false);
    renderTable("tbody-risk", data.at_risk,        false);

    // Charts
    renderBarChart(data.students);
    renderCurveChart(data.students);
    renderGradeChart(data.grade_distribution);

    show("results-section");
  } catch(err) { showToast("Network error", "bg-danger"); }
}

// ---------------------------------------------------------------------------
// Tables
// ---------------------------------------------------------------------------
function renderTable(tbodyId, rows, highlight) {
  var tbody = document.getElementById(tbodyId);
  if (!tbody) return;
  if (!rows || rows.length === 0) {
    tbody.innerHTML = "<tr><td colspan='4' style='color:#888;text-align:center'>None</td></tr>";
    return;
  }
  tbody.innerHTML = rows.map(function(r, i) {
    return "<tr><td>" + (i+1) + "</td><td>" + r.student_name + "</td><td>" + r.marks_obtained + "</td><td><span class='badge-grade g-" + (r.grade||"F") + "'>" + (r.grade||"F") + "</span></td></tr>";
  }).join("");
}

// ---------------------------------------------------------------------------
// Bar chart
// ---------------------------------------------------------------------------
function renderBarChart(students) {
  var canvas = document.getElementById("barChart");
  if (!canvas) return;
  if (barChart) { barChart.destroy(); barChart = null; }

  var avg = students.reduce(function(s,r){ return s + r.marks_obtained; }, 0) / students.length;
  var avgLine = students.map(function(){ return avg; });

  barChart = new Chart(canvas.getContext("2d"), {
    type: "bar",
    data: {
      labels: students.map(function(r){ return r.student_name; }),
      datasets: [
        { label:"Marks", data: students.map(function(r){ return r.marks_obtained; }), backgroundColor:"rgba(91,106,191,0.75)", borderColor:"rgba(91,106,191,1)", borderWidth:1 },
        { label:"Class Avg", data: avgLine, type:"line", borderColor:"#e05555", borderWidth:2, pointRadius:0, fill:false }
      ]
    },
    options: { responsive:true, scales:{ y:{ beginAtZero:true, max:100 } }, plugins:{ legend:{ display:true } } }
  });
}

// ---------------------------------------------------------------------------
// Curve chart (distribution histogram)
// ---------------------------------------------------------------------------
function renderCurveChart(students) {
  var canvas = document.getElementById("curveChart");
  if (!canvas) return;
  if (curveChart) { curveChart.destroy(); curveChart = null; }

  var bins   = [0,0,0,0,0,0,0,0,0,0];
  var labels = ["0-9","10-19","20-29","30-39","40-49","50-59","60-69","70-79","80-89","90-100"];
  students.forEach(function(r) {
    var idx = Math.min(Math.floor(r.marks_obtained / 10), 9);
    bins[idx]++;
  });

  curveChart = new Chart(canvas.getContext("2d"), {
    type: "line",
    data: {
      labels: labels,
      datasets: [{
        label: "Students",
        data: bins,
        borderColor: "#5b6abf",
        backgroundColor: "rgba(91,106,191,0.2)",
        borderWidth: 2,
        fill: true,
        tension: 0.4,
        pointBackgroundColor: "#5b6abf"
      }]
    },
    options: { responsive:true, scales:{ y:{ beginAtZero:true, ticks:{ stepSize:1 } } }, plugins:{ legend:{ display:false } } }
  });
}

// ---------------------------------------------------------------------------
// Grade donut chart
// ---------------------------------------------------------------------------
function renderGradeChart(dist) {
  var canvas = document.getElementById("gradeChart");
  if (!canvas) return;
  if (gradeChart) { gradeChart.destroy(); gradeChart = null; }

  gradeChart = new Chart(canvas.getContext("2d"), {
    type: "doughnut",
    data: {
      labels: ["A","B","C","D","F"],
      datasets: [{
        data: [dist.A, dist.B, dist.C, dist.D, dist.F],
        backgroundColor: ["#3a9e6e","#5b6abf","#3aabbb","#d4a017","#c0392b"],
        borderWidth: 2
      }]
    },
    options: { responsive:true, plugins:{ legend:{ position:"bottom", labels:{ font:{ size:12 } } } } }
  });
}

// ---------------------------------------------------------------------------
// Tab switching
// ---------------------------------------------------------------------------
function switchTab(id) {
  document.querySelectorAll(".tab-content").forEach(function(el){ el.classList.remove("active"); });
  document.querySelectorAll(".tab-btn").forEach(function(el){ el.classList.remove("active"); });
  document.getElementById(id).classList.add("active");
  event.target.classList.add("active");
}

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------
function show(id) { var el = document.getElementById(id); if (el) el.style.display = ""; }
function hide(id) { var el = document.getElementById(id); if (el) el.style.display = "none"; }

function showInline(id, msg) {
  var el = document.getElementById(id);
  if (!el) return;
  el.textContent = msg;
  el.style.display = "block";
}

function showToast(message, bgClass) {
  bgClass = bgClass || "bg-secondary";
  var toastEl   = document.getElementById("toast");
  var toastBody = document.getElementById("toast-body");
  if (!toastEl || !toastBody) return;
  toastEl.className     = "toast align-items-center text-white border-0 " + bgClass;
  toastBody.textContent = message;
  bootstrap.Toast.getOrCreateInstance(toastEl).show();
}
