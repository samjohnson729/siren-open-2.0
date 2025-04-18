$(document).ready(function () {
    // Function to sort a table by a specific column
    function sortTable(column, order) {
        let $table = $('#stats-leaderboard');
        let $rows = $table.find('tbody tr').detach(); // Detach rows to manipulate them easily

        $rows.sort(function (a, b) {
            let aValue = $(a).find('td').eq(column).text().trim(); // Trim whitespace for accurate checks
            let bValue = $(b).find('td').eq(column).text().trim();
        
            const aIsNull = !aValue; // Consider empty strings as null
            const bIsNull = !bValue;
        
            if (aIsNull && bIsNull) {
                return 0; // Both are null, no change in order
            } else if (aIsNull) {
                return 1; // a is null, b is not, so a goes after b
            } else if (bIsNull) {
                return -1; // b is null, a is not, so b goes after a
            } else {
                // Attempt to convert values to numbers for numeric comparison
                let aNum = parseFloat(aValue);
                let bNum = parseFloat(bValue);
        
                if (!isNaN(aNum) && !isNaN(bNum)) { // If both are valid numbers
                    if (order === 'asc') {
                        return aNum - bNum; // Numeric comparison
                    } else {
                        return bNum - aNum; // Numeric comparison
                    }
                } else {
                    // If not numbers, perform string comparison
                    if (order === 'asc') {
                        return aValue.localeCompare(bValue);
                    } else {
                        return bValue.localeCompare(aValue);
                    }
                }
            }
        });

        $('#stats-leaderboard tbody').append($rows); // Append sorted rows back to the table
    }

    // Add click handlers to the table headers
    $('th').click(function () {
        let column = $(this).index(); // Get the index of the clicked header
        let currentOrder = $(this).data('order'); // Get the current sort order
        // Toggle the sort order (asc/desc)
        let newOrder = (currentOrder === 'asc') ? 'desc' : 'asc';
        // Remove 'sorted' and 'asc/desc' classes from all headers
        $('th').removeClass('sorted asc desc');
        // Add 'sorted' and the new order class to the clicked header
        $(this).addClass('sorted ' + newOrder);
        $(this).data('order', newOrder); // Set the data attribute with the new order
        // Sort the table
        sortTable(column, newOrder);
    });

    // Initialize the first column as sorted on page load
    $('th:first-child').addClass('sorted asc');
    $('th:first-child').data('order', 'asc');
});

function updateLeaderboard() {

    var year = document.getElementById('year-dropdown').dataset.key;
    var statistic = document.getElementById('statistic-dropdown').dataset.key;

    let url = '/stats/leaderboard?';
    if (year && year != 'all') url = url + 'year=' + year;
    url = url + '&statistic=' + statistic;
    window.location.href = url;
}

const observer = new MutationObserver((mutationsList, observer) => {
    for (const mutation of mutationsList) {
        if (mutation.type === 'attributes' && mutation.attributeName === 'data-key') {
            updateLeaderboard();
        }
    }
});
const year = document.getElementById('year-dropdown');
const statistic = document.getElementById('statistic-dropdown');
observer.observe(year, { attributes: true });
observer.observe(statistic, { attributes: true });
