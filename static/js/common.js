if ($('#industries').length > 0) {
    $('#industries').change(function() {
        refresh_content();
    });
}

function refresh_content() {
    get_filters();
    $("#data-table-employer").bootgrid('reload');
}

function filter() {
	$('.filter-form').submit();
}
