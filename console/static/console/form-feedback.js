function buttonHandle(btn, success=true){
    if (success) buttonSuccess(btn);
    else buttonError(btn);
}
function buttonSuccess(btn){
    btn.innerHTML = '<i class="fa fa-check"></i>';
    btn.style.backgroundColor = 'green';
    btn.style.borderColor = 'white';
}
function buttonError(btn){
    btn.innerHTML = '<i class="fa fa-times"></i>';
    btn.style.backgroundColor = 'red';
    btn.style.borderColor = 'black';
}
function buttonLoading(btn){
    btn.innerHTML = '<i class="fas fa-circle-notch fa-spin"></i>';
    btn.style.backgroundColor = 'darkblue';
    btn.style.borderColor = 'white';
}