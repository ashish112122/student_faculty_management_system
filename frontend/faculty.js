/**
 * Member 2 - Faculty & Marks Module
 * frontend/faculty.js
 */

document.addEventListener("DOMContentLoaded", () => {
  const facultyId = document
    .querySelector('meta[name="faculty-id"]')
    ?.getAttribute("content");

  if (!facultyId) return;

  loadDashboard(facultyId);

  const updateForm = document.getElementById("update-profile-form");
  if (updateForm) {
    updateForm.addEventListener("submit", (e) => {
      e.preventDefault();
      updateProfile(facultyId);
    });
  }
});

async function loadDashboard(facultyId) {
  try {
    const res  = await fetch("/faculty/dashboard?faculty_id=" + facultyId);
    const data = await res.json();

    if (!res.ok) {
      showToast(data.error || "Failed to load dashboard", "bg-danger");
      return;
    }

    document.getElementById("prof-name").textContent          = data.profile.name        || "-";
    document.getElementById("prof-email-display").textContent = data.profile.email       || "";
    document.getElementById("prof-dept").textContent          = data.profile.dept_id     != null ? data.profile.dept_id : "-";
    document.getElementById("prof-designation").textContent   = data.profile.designation || "-";

    document.getElementById("upd-dept").value        = data.profile.dept_id     != null ? data.profile.dept_id : "";
    document.getElementById("upd-designation").value = data.profile.designation || "";

    var subjEl = document.getElementById("prof-subjects");
    if (subjEl) {
      if (!data.classes || data.classes.length === 0) {
        subjEl.innerHTML = "<span style='color:#7a82a8'>None assigned</span>";
      } else {
        subjEl.innerHTML = data.classes.map(function(c) {
          return "<div style='padding:2px 0'>" + c.subject_name + "</div>";
        }).join("");
      }
    }

    var classesList = document.getElementById("classes-list");
    if (classesList) {
      if (!data.classes || data.classes.length === 0) {
        classesList.textContent = "No classes found.";
      } else {
        classesList.innerHTML = data.classes.map(function(cls) {
          return "<div style='padding:6px 0;border-bottom:1px solid #b8bece'><strong>" + cls.subject_name + "</strong><span style='float:right;color:#5b6abf'>" + cls.student_count + " students</span></div>";
        }).join("");
      }
    }
  } catch (err) {
    showToast("Network error loading dashboard", "bg-danger");
  }
}

async function updateProfile(facultyId) {
  var deptId      = document.getElementById("upd-dept").value.trim();
  var designation = document.getElementById("upd-designation").value.trim();
  var msgEl       = document.getElementById("update-msg");

  msgEl.textContent = "";

  try {
    const res  = await fetch("/faculty/profile/update", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        faculty_id:  parseInt(facultyId, 10),
        dept_id:     parseInt(deptId, 10),
        designation: designation
      })
    });
    const data = await res.json();

    if (res.ok) {
      var modal = document.getElementById("editProfileModal");
      if (modal) bootstrap.Modal.getInstance(modal).hide();
      document.getElementById("prof-dept").textContent        = deptId;
      document.getElementById("prof-designation").textContent = designation;
      msgEl.textContent = "Profile updated";
      msgEl.style.color = "#7ddb8f";
    } else {
      msgEl.textContent = data.error || "Update failed";
      msgEl.style.color = "#e05555";
    }
  } catch (err) {
    msgEl.textContent = "Network error";
    msgEl.style.color = "#e05555";
  }
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
