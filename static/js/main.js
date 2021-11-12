$('#sig-info').on('click', function(){
    event.preventDefault()
    $(this).fadeOut().addClass("d-none");
    $('#modal-button').addClass("d-none");
    $('#type_load').animate({
        height: 'toggle'
    });
    $('#exampleModal').modal('hide');
    $('#info-load').removeClass('d-none').fadeTo("slow")
    $('#leyend-info-load').removeClass('d-none').fadeTo("slow")
    $('#save-info').removeClass('d-none').fadeTo("slow")
})

$('input[name=order_type]').on('change', function(){
    $('#modal-body').text('Usted registrará una nueva orden de ' + $(this).val())
    $("#modal-button").prop('disabled', false);
})
