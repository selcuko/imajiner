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
function handleForm(form, btn, action=null){
    if (typeof form === 'string') form = document.getElementById(form);
    if (typeof btn === 'string') btn = document.getElementById(btn);

    form.onsubmit = (e) => {
        buttonLoading(btn);
        e.preventDefault();
        
        const fd = new FormData(form);
        if (action) fd.set('action', action);

        fetch('', {
            method: 'POST',
            body: fd
        })
        .then(response => buttonHandle(btn, success=response.ok))
        .catch(error => buttonError(btn))
    }
}