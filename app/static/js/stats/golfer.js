function updateContent() {
    const golfer = document.getElementById('golfer-dropdown').dataset.key;
    const statistic = document.getElementById('statistic-dropdown').dataset.key;

    let url = '/stats/golfer?'
    url = url + 'golfer=' + golfer;
    url = url + '&statistic=' + statistic;
    window.location.href = url;
}

const observer = new MutationObserver((mutationsList, observer) => {
    for (const mutation of mutationsList) {
        if (mutation.type === 'attributes' && mutation.attributeName === 'data-key') {
            updateContent();
        }
    }
});
const golfer = document.getElementById('golfer-dropdown');
const statistic = document.getElementById('statistic-dropdown');
observer.observe(golfer, { attributes: true });
observer.observe(statistic, { attributes: true });

function renderRadarChart(labels, values) {
    const data = {
        labels: labels,
        datasets: [{
            data: values, // Replace with your actual data values for each axis
            backgroundColor: 'rgba(255, 99, 132, 0.2)',
            borderColor: 'rgb(255, 99, 132)',
            pointBackgroundColor: 'rgb(255, 99, 132)',
            pointBorderColor: '#fff',
            pointHoverBackgroundColor: '#fff',
            pointHoverBorderColor: 'rgb(255, 99, 132)'
        }]
    };

    const config = {
        type: 'radar',
        data: data,
        options: {
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                r: {
                    min: 0,
                    max: 1,
                    beginAtZero: true,
                    ticks: {
                        display: false,
                        stepSize: .25
                    },
                    pointLabels: {
                        font: {
                            size: 18,
                            weight: 'bold',
                        },
                        color: 'black'
                    },
                    grid: {
                        color: 'gray'
                    },
                    angleLines: {
                        color: 'gray'
                    }
                }
            },
        }
    };

    const myChart = new Chart(
        document.getElementById('myRadarChart'),
        config
    );
}
