//Indlæs dele af hjemmesiden
let lastRefreshTimeSpan = document.getElementById("lastRefreshTime");
let attendanceRatio_studentNumber = document.getElementById("attendanceRatio_studentNumber");

let studentsJSON = {}

//Gør forskellige ting og sager når siden indlæses
onload = setTimeout(() => {
    lastRefreshTimeSpan.innerHTML = "Opdateret " + prettyDate()
    $(document).ready(function(){
        $.getJSON("/examples/data/test.json", function(data){
            studentsJSON = data;
            console.log(studentsJSON);
        }).fail(function(){
            document.write("An error has occurred.");
        });
    });
}, 50);

function updateAttendance() {
    lastRefreshTimeSpan.innerHTML = "Opdateret " + prettyDate()
}

function prettyDate() {
    var dateWithouthSecond = new Date();
    return dateWithouthSecond.toLocaleTimeString(navigator.language, {hour: '2-digit', minute:'2-digit'});
}


