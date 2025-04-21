function setYearDropdown(value) {
    var year_element = document.getElementById('year-dropdown');
    year_element.textContent = value;
    year_element.dataset.key = value;
}
function setStatisticDropdown(key, value) {
    var statistic_element = document.getElementById('statistic-dropdown');
    statistic_element.textContent = value;
    statistic_element.dataset.key = key;
}
function setGolferDropdown(key, value) {
    var golfer_element = document.getElementById('golfer-dropdown');
    golfer_element.textContent = value;
    golfer_element.dataset.key = key;
}
function setCourseDropdown(key, value) {
    var course_element = document.getElementById('course-dropdown');
    course_element.textContent = value;
    course_element.dataset.key = key;
}

window.addEventListener('DOMContentLoaded', function() {
    const dropdowns = document.getElementById('filters');
    var available_width = dropdowns.offsetWidth;
    var initial_used_width = 0;
    for (var dropdown of dropdowns.children) {
        initial_used_width = initial_used_width + dropdown.offsetWidth;
    }

    if (initial_used_width > available_width) {
        for (var dropdown of dropdowns.children) {
            for (var el of dropdown.children) {
                if (el.type === "button") {
                    el.style.maxWidth = `${el.offsetWidth * available_width / initial_used_width}px`;
                }
            }
        }
    } else {

    }
});