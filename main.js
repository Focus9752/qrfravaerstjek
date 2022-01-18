

function updateAttendance() {

}

function prettyDate() {
    var dateWithouthSecond = new Date();
    return dateWithouthSecond.toLocaleTimeString(navigator.language, {hour: '2-digit', minute:'2-digit'});
}
