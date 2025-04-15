$(document).ready(function() {
    // Function to sort a table by a specific column
    function sortTable(table_id, column, order) {
        //let $table = $('#myTable');
        let $table = $('#' + table_id);
        let $rows = $table.find('tbody tr').detach(); // Detach rows to manipulate them easily

        $rows.sort(function(a, b) {
            let aValue = $(a).find('td').eq(column).text();
            let bValue = $(b).find('td').eq(column).text();

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
        });

        $('#' + table_id + ' tbody').append($rows); // Append sorted rows back to the table
    }

    // Add click handlers to the table headers
    $('th').click(function() {
        if ('sort' in this.dataset) {
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
            let table_id = this.parentElement.parentElement.parentElement.id;
            sortTable(table_id, column, newOrder);
        }
    });

    // Initialize the first column as sorted on page load
    $('th:first-child').addClass('sorted asc');
    $('th:first-child').data('order', 'asc');
});