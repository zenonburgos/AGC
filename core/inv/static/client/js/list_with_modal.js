var tblClient;

function getData() {
    tblClient = $('#zero-config').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        ajax: {
            url: window.location.pathname,
            type: 'POST',
            data: {
                'action': 'searchdata'
            },
            dataSrc: ""
        },
        columns: [
            {"data": "id"},
            {"data": "name"},
            {"data": "surname"},
            {"data": "dni"},
            {"data": "date_of_birth"},
            {"data": "gender.name"},
            {"data": "active"},
            {"data": "id"},
        ],
        columnDefs: [
            {
                targets: [-2],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    // console.log(data)
                    // console.log(row)

                    if(row.active){
                        return '<span class="badge badge-success">Activo</span>';
                    }
                    return '<span class="badge badge-danger">Inactivo</span>';
                }
            },
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    htm = '<div class="btn-group">';
                    htm += '<a href="#' + row.id + '/" rel="edit" class="btn btn-dark btn-sm">Editar</a>';
                    htm += '<button type="button" class="btn btn-dark btn-sm dropdown-toggle dropdown-toggle-split" id="dropdownMenuReference17" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false" data-reference="parent">';
                    htm += '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-chevron-down">';
                    htm += '<polyline points="6 9 12 15 18 9"></polyline></svg></button>';
                    htm += '<div class="dropdown-menu" aria-labelledby="dropdownMenuReference17">';
                    htm += (row.active ? '<a class="dropdown-item" href="#" rel="delete"' + row.id + '/">Inactivar</a>' :
                    '<a class="dropdown-item" href="#" rel="activar"' + row.id + '/">Activar</a>');
                    htm += '</div>';
                    htm += '</div>';
                    return htm;

                    // var buttons = '<a href="/inv/category/update/' + row.id + '/" class="btn btn-warning btn-xs btn-flat"><i class="fas fa-edit"></i></a> ';
                    // buttons += '<a href="/inv/category/delete/' + row.id + '/" type="button" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash-alt"></i></a>';
                    // return buttons;


                }
            },
        ],
        initComplete: function (settings, json) {

        },

        "dom": "<'dt--top-section'<'row'<'col-12 col-sm-6 d-flex justify-content-sm-start justify-content-center'l><'col-12 col-sm-6 d-flex justify-content-sm-end justify-content-center mt-sm-0 mt-3'f>>>" +
            "<'table-responsive'tr>" +
            "<'dt--bottom-section d-sm-flex justify-content-sm-between text-center'<'dt--pages-count  mb-sm-0 mb-3'i><'dt--pagination'p>>",
        "oLanguage": {
            "oPaginate": {
                "sPrevious": '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-arrow-left"><line x1="19" y1="12" x2="5" y2="12"></line><polyline points="12 19 5 12 12 5"></polyline></svg>',
                "sNext": '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-arrow-right"><line x1="5" y1="12" x2="19" y2="12"></line><polyline points="12 5 19 12 12 19"></polyline></svg>'
            },
            "sInfo": "Mostrando página _PAGE_ de _PAGES_",
            "sSearch": '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-search"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>',
            "sSearchPlaceholder": "Buscar...",
            "sZeroRecords": "No se encontraron resultados",
            "sInfoEmpty": "Mostrando registros del 0 al 0 de un total de 0 registros",
            "sInfoFiltered": "(filtrado de un total de _MAX_ registros)",
            "sInfoPostFix": "",
            "sSearch": "Buscar:",
            "sUrl": "",
            "sInfoThousands": ",",
            "sLoadingRecords": "Cargando...",
            "order": [[0, "desc"]],
            "oAria": {
                "sSortAscending": ": Activar para ordenar la columna de manera ascendente",
                "sSortDescending": ": Activar para ordenar la columna de manera descendente"
            },
            "sLengthMenu": "Resultados :  _MENU_",
        },
        "stripeClasses": [],
        "lengthMenu": [7, 10, 20, 50],
        "pageLength": 7,
        order: [[0, 'desc']],
    });
}

$(function () {

    modal_title = $('.modal-title');

    getData();

    $('.btnAdd').on('click', function () {
        $('input[name="action"]').val('add');
        modal_title.find('span').html('Nuevo Cliente');

        $('#myModalClient').modal('show');
    });

    $('#zero-config tbody')
        .on('click', 'a[rel="edit"]', function () {
            modal_title.find('span').html('Edición de Cliente');

            var tr = tblClient.cell($(this).closest('td, li')).index();
            var data = tblClient.row(tr.row).data();
            $('input[name="action"]').val('edit');
            $('input[name="id"]').val(data.id);
            $('input[name="name"]').val(data.name);
            $('input[name="surname"]').val(data.surname);
            $('input[name="dni"]').val(data.dni);
            $('input[name="date_of_birth"]').val(data.date_of_birth);
            $('input[name="address"]').val(data.address);
            $('input[name="gender"]').val(data.gender.id);
            //$('input[name="active"]').prop("checked", data.active);

            $('#myModalClient').modal('show');
            console.log(data);
        })
        .on('click', 'a[rel="delete"]', function () {
            var tr = tblClient.cell($(this).closest('td, li')).index();
            var data = tblClient.row(tr.row).data();
            //console.log(data);
            var parameters = new FormData();
            parameters.append('action', 'delete');
            parameters.append('id', data.id);
            submit_with_ajax(window.location.pathname, 'Notificación', '¿Estas seguro de inactivar el siguiente registro?', parameters, function () {
                tblClient.ajax.reload();
            });
        }).on('click', 'a[rel="activar"]', function () {
            var tr = tblClient.cell($(this).closest('td, li')).index();
            var data = tblClient.row(tr.row).data();
            //console.log(data);
            var parameters = new FormData();
            parameters.append('action', 'activar');
            parameters.append('id', data.id);
            submit_with_ajax(window.location.pathname, 'Notificación', '¿Estas seguro de activar el siguiente registro?', parameters, function () {
                tblClient.ajax.reload();
            });
        });

    // $('#myModalClient').on('shown.bs.modal', function(){
    //     $('form')[0].reset();
    // });

    $('#myModalClient').on('hidden.bs.modal', function () {
        $(this).find('form').trigger('reset');
    })

    $('form').on('submit', function (e) {
        e.preventDefault();

        var parameters = new FormData(this);
        submit_with_ajax(window.location.pathname, 'Notificación', '¿Estas seguro de realizar la siguiente acción?', parameters, function () {
            $('#myModalClient').modal('hide');
            tblClient.ajax.reload();
            //getData();
        });
    });
});