/**
 * classes.js - My Classes page
 */

var barChart   = null;
var curveChart = null;
var gradeChart = null;
var selectedSubjectId   = null;
var selectedSubjectName = null;
var selectedExamType    = "midterm";

document.addEventListener("DOMContentLoaded", function() {
  var facultyId = document.querySelector("meta[name='faculty-id']")?.getAttribute("content");
  if (!facultyId) return;
  loadSubjects(facultyId);
});

async function loadSubjects(facultyId) {
  try {
    var res  = await fetch("/faculty/dashboard?faculty_id=" + facultyId);
    var data = await res.json();
    var grid = document.getElementById("subject-grid");
    if (!data.classes || data.classes.length === 0) {
      grid.innerHTML = "<div style='color:#666;font-size:14px'>No classes assigned.</div>";
      return;
    }
    grid.innerHTML = data.classes.map(function(c) {
      return "<div class='subject-card' onclick='selectSubject(this," + c.subject_id + ",\"" + c.subject_name + "\")'>" +
             "<h5>" + c.subject_name + "</h5>" +
             "<p>" + c.student_count + " students</p></div>";
    }).join("");
  } catch(e) {
    document.getElementById("subject-grid").innerHTML = "<div style='color:#c0392b'>Failed to load subjects.</div>";
  }
}

function selectSubject(el, subjectId, subjectName) {
  document.querySelectorAll(".subject-card").forEach(function(c){ c.classList.remove("selected"); });
  el.classList.add("selected");
  selectedSubjectId   = subjectId;
  selectedSubjectName = subjectName;
  document.getElementById("analytics-panel").style.display = "block";
  loadAnalytics();
}

function selectExam(btn, examType) {
  document.querySelectorAll(".exam-btn").forEach(function(b){ b.classList.remove("active"); });
  btn.classList.add("active");
  selectedExamType = examType;
  if (selectedSubjectId) loadAnalytics();
}

async function loadAnalytics() {
  hide("no-data-msg"); hide("data-section");

  try {
    var res  = await fetch("/marks/analytics?subject_id=" + selectedSubjectId + "&exam_type=" + encodeURIComponent(selectedExamType));
    var data = await res.json();

    if (!res.ok) {
      show("no-data-msg"); return;
    }

    document.getElementById("analytics-title").textContent = selectedSubjectName + " — " + selectedExamType.charAt(0).toUpperCase() + selectedExamType.slice(1);
    document.getElementById("stat-avg").textContent    = data.stats.average;
    document.getElementById("stat-median").textContent = data.stats.median;
    document.getElementById("stat-high").textContent   = data.stats.highest;
    document.getElementById("stat-low").textContent    = data.stats.lowest;
    document.getElementById("stat-total").textContent  = data.stats.total;

    renderTable("tbody-all",  data.students);
    renderTable("tbody-top",  data.top_performers);
    renderTable("tbody-risk", data.at_risk);
    renderBarChart(data.students);
    renderCurveChart(data.students);
    renderGradeChart(data.grade_distribution);

    show("data-section");
  } catch(e) {
    show("no-data-msg");
  }
}

function renderTable(tbodyId, rows) {
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

function renderBarChart(students) {
  var canvas = document.getElementById("barChart");
  if (!canvas) return;
  if (barChart) { barChart.destroy(); barChart = null; }
  var avg = students.reduce(function(s,r){ return s + r.marks_obtained; }, 0) / students.length;
  barChart = new Chart(canvas.getContext("2d"), {
    type: "bar",
    data: {
      labels: students.map(function(r){ return r.student_name; }),
      datasets: [
        { label:"Marks", data: students.map(function(r){ return r.marks_obtained; }), backgroundColor:"rgba(91,106,191,0.75)", borderColor:"rgba(91,106,191,1)", borderWidth:1 },
        { label:"Class Avg", data: students.map(function(){ return avg; }), type:"line", borderColor:"#e05555", borderWidth:2, pointRadius:0, fill:false }
      ]
    },
    options: { responsive:true, scales:{ y:{ beginAtZero:true, max:100 } }, plugins:{ legend:{ display:true } } }
  });
}

function renderCurveChart(students) {
  var canvas = document.getElementById("curveChart");
  if (!canvas) return;
  if (curveChart) { curveChart.destroy(); curveChart = null; }
  var bins = [0,0,0,0,0,0,0,0,0,0];
  students.forEach(function(r) { bins[Math.min(Math.floor(r.marks_obtained/10),9)]++; });
  curveChart = new Chart(canvas.getContext("2d"), {
    type: "line",
    data: {
      labels: ["0-9","10-19","20-29","30-39","40-49","50-59","60-69","70-79","80-89","90-100"],
      datasets: [{ label:"Students", data:bins, borderColor:"#5b6abf", backgroundColor:"rgba(91,106,191,0.2)", borderWidth:2, fill:true, tension:0.4, pointBackgroundColor:"#5b6abf" }]
    },
    options: { responsive:true, scales:{ y:{ beginAtZero:true, ticks:{ stepSize:1 } } }, plugins:{ legend:{ display:false } } }
  });
}

function renderGradeChart(dist) {
  var canvas = document.getElementById("gradeChart");
  if (!canvas) return;
  if (gradeChart) { gradeChart.destroy(); gradeChart = null; }
  gradeChart = new Chart(canvas.getContext("2d"), {
    type: "doughnut",
    data: {
      labels: ["A","B","C","D","F"],
      datasets: [{ data:[dist.A,dist.B,dist.C,dist.D,dist.F], backgroundColor:["#3a9e6e","#5b6abf","#3aabbb","#d4a017","#c0392b"], borderWidth:2 }]
    },
    options: { responsive:true, plugins:{ legend:{ position:"bottom", labels:{ font:{ size:12 } } } } }
  });
}

function switchTab(e, id) {
  document.querySelectorAll(".tab-content").forEach(function(el){ el.classList.remove("active"); });
  document.querySelectorAll(".tab-btn").forEach(function(el){ el.classList.remove("active"); });
  document.getElementById(id).classList.add("active");
  e.target.classList.add("active");
}

function show(id) { var el = document.getElementById(id); if (el) el.style.display = ""; }
function hide(id) { var el = document.getElementById(id); if (el) el.style.display = "none"; }
