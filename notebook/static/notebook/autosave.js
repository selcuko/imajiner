

let last = {
    value: '',
    fetch: null,
};

const intervalMs = 3000;
const $form  = document.getElementById('form');
const $textarea  = document.getElementById('body');
const $status = document.getElementById('status');

let intervalId = setInterval(f, intervalMs);

$form.onsubmit = function (e){
    e.preventDefault();
    post(action='SUBMIT');
    $status.innerText = "Bildirge yayınlandı"
    clearInterval(intervalId);
}

$status.innerText = "Değişiklikler kaydedildi"
function f(){
    if ($textarea.value !== last.value){
        $status.innerText = "Eşleniyor"
        post(action='AUTOSAVE');
        last.value = $textarea.value;
    }
    $status.innerText = "Değişiklikler kaydedildi"
}

let c = 0;
const uuid = Date.now() + Math.random();

function post(action='SUBMIT'){
    const fd = new FormData($form);
    fd.append('action', action);
    fd.append('count', c++);
    fd.append('uuid', uuid)
    console.log(fd.get('csrfmiddlewaretoken'));
    fetch('', {
        method: 'POST',
        body: fd,
        credentials: 'same-origin',
    })
}
//post('AUTOSAVE')
//c--;