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
