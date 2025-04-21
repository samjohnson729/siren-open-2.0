function updateContent() {
    const year = document.getElementById('year-dropdown').dataset.key;
    const course = document.getElementById('course-dropdown').dataset.key;
    const golfer = document.getElementById('golfer-dropdown').dataset.key;

    let url = '/stats/breakdown?';
    if (year && year != 'all') url = url + 'year=' + year;
    if (course && course != 'all') url = url + '&course=' + course;
    if (golfer && golfer != 'all') url = url + '&golfer=' + golfer;
    window.location.href = url;
}

const observer = new MutationObserver((mutationsList, observer) => {
    for (const mutation of mutationsList) {
        if (mutation.type === 'attributes' && mutation.attributeName === 'data-key') {
            updateContent();
        }
    }
});
const course = document.getElementById('course-dropdown');
const year = document.getElementById('year-dropdown');
const golfer = document.getElementById('golfer-dropdown');
observer.observe(course, { attributes: true });
observer.observe(year, { attributes: true });
observer.observe(golfer, { attributes: true });

function renderBreakdown(labels, values) {
    const ctx = document.getElementById('myChart').getContext('2d');
    const colors = [
        'rgba(85, 127, 181, 0.8)',
        'rgba(56, 101, 158, 0.8)',
        'rgba(114, 114, 114, 0.8)',
        'rgba(196, 135, 106, 0.8)',
        'rgba(200, 107, 66, 0.8)',
        'rgba(177, 77, 34, 0.8)'
    ]
    const myChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Score Type',
                data: values, // Replace with your actual data values
                backgroundColor: colors,
                borderColor: colors,
                borderWidth: 1
            }]
        },
        options: {
            plugins: {
                legend: {
                    display: false
                }
            },
            indexAxis: 'x',
            scales: {
                x: {
                    beginAtZero: true
                }
            }
        }
    });
}
