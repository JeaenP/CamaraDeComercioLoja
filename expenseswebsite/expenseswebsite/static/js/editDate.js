
$(document).ready(function() {
    $(".datepicker").datepicker({
        dateFormat: 'dd-mm-yy',
        showOtherMonths: true,
        selectOtherMonths: true,
        changeMonth: true,
        changeYear: true,
        yearRange: "1900:+nn",
        monthNames: ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"],
        monthNamesShort: ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"],
        dayNames: ["Domingo", "Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado"],
        dayNamesShort: ["Dom", "Lun", "Mar", "Mié", "Jue", "Vie", "Sáb"],
        dayNamesMin: ["Do", "Lu", "Ma", "Mi", "Ju", "Vi", "Sá"],
    });

    
    $(".datepicker").each(function() {
            var fechaGuardada = $(this).val();
    
            if (fechaGuardada) {
                $(this).datepicker("setDate", new Date(fechaGuardada));
            }
        });
    $("form").submit(function(event) {
        $(".datepicker").each(function() {
            var fechaGuardada = $(this).datepicker("getDate");
            if (fechaGuardada) {
                var fechaFormateada = $.datepicker.formatDate('yy-mm-dd', fechaGuardada);
                $(this).val(fechaFormateada);
            }
        });
    });

});
