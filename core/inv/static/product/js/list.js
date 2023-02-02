var product = {
    list: function () {
        
        table = $('#zero-config').DataTable({     
                   
            responsive: true,
            autoWidth: false,
            destroy: true,
            deferRender: true,
            order: [[8, "asc"]],
            
            ajax: {
                url: pathname,
                type: 'POST',
                data: {
                    'action': 'search'
                },
                dataSrc: "",
                headers: {
                    'X-CSRFToken': csrftoken
                }
            },
            columns: [
                {"data": "tags"},
                {"data": "id"},
                {"data": "name"},
                // {"data": "category.name"},
                {"data": "code"},
                {"data": "brand.name"},
                {"data": "image"},
                // {"data": "is_inventoried"},
                {"data": "stock"},
                {"data": "price"},
                {"data": "last_purchase_date"},
                {"data": "id"},
            ],
            columnDefs: [
                {
                    targets: [-10],
                    visible: false,
                },
                {
                    targets: [-5],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<img src="' + data + '" class="img-fluid rounded-circle" style="width: 20px; height: 20px;">';
                    }
                },
                {
                    targets: [-4],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        // console.log(data);
                        // console.log(row);
                        if (!row.is_inventoried) {
                            return '<span class="badge badge-secondary">Sin stock</span>';
                        }
                        if (row.stock > 0) {
                            return '<span class="badge badge-success">' + data + '</span>'
                        }
                        return '<span class="badge badge-danger">' + data + '</span>'
                    }
                },
                // {
                //     targets: [-4],
                //     class: 'text-center',
                //     orderable: false,
                //     render: function (data, type, row) {
                //         if (row.is_inventoried) {
                //             return '<span class="badge badge-success">Sí</span>'
                //         }
                //         return '<span class="badge badge-warning">No</span>'
                //     }
                // },
                {
                    targets: [-1],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        htm = '<div class="btn-group">';
                        htm += '<a href="/inv/product/update/' + row.id + '/" class="btn btn-dark btn-sm">Editar</a>';
                        htm += '<button type="button" class="btn btn-dark btn-sm dropdown-toggle dropdown-toggle-split" id="dropdownMenuReference17" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false" data-reference="parent">';
                        htm += '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-chevron-down">';
                        htm += '<polyline points="6 9 12 15 18 9"></polyline></svg></button>';
                        htm += '<div class="dropdown-menu" aria-labelledby="dropdownMenuReference17">';
                        htm += '<a class="dropdown-item" href="/inv/product/delete/' + row.id + '/">Eliminar</a>';
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
                "oAria": {
                    "sSortAscending": ": Activar para ordenar la columna de manera ascendente",
                    "sSortDescending": ": Activar para ordenar la columna de manera descendente"
                },
                "sLengthMenu": "Resultados :  _MENU_",
                // "order": [[8, "asc"]],
            },
            "stripeClasses": [],
            "lengthMenu": [7, 10, 20, 50],
            "pageLength": 20,
            // order: [[7, 'asc']],
        });
        
        /*********************/
        //Criterios de Búsqueda
        /*********************/
        $("#iptNombre").keyup(function(){
            table.column($(this).data('index')).search(this.value).draw();
        })
        $("#iptCodigo").keyup(function(){
            table.column($(this).data('index')).search(this.value).draw();
        })
        $("#iptMarca").keyup(function(){
            table.column($(this).data('index')).search(this.value).draw();
        })

        $("#iptStockMayor, #iptStockMenor").keyup(function(){
            table.draw();
        })
        $("#iptPrecioDesde, #iptPrecioHasta").keyup(function(){
            table.draw();
        })

        $.fn.dataTable.ext.search.push(
            function(settings, data, dataIndex){
                var stockMayorQue = parseFloat($("#iptStockMayor").val());
                var stockMenorQue = parseFloat($("#iptStockMenor").val());
            
                var col_stock = parseFloat(data[5]);                

                if((isNaN(stockMayorQue) && isNaN(stockMenorQue)) || 
                    (isNaN(stockMayorQue) && col_stock <= stockMenorQue) ||
                    (stockMayorQue <= col_stock && isNaN(stockMenorQue)) ||
                    (stockMayorQue <= col_stock && col_stock <= stockMenorQue)){
                        return true;
                }

                return false;
            }
            
        )

        $.fn.dataTable.ext.search.push(
            function(settings, data, dataIndex){
                var precioDesde = parseFloat($("#iptPrecioDesde").val());
                var precioHasta = parseFloat($("#iptPrecioHasta").val());

                var col_precio = parseFloat(data[6]);
                
                if((isNaN(precioDesde) && isNaN(precioHasta)) || 
                    (isNaN(precioDesde) && col_precio <= precioHasta) ||
                    (precioDesde <= col_precio && isNaN(precioHasta)) ||
                    (precioDesde <= col_precio && col_precio <= precioHasta)){
                        return true;
                }

                return false;
            }
            
        )

        $("#btnLimpiarBusqueda").on('click', function(){
            $("#iptNombre").val('')
            $("#iptCodigo").val('')
            $("#iptMarca").val('')
            $("#iptStockMayor").val('')
            $("#iptStockMenor").val('')
            $("#iptPrecioDesde").val('')
            $("#iptPrecioHasta").val('')

            table.search('').columns().search('').draw();
        })
    }
};

$(function () {
    product.list();
});
