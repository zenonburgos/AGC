var input_is_inventoried;

//Para evitar submit con enter
document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('input[type=text]').forEach( node => node.addEventListener('keypress', e => {
      if(e.keyCode == 13) {
        e.preventDefault();
      }
    }))
});

$(function () {

    // Search brand
    $('select[name="brand"]').select2({
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
                    action: 'search_brands'
                }
                return queryParameters;
            },
            processResults: function (data) {
                return {
                    results: data
                };
            },
        },
        placeholder: 'Enter o click para buscar por marca',
        minimumInputLength: 1,
    });

    $('.btnAddBrand').on('click', function () {
        $('#myModalBrand').modal('show');
    });

    $('#myModalBrand').on('hidden.bs.modal', function (e) {
        $('#frmBrand').trigger('reset');
    })

    $('#frmBrand').on('submit', function (e) {
        e.preventDefault();
        var parameters = new FormData(this);
        parameters.append('action', 'create_brand');
        submit_with_ajax(window.location.pathname, 'Notificación',
            '¿Está seguro de crear una nueva Marca?', parameters, function (response) {
                //console.log(response);
                var newOption = new Option(response.name, response.id, false, true);
                $('select[name="brand"]').append(newOption).trigger('change');
                $('#myModalBrand').modal('hide');
            });
    });    


    // Search categories
    $('select[name="category"]').select2({
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
                    action: 'search_cats'
                }
                return queryParameters;
            },
            processResults: function (data) {
                return {
                    results: data
                };
            },
        },
        placeholder: 'Enter o click para buscar por categoría',
        minimumInputLength: 1,
    });

    $('.btnAddCat').on('click', function () {
        $('#myModalCat').modal('show');
    });

    $('#myModalCat').on('hidden.bs.modal', function (e) {
        $('#frmCategory').trigger('reset');
    })


    
    ///// Manejo de inputs /////
    input_is_inventoried = $('input[name="is_inventoried"]');
    product_cost = $('input[name="cost"]');

    fact1 = $('input[name="fact"]');
    fact2 = $('input[name="fact2"]');
    fact3 = $('input[name="fact3"]');
    
    input_is_inventoried.on('change', function () {
        var container = $(this).parent().parent().parent().parent().parent().find('input[name="stock"]').parent().parent();

        console.log(container);

        $(container).show();
        if (!this.checked) {
             $(container).hide();
        }
    });

    product_cost.on('change', function () {
        var cost = parseFloat($(this).val())*1.13;
        
        //alert($('input[name="price2"]').val() == 0 || $('input[name="price2"]').val() === "")
        
        if($('input[name="price"]').val() == 0 || $('input[name="price"]').val() === ""){
            if($('input[name="fact"]').val() > 0){
                var price1 = parseFloat(cost/fact1.val()).toFixed(2);
                $("#id_price").val(price1);
            }
        }

        if($('input[name="price2"]').val() == 0 || $('input[name="price2"]').val() === ""){            
            if($('input[name="fact2"]').val() > 0){            
                var price2 = parseFloat(cost/fact2.val()).toFixed(2);
                $("#id_price2").val(price2);
            }
        }

        if($('input[name="price3"]').val() == 0 || $('input[name="price3"]').val() === ""){
            if($('input[name="fact3"]').val() > 0){            
                var price3 = parseFloat(cost/fact3.val()).toFixed(2);
                $("#id_price3").val(price3);
            }
        }

        incons_precio();
        
        // if($(this).val() == 0){            
        //     $("#id_price").val(0);
        // }

        // if(fact1.val() == 0){
        //     parseFloat($("#id_price").val(0)).toFixed(2);
        // }

    });    

    fact1.on('change', function () {
        var cost = parseFloat($('input[name="cost"]').val())*1.13;
        
        var price1 = parseFloat(cost/$(this).val()).toFixed(2);
        if($(this).val() > 0){
            $("#id_price").val(price1);
        }

    });

    fact2.on('change', function () {
        var cost = parseFloat($('input[name="cost"]').val())*1.13;
        
        var price2 = parseFloat(cost/$(this).val()).toFixed(2);
        if($(this).val() > 0){
            $("#id_price2").val(price2);
        }
    });
    fact3.on('change', function () {
        var cost = parseFloat($('input[name="cost"]').val())*1.13;
        
        var price3 = parseFloat(cost/$(this).val()).toFixed(2);
        if($(this).val() > 0){
            $("#id_price3").val(price3);
        }
    });

    if($('input[name="action"]').val() === 'edit'){
        input_is_inventoried.trigger('change');
    }

    //Botón actualizar precios
    $('#actualizaPrecios').on('click', function () {
        var cost = parseFloat($('input[name="cost"]').val())*1.13;

        var price1 = parseFloat(cost/fact1.val()).toFixed(2);
        $("#id_price").val(price1);
        var price2 = parseFloat(cost/fact2.val()).toFixed(2);
        $("#id_price2").val(price2);
        var price3 = parseFloat(cost/fact3.val()).toFixed(2);
        $("#id_price3").val(price3);

        incons_precio();
    });

    incons_precio();
    
});

function incons_precio() {
    //Aviso inconsistencia precios
    if(parseFloat(($('input[name="cost"]').val()*1.13)/fact1.val()).toFixed(2) != $("#id_price").val()){
        $('.incons_precio').show();
    }else{
        $('.incons_precio').hide();
    }

    if(parseFloat(($('input[name="cost"]').val()*1.13)/fact2.val()).toFixed(2) != $("#id_price2").val()){
        $('.incons_precio').show();
    }else{
        $('.incons_precio').hide();
    }

    if(parseFloat(($('input[name="cost"]').val()*1.13)/fact3.val()).toFixed(2) != $("#id_price3").val()){
        $('.incons_precio').show();
    }else{
        $('.incons_precio').hide();
    }
}

// document.getElementById('id_fact').onchange = function() {
//     var cost = parseFloat(document.getElementById('id_cost').value);
//     var new_cost = cost.toFixed(2);
//     document.getElementById('id_price').value = new_cost;
// };