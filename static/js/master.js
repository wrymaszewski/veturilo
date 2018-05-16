$(document).ready(function(){
    // jquery datatables
    $('.datatable').DataTable({
        "scrollY":        "400px",
        "scrollCollapse": true,
        "paging":         false
    });
});

$(window).ready(function() {
    $('#loading').hide();
    $('#loading_div').hide();
});
