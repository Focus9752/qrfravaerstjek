//Indlæs dele af hjemmesiden
let lastRefreshTimeSpan = document.getElementById("lastRefreshTime");
let attendanceRatio_studentNumber = document.getElementById("attendanceRatio_studentNumber");

let studentsJSON = JSON.parse("./students.json");
console.log(studentsJSON);

//Gør forskellige ting og sager når siden indlæses
onload = function() {
    lastRefreshTimeSpan.innerHTML = "Opdateret " + prettyDate()
}

function updateAttendance() {
    lastRefreshTimeSpan.innerHTML = "Opdateret " + prettyDate()
}

function prettyDate() {
    var dateWithouthSecond = new Date();
    return dateWithouthSecond.toLocaleTimeString(navigator.language, {hour: '2-digit', minute:'2-digit'});
}

