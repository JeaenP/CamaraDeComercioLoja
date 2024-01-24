document.addEventListener('DOMContentLoaded', function() {
    var elements = document.querySelectorAll('.form-select, .form-control');
    
    elements.forEach(function(element) {
        validateInput(element);
    });
}); 
function validateNumberInput(input) {
    input.value = input.value.replace(/[^0-9]/g, '');

    var formGroupLabel = input.parentElement;

    if (input.value.trim() === '') {
        formGroupLabel.querySelector('.validation-asterisk').style.display = 'inline';
    } else {
        formGroupLabel.querySelector('.validation-asterisk').style.display = 'none';
    }
}
function validateInput(input) {
    var formGroupLabel = input.parentElement;
    
    // Check if formGroupLabel and .validation-asterisk exist before using querySelector
    if (formGroupLabel && formGroupLabel.querySelector && formGroupLabel.querySelector('.validation-asterisk')) {
        if ((input.tagName === 'SELECT' || input.tagName === 'INPUT') && input.value.trim() === '') {
            formGroupLabel.querySelector('.validation-asterisk').style.display = 'inline';
        } else {
            formGroupLabel.querySelector('.validation-asterisk').style.display = 'none';
        }
    }
}