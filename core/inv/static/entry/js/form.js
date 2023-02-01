var tblProducts;
var tblSearchProducts;
var itemno = 0;
var select_search_product;
var ents = {
    //Datos de Cabecera de factura
    items: {
        supplier: '',
        date_joined: '',
        doc: '',
        doc_ser: '',
        doc_num: '',
        nulled: false,
        supplier_doc_num: '',
        subtotal: 0.00,
        iva: 0.00,
        total: 0.00,
        products: []
    },
    
    getProductsIds: function () {
        return this.items.products.map(value => value.id);
    },
    calculateInvoice: function () {
        var subtotal = 0.00;
        var iva = $('input[name="iva"]').val();
        this.items.products.forEach(function (value, index, array) {
            value.index = index;
            value.cant = parseInt(value.cant);
            value.subtotal = value.cant * parseFloat(value.cost);
            subtotal += value.subtotal;
        });

        this.items.subtotal = subtotal;
        this.items.iva = this.items.subtotal * iva;
        this.items.total = this.items.subtotal + this.items.iva;

        $('input[name="subtotal"]').val(this.items.subtotal.toFixed(2));
        $('input[name="ivacalc"]').val(this.items.iva.toFixed(2));
        $('input[name="total"]').val(this.items.total.toFixed(2));
    },
    
    add: function (item) {
        this.items.products.push(item);
        this.list();
    },
    list: function () {
        this.calculateInvoice();

        tblProducts = $('.tblProducts').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            deferRender: true,
            data: this.items.products,
            columns: [
                {"data": "itemno"},
                {"data": "code"},
                {"data": "name"},
                {"data": "cant"},
                {"data": "cost"},
                {"data": "subtotal"},
                {"data": "id"},
            ],
            columnDefs: [
                {
                    targets: [-7],
                    visible: false,
                },
                {
                    targets: [-6],
                    class: 'text-left',
                    orderable: false,
                },
                // Era para stock
                // {
                //     targets: [-5],
                //     class: 'text-center',
                //     render: function (data, type, row) {
                //         if(!row.is_inventoried) {
                //             return '<span class="badge badge-warning">Sin Stock</span>';
                //         }
                //         return '<span class="badge badge-secondary">' + data + '</span>';
                //     }
                // },                
                {
                    targets: [-5],
                    class: 'text-left',
                    orderable: false,
                    render: function (data, type, row) {
                        capitalized = data.charAt(0).toUpperCase() + data.slice(1).toLowerCase().substring(0,60)
                        htm = '<div title="">';
                        htm += capitalized;
                        htm += '</div>';

                        return htm;
                    }
                },
                {
                    targets: [-3],
                    class: 'text-left',
                    orderable: false,
                    render: function (data, type, row) {
                        // return '$'+parseFloat(data).toFixed(2);
                        return '<input type="text" name="cost" class="form-control form-control-sm input-sm inputNum" autocomplete="off" value="' + parseFloat(row.cost).toFixed(2) + '" style="padding:5px; font-size:12px;">';
                    }
                },
                {
                    targets: [-4],
                    class: 'text-left',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<input type="text" name="cant" class="form-control form-control-sm" autocomplete="off" value="' + row.cant + '" style="padding: 5px; font-size:12px;">'
                    }
                },
                {
                    targets: [-2],
                    class: 'text-right',
                    orderable: false,
                    render: function (data, type, row) {
                        //return '<input type="text" name="subtotal" class="form-control form-control-sm" autocomplete="off" value="' + data + '" style="font-size:12px;">'
                        return '$' + parseFloat(data).toFixed(2);
                    }
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return button = '<a rel="remove" class="btn btn-danger btn-sm">x</a>';
                    }
                },
            ],

            rowCallback(row, data, displayNum, displayIndex, dataIndex) {
                // console.log(row);
                // console.log(data);
                $(row).find('input[name="cant"]').TouchSpin({
                    min: 1,
                    max: 1000000,
                    //max: data.is_inventoried ? row.stock: 1000000,
                    step: 1,
                    verticalbuttons: true,
                });
                // $(row).find('input[name="cost"]').TouchSpin({
                //     min: 0,
                //     max: 10000000,
                //     decimals: 2,
                //     step: 1,
                //     verticalbuttons: true,
                // });
            },
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
                //"sSearchPlaceholder": "Buscar...",
                "sZeroRecords": "No se encontraron resultados",
                "sInfoEmpty": "Mostrando registros del 0 al 0 de un total de 0 registros",
                "sInfoFiltered": "(filtrado de un total de _MAX_ registros)",
                "sInfoPostFix": "",
                //"sSearch": "Buscar:",
                "sUrl": "",
                "sInfoThousands": ",",
                "sLoadingRecords": "Cargando...",
                "order": [[0, "asc"]],
                "oAria": {
                    "sSortAscending": ": Activar para ordenar la columna de manera ascendente",
                    "sSortDescending": ": Activar para ordenar la columna de manera descendente"
                },
                "sLengthMenu": "Resultados :  _MENU_",
            },
            "stripeClasses": [],
            "lengthMenu": [7, 10, 20, 50],
            "pageLength": 7,

        });
        //var xfecha = localStorage.getItem("xfecha");
        //console.log(this.items);
        //console.log(this.get_ids());        
    }
};

var modo = $('input[name="action"]').val()
var tipomov = $('input[name="tipomov"]').val() //El input hidden en create.html

if(modo === 'add'){
    var id_tipomov = $('input[name="id_tipomov"]').val() //El input hidden en create.html
    //document.getElementById("id_doc").value = 1;
    $("#id_doc").val(id_tipomov);
}

function formatRepo(repo) {
    if (repo.loading) {
        return repo.text;
    }

    if (!Number.isInteger(repo.id)) {
        return repo.text;
    }

    var stock = repo.is_inventoried ? repo.stock : 'No maneja stock';

    var option = $(
        '<div class="wrapper container">' +
        '<div class="row">' +
        '<div class="col-lg-1">' +
        '<img src="' + repo.image + '" class="img-fluid img-thumbnail d-block mx-auto rounded">' +
        '</div>' +
        '<div class="col-lg-11 text-left shadow-sm">' +
        //'<br>' +
        '<p style="margin-bottom: 0;">' +
        '<b>Nombre:</b> ' + repo.full_name + '<br>' +
        '<b>Código:</b> ' + repo.code + '<br>' +
        '<b>Stock: </b>' + stock + '<br>' +
        '<b>Costo:</b> <span class="badge badge-warning">$' + repo.cost + '</span>' +
        '</p>' +
        '</div>' +
        '</div>' +
        '</div>');

    return option;
}

$(function () {
    select_search_product = $('select[name="search_product"]');    

    $(".placeholder").select2({
        placeholder: "Seleccione",
        allowClear: true,
        language: "es"
    });

    // $('#date_joined').datetimepicker();

    $(".sidebarCollapse").click(); //Colapsar barra lateral

    configFlatpickr = {
        locale: {
            firstDayOfWeek: 1,
            weekdays: {
                shorthand: ['Do', 'Lu', 'Ma', 'Mi', 'Ju', 'Vi', 'Sa'],
                longhand: ['Domingo', 'Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado'],
            },
            months: {
                shorthand: ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Оct', 'Nov', 'Dic'],
                longhand: ['Enero', 'Febreo', 'Мarzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'],
            },
        },
        //dateFormat: "d-m-Y",
        altInput: true,
        altFormat: "F j, Y",
        dateFormat: "Y-m-d",
    }
    
    if(modo == "add"){
        $("#date").val(localStorage.getItem("xfecha"))
        $("#id_doc_num" ).val(parseInt($("#numdoc").val())+1);
    }
    flatpickr("#date", configFlatpickr);

    $("input[name='iva']").TouchSpin({
        min: 0,
        max: 100,
        step: 0.01,
        decimals: 2,
        boostat: 5,
        maxboostedstep: 10,
        verticalbuttons: true,
    }).on('change', function () {
        // console.clear()
        // console.log($(this).val());
        ents.calculateInvoice();
    }).val(0.13);

    // Search suppliers
    $('select[name="supplier"]').select2({
        theme: "bootstrap4",
        language: 'es',
        allowClear: true,
        ajax: {
            delay: 250,
            type: 'POST',
            url: pathname,
            headers: {
                'X-CSRFToken': csrftoken
            },
            data: function (params) {
                var queryParameters = {
                    term: params.term,
                    action: 'search_suppliers'
                }
                return queryParameters;
            },
            processResults: function (data) {
                return {
                    results: data
                };
            },
        },
        placeholder: 'Busque por RAZÓN SOCIAL, NRC, NIT...',
        minimumInputLength: 1,
    });

    $('.btnAddSupplier').on('click', function () {
        $('#myModalSupplier').modal('show');
    });

    $('#myModalSupplier').on('hidden.bs.modal', function (e) {
        $('#frmSupplier').trigger('reset');
    })

    $('#frmSupplier').on('submit', function (e) {
        e.preventDefault();
        var parameters = new FormData(this);
        parameters.append('action', 'create_supplier');
        submit_with_ajax(window.location.pathname, 'Notificación',
            '¿Está seguro de crear un nuevo proveedor?', parameters, function (response) {
                //console.log(response);
                var newOption = new Option(response.full_name, response.id, false, true);
                $('select[name="supplier"]').append(newOption).trigger('change');
                $('#myModalSupplier').modal('hide');
            });
    });    

    $('.btnRemoveAll').on('click', function () {
        if (ents.items.products.length === 0) return false;
        alert_action('Notificación', '¿Seguro de eliminar todos los items del detalle?', function () {
            ents.items.products = [];
            ents.list();
        }, function () {

        });
    });

    // Evento cantidad, remove y cost
    $('.tblProducts tbody')
        .on('click', 'a[rel="remove"]', function () {
            var tr = tblProducts.cell($(this).closest('td, li')).index();
            ents.items.products.splice(tr.row, 1);
            tblProducts.row(tr.row).remove().draw();
            ents.calculateInvoice();
        })
        .on('change keyup', 'input[name="cant"]', function () {
            if (isNaN(parseInt(this.value))) {
                this.value = 1;
            }
            var cant = parseInt($(this).val());
            var tr = tblProducts.cell($(this).closest('td, li')).index();            

            ents.items.products[tr.row].cant = cant;

            console.log(ents.items.products);
            ents.calculateInvoice();
            $('td:eq(4)', tblProducts.row(tr.row).node()).html('$' + ents.items.products[tr.row].subtotal.toFixed(2));
        }).on('change keyup', 'input[name="cost"]', function () {
        if (isNaN(parseInt(this.value))) {
            this.value = 0;
        }
        var cost = parseFloat($(this).val());
        var tr = tblProducts.cell($(this).closest('td, li')).index();
        ents.items.products[tr.row].cost = cost;
        ents.calculateInvoice();
        $('td:eq(4)', tblProducts.row(tr.row).node()).html('$' + ents.items.products[tr.row].subtotal.toFixed(2));
    });

    $('.btnClearSearch').on('click', function () {
        $('select[name="search_product"]').val('').focus();
    });


    //////// Modal de búsqueda de productos //////////
    $('.btnSearchProducts').on('click', function () {
        tblSearchProducts = $('#tblSearchProducts').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            deferRender: true,
            ajax: {
                url: window.location.pathname,
                type: 'POST',
                data: {
                    'action': 'search_products',
                    // 'ids': JSON.stringify(ents.get_ids()),
                    ids: JSON.stringify(ents.getProductsIds()),
                    'term': $('select[name="search_product"]').val()
                },
                dataSrc: "",
                headers: {
                    'X-CSRFToken': csrftoken
                }
            },
            columns: [
                {"data": 'itemno'},
                {"data": "name"},
                {"data": "image"},
                {"data": "cost"},
                {"data": "stock"},
                {"data": "id"},
            ],
            columnDefs: [
                {
                    targets: [-4],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<img src="' + data + '" class="img-fluid rounded-circle" style="width: 20px; height: 20px;">';
                    }
                },
                {
                    targets: [-2],
                    class: 'text-center',
                    render: function (data, type, row) {
                        if(!row.is_inventoried) {
                            return '<span class="badge badge-warning">Sin Stock</span>';
                        }
                        return '<span class="badge badge-secondary">' + data + '</span>';
                    }
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        htm = '<div class="btn-group">';
                        htm += '<a rel="add" class="btn btn-dark btn-sm">+</a>';
                        htm += '</div>';
                        htm += '</div>';
                        return htm;

                        // var buttons = '<a href="/inv/product/update/' + row.id + '/" class="btn btn-warning btn-xs btn-flat"><i class="fas fa-edit"></i></a> ';
                        // buttons += '<a href="/inv/product/delete/' + row.id + '/" type="button" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash-alt"></i></a>';
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
        $('#myModalSearchProducts').modal('show');
    });

    $('#tblSearchProducts tbody')
    .on('click', 'a[rel="add"]', function () {
        itemno += 1;
        var tr = tblSearchProducts.cell($(this).closest('td, li')).index();
        var product = tblSearchProducts.row(tr.row).data();
        product.itemno = itemno;
        product.cant = 1;
        product.subtotal = 0.00;
        ents.add(product);
        tblSearchProducts.row($(this).parents('tr')).remove().draw();
    });

    var anulado = document.getElementById('id_nulled');
    var supplier = document.getElementById('id_supplier');

    anulado.addEventListener("change", siEsAnulado, false);
    
    //Doc select
    tipodocSelect = $('select[name="doc"]');
    
    tipodocSelect.on('change', function () {
        console.log(this.value)
    });
    
    function siEsAnulado()
    {
        var checked = anulado.checked;
        if(checked){
            $('#searchproducts').prop('disabled', true);
            
            //Si no hay items en detalles solo nos salimos
            if (ents.items.products.length === 0) return false;
            
            if (confirm("Al ingresar como NULO se borrarán los productos del detalle, ¿Desea continuar?")) {
                ents.items.products = [];
                ents.list();
            }else{
                $(this).prop('checked', false);
                $('#searchproducts').prop('disabled', false);
            }
            
        }else{
            $('#searchproducts').prop('disabled', false);
        }
    }

    //event submit
    $('#frmEntry').on('submit', function (e) {
        e.preventDefault();

        /******** VALIDACIONES ***************/

        if( $('#id_nulled').is(':checked') != true){
            if (ents.items.products.length === 0 ) {
                message_error('Debe al menos tener un item en su detalle');                
                return false;
            }
        }

        if(supplier.value === '' && tipomov == 'HDE'){ // Si no se ha especificado proveedor         
            if(anulado.checked === false){ // Y si el documento no es anulado
                // Disparamos mensaje porque no pueden ir documentos no anulados sin proveedor
                message_error('Debe elegir al menos "COMPRAS VARIAS" como proveedor.');
                return false;
            }
        }

        // if( $('#id_supplier').is(':checked') != true){
        //     if (ents.items.products.length === 0 ) {
        //         message_error('Debe al menos tener un item en su detalle');                
        //         return false;
        //     }
        // }

        //var anulado = document.getElementById("id_nulled");

        ents.items.date_joined = $('input[name="date_joined"]').val();
        ents.items.doc = $('select[name="doc"]').val();
        ents.items.doc_ser = $('input[name="doc_ser"]').val();
        ents.items.doc_num = $('input[name="doc_num"]').val();
        ents.items.nulled = anulado.checked;
        ents.items.supplier = $('select[name="supplier"]').val();
        ents.items.supplier_doc_num = $('input[name="supplier_doc_num"]').val();

        localStorage.setItem("xfecha", ents.items.date_joined);
        console.log(ents)
        
        var parameters = new FormData();
        parameters.append('action', $('input[name="action"]').val())
        parameters.append('tipomov', $('input[name="tipomov"]').val())
        parameters.append('ents', JSON.stringify(ents.items));
        submit_with_ajax(window.location.pathname,
            'Notificación', '¿Estas seguro de guardar los cambios?', parameters, function (response) {
                // alert_action('Notificación', '¿Desea imprimir el comprobante?', function () {
                //     window.open('/inv/entry/invoice/pdf/' + response.id + '/', '_blank');
                //     location.href = '/inv/entry/list';
                // }, function () {
                //     location.href = '/inv/entry/list';
                // });
                location.href = '/inv/entry/list/'+tipomov+'/';

        });
    });

    ents.list();

    // Select productos autocomplete
    select_search_product.select2({
        theme: "bootstrap4",
        language: 'es',
        allowClear: true,
        ajax: {
            delay: 250,
            type: 'POST',
            url: pathname,
            headers: {
                'X-CSRFToken': csrftoken
            },
            data: function (params) {
                var queryParameters = {
                    term: params.term,
                    action: 'search_autocomplete',
                    //ids: JSON.stringify(ents.get_ids())
                    ids: JSON.stringify(ents.getProductsIds())
                }
                return queryParameters;
            },
            processResults: function (data) {
                return {
                    results: data
                };
            },
        },
        placeholder: 'Click o Enter para empezar a buscar productos...',
        minimumInputLength: 1,
        templateResult: formatRepo,
    }).on('select2:select', function (e) {
        var data = e.params.data;
        if (!Number.isInteger(data.id)) {
            return false;
        }
        itemno += 1;
        data.itemno = itemno;
        data.cant = 1;
        data.subtotal = 0.00;
        ents.add(data);
        select_search_product.val('').trigger('change.select2');
        //console.log(data);
    });
});

