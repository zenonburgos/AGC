var dateFrom = null;
var dateTo = null;
var date_now = new Date();
date_now = String(date_now.getFullYear() + '-' + String(date_now.getMonth() + 1).padStart(2, '0') + '-' + date_now.getDate()).padStart(2, '0');
console.log(date_now);

function generate_report() {
    var parameters = {
        'action': 'search_report',
        'start_date': date_now,
        'end_date': date_now,
    };

    if (dateFrom !== null) {
        parameters['start_date'] = dateFrom
        parameters['end_date'] = dateTo
    }

    $('#html5-extension').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        ajax: {
            url: window.location.pathname,
            type: 'POST',
            data: parameters,
            dataSrc: ""
        },
        order: false,
        // paging: false,
        // ordering: false,
        // info: false,
        // searching: false,

        // columns: [
        //     {"data": "id"},
        //     {"data": "name"},
        //     {"data": "slug"},
        //     {"data": "slug"},
        // ],
        columnDefs: [
            {
                targets: [-1, -2, -3],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    return '$' + parseFloat(data).toFixed(2);
                }
            },
        ],
        initComplete: function (settings, json) {

        },

        "dom": "<'dt--top-section'<'row'<'col-sm-12 col-md-6 d-flex justify-content-md-start justify-content-center'B><'col-sm-12 col-md-6 d-flex justify-content-md-end justify-content-center mt-md-0 mt-3'f>>>" +
            "<'table-responsive'tr>" +
            "<'dt--bottom-section d-sm-flex justify-content-sm-between text-center'<'dt--pages-count  mb-sm-0 mb-3'i><'dt--pagination'p>>",
        buttons: {
            buttons: [
                {extend: 'copy', className: 'btn btn-sm'},
                {extend: 'csv', className: 'btn btn-sm'},
                {extend: 'excel', className: 'btn btn-sm'},
                {extend: 'print', className: 'btn btn-sm'}
            ]
        },
        "oLanguage": {
            "oPaginate": {
                "sPrevious": '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-arrow-left"><line x1="19" y1="12" x2="5" y2="12"></line><polyline points="12 19 5 12 12 5"></polyline></svg>',
                "sNext": '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-arrow-right"><line x1="5" y1="12" x2="19" y2="12"></line><polyline points="12 5 19 12 12 19"></polyline></svg>'
            },
            "sInfo": "Showing page _PAGE_ of _PAGES_",
            "sSearch": '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-search"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>',
            "sSearchPlaceholder": "Search...",
            "sLengthMenu": "Results :  _MENU_",
        },
        "stripeClasses": [],
        "lengthMenu": [7, 10, 20, 50],
        "pageLength": 7
    });
}

$(function () {
    var f3 = flatpickr(document.getElementById('rangeCalendarFlatpickr'), {
        mode: "range",
        defaultDate: "today",
        locale: 'es',
        onClose: function (selectedDates, dateStr, instance) {

            if (selectedDates.length == 1) {
                instance.setDate([selectedDates[0], selectedDates[0]], true);
                dateFrom = dateStr;
                dateTo = dateStr;
            } else {
                if (dateStr.includes("a")) {
                    dateFrom = dateStr.substring(0, dateStr.indexOf("a")).trim();
                    dateTo = dateStr.substring(dateStr.indexOf("a") + 1).trim();
                } else {
                    dateFrom = dateStr;
                    dateTo = dateStr;
                }
            }

            generate_report();
            //console.log(dateTo);
            console.log(date_now);
        },
    });

    generate_report();
});