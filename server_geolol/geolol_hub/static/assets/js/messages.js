toastr.options = {
    "closeButton": true,
    "debug": false,
    "newestOnTop": false,
    "progressBar": false,
    "positionClass": "toast-top-right",
    "preventDuplicates": false,
    "onclick": null,
    "showDuration": "300",
    "hideDuration": "1000",
    "timeOut": "5000",
    "extendedTimeOut": "1000",
    "showEasing": "swing",
    "hideEasing": "linear",
    "showMethod": "fadeIn",
    "hideMethod": "fadeOut"
}

function noficationMessage(level, message) {
    const toastrTypes = {
        25: toastr.success,
        30: toastr.warning,
        40: toastr.error,
        20: toastr.info
    };

    const toastrFunction = toastrTypes[level] || toastr.info;

    const displayMessage = message || "Mensagem não fornecida.";

    toastrFunction(displayMessage);
}
