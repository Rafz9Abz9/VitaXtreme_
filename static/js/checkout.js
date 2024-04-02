// create stripe  card and style
var stripePublicKey = $("#id_stripe_public_key").text().slice(1, -1);
var clientSecret = $("#id_client_secret").text().slice(1, -1);
var stripe = Stripe(stripePublicKey);
var elements = stripe.elements();
var card = elements.create('card');
var errorDiv = document.getElementById('card-errors')



var style = {
    base:{
        color:'#32325d',
        fontFamily:'"Helvetica Neue", Helvetica, san-serif',
        fontSmoothing:'antialiased',
        fontSize:'14px',
        '::placeholder':{
            color:'#aab7c4'
        }
    },
    invalid:{
        colot:'#fa755a',
        iconColor:'#fa755a'
    }
}

card.mount('#card-element', {style:style});

card.addEventListener('change', function (event){
    if(event.error){
        var elem = `
        <span class="icon text-danger">
            <i class="icon-close"></i>
        </span>
        <span class="icon text-danger">  ${event.error.message}</span>
        `
        $(errorDiv).html(elem);
    }else{
        errorDiv.textContent = ""
    }


})

// handle form event
var form = document.getElementById('payment-form')

form.addEventListener('submit', function(ev){
    ev.preventDefault()
    card.update({'disabled': true})
    $('#submit-button').attr('disabled', true)
    var overlay = document.querySelector('.loading-overlay')
    overlay.style.display = 'flex'
    console.log(overlay)
    $('#payment-form').fadeToggle(100);

    var csrfToken = $('input[name="csrfmiddlewaretoken"]').val()
    var first_name = $('input[name="first_name"]').val()
    var last_name = $('input[name="last_name"]').val()
    var email = $('input[name="email"]').val()
    var phone = $('input[name="phone"]').val()
    var street_address = $('input[name="street_address"]').val()
    var post_code = $('input[name="post_code"]').val()
    var city = $('input[name="city"]').val()
    var state = $('input[name="state"]').val()
    var country = $('input[name="country"]').val()
    var shipping_method = $('input[name="shipping_method"]').val()
    var shipping_price = $('input[name="shipping_price"]').val()
    var sub_total = $('input[name="sub_total"]').val()
    var grand_total = $('input[name="grand_total"]').val()
    var postData ={
        'csrfmiddlewaretoken':csrfToken,
        'client_secret':clientSecret,
        'first_name':first_name,
        'last_name':last_name,
        'email':email,
        'post_code':post_code,
        'phone':phone,
        'street_address':street_address,
        'city':city,
        'state':state,
        'country':country,
        'shipping_method':shipping_method,
        'shipping_price':shipping_price,
        'sub_total':sub_total,
        'grand_total':grand_total,
    }
    var url='/checkout/cache_checkout_data/'

    $.post(url, postData).done(function(){
        stripe.confirmCardPayment(clientSecret, {
            payment_method:{
                card:card,
                billing_details:{
                    name:$.trim(form.first_name.value) + " " + $.trim(form.last_name.value),
                    email:$.trim(form.email.value),
                    phone:$.trim(form.phone.value),
                    address:{
                        line1:$.trim(form.street_address.value),
                        city:$.trim(form.city.value),
                        state:$.trim(form.state.value),
                        country:$.trim(form.country.value),
                    }
                },
                
            }
        }).then(function(result) {
            if(result.error){
                var elem = `
                <span class="icon text-danger">
                    <i class="icon-close"></i>
                </span>
                <span class="icon text-danger">  ${result.error.message}</span>
                `
                $(errorDiv).html(elem);
    
                card.update({'disabled': false})
                $('#payment-form').fadeToggle(100);
                overlay.style.display = 'none'
                $('#submit-button').attr('disabled', false)
            }else{
                if(result.paymentIntent.status === 'succeeded'){
                    overlay.style.display = 'none'
                    form.submit()
                    card.update({'disabled': false})
                    $('#submit-button').attr('disabled', false)
                }
            }
        })

    }).fail(function(e){
        console.log(e)
        location.reload()
    })

    })
