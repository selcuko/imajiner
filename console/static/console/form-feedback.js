function buttonHandle(btn, success=true){
    if (success) buttonSuccess(btn);
    else buttonError(btn);
}
function buttonSuccess(btn){
    languagesButton.innerHTML = '<i class="fa fa-check"></i>';
    languagesButton.style.backgroundColor = 'green';
    languagesButton.style.borderColor = 'white';
}
function buttonError(btn){
    languagesButton.innerHTML = '<i class="fa fa-times"></i>';
    languagesButton.style.backgroundColor = 'red';
    languagesButton.style.borderColor = 'black';
}
function buttonLoading(btn){
    languagesButton.innerHTML = '<i class="fas fa-circle-notch fa-spin"></i>';
    languagesButton.style.backgroundColor = 'darkblue';
    languagesButton.style.borderColor = 'white';
}