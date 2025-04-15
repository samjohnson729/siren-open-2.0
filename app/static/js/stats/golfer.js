function updateContent() {
    const golfer = document.getElementById('golfer-dropdown').dataset.key;
    const statistic = document.getElementById('statistic-dropdown').dataset.key;

    let url = '/stats/golfer?'
    url = url + 'golfer=' + golfer;
    url = url + '&statistic=' + statistic;
    window.location.href = url;
}
function setYearDropdown(value) {
    var year_element = document.getElementById('year-dropdown');
    year_element.textContent = value;
    year_element.dataset.key = value;
    updateContent();
}
function setStatisticDropdown(key, value) {
    var statistic_element = document.getElementById('statistic-dropdown');
    statistic_element.textContent = value;
    statistic_element.dataset.key = key;
    updateContent();
}
function setGolferDropdown(key, value) {
    var golfer_element = document.getElementById('golfer-dropdown');
    golfer_element.textContent = value;
    golfer_element.dataset.key = key;
    updateContent();
}
