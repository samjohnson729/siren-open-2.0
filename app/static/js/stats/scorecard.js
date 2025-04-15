function updateScorecard() {
    const year = document.getElementById('year-dropdown').dataset.key;
    const course = document.getElementById('course-dropdown').dataset.key;
    const statistic = document.getElementById('statistic-dropdown').dataset.key;

    let url = '/stats/scorecard?';
    if (year && year != 'all') url = url + 'year=' + year;
    url = url + '&course=' + course;
    url = url + '&statistic=' + statistic;
    window.location.href = url;
}

function setYearDropdown(value) {
    var year_element = document.getElementById('year-dropdown');
    year_element.textContent = value;
    year_element.dataset.key = value;
    updateScorecard();
}
function setStatisticDropdown(key, value) {
    var statistic_element = document.getElementById('statistic-dropdown');
    statistic_element.textContent = value;
    statistic_element.dataset.key = key;
    updateScorecard();
}
function setCourseDropdown(key, value) {
    var course_element = document.getElementById('course-dropdown');
    course_element.textContent = value;
    course_element.dataset.key = key;
    updateScorecard();
}