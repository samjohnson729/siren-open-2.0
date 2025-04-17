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

const observer = new MutationObserver((mutationsList, observer) => {
    for (const mutation of mutationsList) {
        if (mutation.type === 'attributes' && mutation.attributeName === 'data-key') {
            updateScorecard();
        }
    }
});
const course = document.getElementById('course-dropdown');
const year = document.getElementById('year-dropdown');
const statistic = document.getElementById('statistic-dropdown');
observer.observe(course, { attributes: true });
observer.observe(year, { attributes: true });
observer.observe(statistic, { attributes: true });
