var iva = 0.00;

$(document).ready(function () {

    //======================EN INDEX Y STORE ======================//
    //Add to cart en index.html y store.html
    //Creo que no se utiliza en ningún lado, revisar
    $(".add_to_cart_from_home").on("click", function (e) {
		e.preventDefault();
		producto_id = $(this).attr('data-id');
        
        product_qty = 1
        
        url = $(this).attr('data-url');
        data = {
            producto_id: producto_id,
            product_qty: product_qty
        }

        $.ajax({
            type: 'GET',
            url: url,
            data: data,            
            success: function(response){
                console.log(response)
                if(response.status == 'login_required'){
                    swal(response.message, '', 'info').then(function(){
                        window.location = '/login';
                    })
                }if(response.status == 'Failed'){
                    swal(response.message, '', 'error')
                }else{
                    $('#cart_counter').html(response.cart_counter['cart_count']); //Modifica contador carrito en frontend (navbar.html)
                    $('#cart_amount').html(response.cart_amount['grand_total']); //Modifica contador carrito en frontend (navbar.html)
                    toastr["success"]("", "Producto agregado al Carrito.")
                }
            }
        })
	});
    
    //=========================FIN HOME Y STORE==========================//

    //======================EN PRODUCT DETAIL ======================//
    //Add to cart en product_detail, home y store
    $(".adding_to_cart").on("click", function (e) {
        e.preventDefault();
        
        producto_id = $(this).attr('data-id');
        if(window.location.pathname == '/product_detail/'){
            product_qty = $('#cant').val();
        }else{
            product_qty = 1;
        }
        
        url = $(this).attr('data-url');
        data = {
            producto_id: producto_id,
            product_qty: product_qty
        }
        
        $.ajax({
            type: 'GET',
            url: url,
            data: data,            
            success: function(response){
                //console.log(response)
                if(response.status == 'login_required'){
                    swal(response.message, '', 'info').then(function(){
                        window.location = '/login';
                    })
                }if(response.status == 'Failed'){
                    swal(response.message, '', 'error')
                }else{
                    $('#cart_counter').html(response.cart_counter['cart_count']); //Modifica contador carrito en frontend (navbar.html)
                    $('#cart_amount').html(response.cart_amount['grand_total']); //Modifica contador carrito en frontend (navbar.html)
                    toastr["success"]("", "Producto agregado al Carrito.")
                }
            }
        })
    })
     
    // Botones aumenta y disminuye cantidades
    // en página Product Detail
    var i;
    var stock = parseInt($('.stock').attr('data-stock'));
    $('.plus').click(function(){
        i=parseInt($('#cant').val());
        if(i < stock) {
            i=i+1;
        }else{
            swal('¡Felicidades! Estás a punto de llevarte nuestro último producto de este modelo. Puedes seguir comprando o revisar tu cesta.', '', 'success')
            // alert('¡Felicidades! Estás a punto de llevarte nuestro último producto de este modelo.')
        }
        $('#cant').val(i);
        
    })
    $('.minus').click(function(){
        i=parseInt($('#cant').val());
        i=i-1;
        if(i<1){
            i=1;
        }
        $('#cant').val(i);
    })
    //=========================FIN PRODUCT DETAIL==========================//



    //================EN CART PAGE (PÁGINA DEL CARRITO) ================//
    // place the cart item quantity on LOAD
    // Esto lo toma del span oculto en product_detail que trae las cantidades
    // en forma de array, por eso se recorre a continuación

    $('.item_qty').each(function(){
        if(window.location.pathname == '/cart/'){
            var prod_id = $(this).attr('data-idprod')
            var the_id = $(this).attr('id') //qty-idproducto (qty-968, qty-510, etc)
            var qty = $(this).attr('data-qty')
            var the_price = $(this).attr('data-price')
            linetotal = parseInt(qty) * parseFloat(the_price)
            $('#'+the_id).val(qty) //Esto era para poner cantidad según carrito
            $('#sub-'+prod_id).html(linetotal.toFixed(2)) //Esto era para poner cantidad según carrito
        }
    })
    
    //Add to cart
    $(".add_to_cart").on("click", function (e) {
        e.preventDefault();
        producto_id = $(this).attr('data-id');        
        url = $(this).attr('data-url');
        data = {
            producto_id: producto_id,
        }
        
        $.ajax({
            type: 'GET',
            url: url,
            data: data,
            success: function(response){
                console.log(response)
                if(response.status == 'login_required'){
                    swal(response.message, '', 'info').then(function(){
                        window.location = '/login';
                    })
                }else if(response.status == 'Failed'){
                    swal(response.message, '', 'error')
                }else{
                    
                    $('#cart_counter').html(response.cart_counter['cart_count']); //Modifica contador carrito en frontend (navbar.html)
                    $('#cart_amount').html(response.cart_amount['grand_total']); //Modifica contador carrito en frontend (navbar.html)
                    $('#qty-'+producto_id).val(response.qty); //poner cantidad según carrito
                    $('#sub-'+producto_id).html(response.pricecart);
                    
                    cart_totals()
                }
            }
        })
        
    })
    
    //Decrease cart
    $(".decrease_cart").on("click", function (e) {
        e.preventDefault();
        
        producto_id = $(this).attr('data-id');
        url = $(this).attr('data-url');
        cart_id = $(this).attr('id');
        
        $.ajax({
            type: 'GET',
            url: url,
            
            success: function(response){
                console.log(response)
                if(response.status == 'login_required'){
                    swal(response.message, '', 'info').then(function(){
                        window.location = '/login';
                    })
                }else if(response.status == 'Failed'){
                    swal(response.message, '', 'error')
                }else{
                    $('#cart_counter').html(response.cart_counter['cart_count']); //Modifica contador carrito en frontend (navbar.html)
                    $('#cart_amount').html(response.cart_amount['grand_total']); //Modifica contador carrito en frontend (navbar.html)
                    $('#qty-'+producto_id).val(response.qty); //poner cantidad según carrito
                    
                    //Subtotal línea
                    $('#sub-'+producto_id).html(response.pricecart);
                                        
                    cart_totals()

                    if(window.location.pathname == '/cart/'){
                        removeCartItem(response.qty, cart_id);
                        checkEmptyCart();
                    }
                    
                }
            }
        })
    })

    //Delete cart item
    $(".delete_cart").on("click", function (e) {
        e.preventDefault();
        
        cart_id = $(this).attr('data-id');
        url = $(this).attr('data-url');
        
        $.ajax({
            type: 'GET',
            url: url,            
            success: function(response){
                console.log(response)
                if(response.status == 'Failed'){
                    swal(response.message, '', 'error')
                }else{
                    $('#cart_counter').html(response.cart_counter['cart_count']); //Modifica contador carrito en frontend (navbar.html)
                    $('#cart_amount').html(response.cart_amount['grand_total']); //Modifica suma carrito en frontend (navbar.html)
                    toastr["info"]("", response.message)

                    removeCartItem(0, cart_id);
                    checkEmptyCart();

                    cart_totals()
                    
                }
            }
        })
    })


    // delete cart element if qty is 0
    function removeCartItem(cartItemQty, cart_id){
        if(cartItemQty <= 0){
            // remove the cart item element                        
            document.getElementById("cart-item-"+cart_id).remove()
            document.getElementById("cart-item-navbar-"+cart_id).remove()
        }
    }

    // check if the cart is empty in order to display a message
    function checkEmptyCart(){
        var cart_counter = document.getElementById('cart_counter').innerHTML
        var cart_amount =  document.getElementById('cart_amount').innerHTML
        if(cart_counter == 0){
            document.getElementById("empty-cart").style.display = "block";
            $(".shopping-cart").remove();
        }
    }

    function cart_totals(){
        //Defino los totales de mis 2 columnas en 0
        var total_col6 = 0;
        //var total_col2 = 0;
        //Recorro todos los tr ubicados en el tbody
        $('#carrito tbody').find('tr').each(function (i, el) {
                
            //Voy incrementando las variables segun la fila ( .eq(0) representa la fila 1 )     
            //total_col1 += parseFloat($(this).find('td').eq(5).text());
            //alert(total_col1)
            total_col6 += parseFloat($(this).find('td').eq(6).text());            
                    
        });
        //Muestro el resultado en el th correspondiente a la columna
        //$('#carrito tfoot tr th').eq(0).text("Total " + total_col1);
        //$('#carrito tfoot tr th').eq(0).text("Total " + total_col6);

        $('#subtotal').html(total_col6.toFixed(2));
        $('#total').html(total_col6.toFixed(2))
    }

    cart_totals()

    //apply cart amounts
    //Esto pinta los valores en el html
    function applyCartAmounts(subtotal, tax, grand_total){
        if(window.location.pathname == '/cart/'){
            $('#subtotal').html(subtotal)
            // $('#tax').html(tax)
            $('#total').html(grand_total)
        }        
    }

    //========================FIN CART PAGE============================//



    //==================== OPCIONES DEL TOASTER ====================///
    toastr.options = {
        "closeButton": false,
        "debug": false,
        "newestOnTop": false,
        "progressBar": true,
        "positionClass": "toast-top-right",
        "preventDuplicates": false,
        "onclick": null,
        "showDuration": "300",
        "hideDuration": "1000",
        "timeOut": "2000",
        "extendedTimeOut": "1000",
        "showEasing": "swing",
        "hideEasing": "linear",
        "showMethod": "fadeIn",
        "hideMethod": "fadeOut"
      }
})

$('#facebook').click(function() {
    window.open('http://www.facebook.com/sharer.php?u='+window.location.href, '_blank');
});

$('#whatsapp').click(function() {
    window.open('https://api.whatsapp.com/send?text='+window.location.href, '_blank');
});
// $('#whatsapp_product_single').click(function() {
//     window.open('https://wa.me/50377465594?text=Me%20interesa%20este%20producto: %20'+'{{ single_product.code }}', '_blank');
// });

$('#twitter').click(function() {
    window.open('https://twitter.com/intent/tweet?text=MIEpresa&url='+window.location.href, '_blank');
});

$('#linkdin').click(function() {
    window.open('http://www.linkedin.com/shareArticle?url='+window.location.href, '_blank');
});
// $('#youtube').click(function() {
//     window.open('https://twitter.com/intent/tweet?text=MIEpresa&url='+window.location.href, '_blank');
// });