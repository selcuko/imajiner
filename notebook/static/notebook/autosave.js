


const intervalMs = 3000;
const $form  = document.getElementById('form');
let $textarea = document.getElementById('id_body');
const $status = document.getElementById('status');


let last = {
    value: $textarea.value,
    fetch: null,
};

let intervalId = setInterval(f, intervalMs);

$form.onsubmit = function (e){
    e.preventDefault();
    post(action='SUBMIT');
    $status.innerText = "Bildirge yayınlandı"
    clearInterval(intervalId);
}

$status.innerText = "Değişiklikler kaydedildi"
function f(){
    $textarea = document.getElementById('id_body');
    if ($textarea.value !== last.value){
        $status.innerText = "Eşleniyor"
        post(action='AUTOSAVE')
        .then(response => {
            $status.innerText = response.ok ? "Değişiklikler kaydedildi" : "Çok pis işler dönüyo"; 
        })
        .catch(error => {
            $status.innerText = "Çok pis işler dönüyo\n"+error;
        });
        last.value = $textarea.value;
    }
}

let c = 0;
const uuid = Date.now() + Math.random();

async function post(action='SUBMIT'){
    const fd = new FormData($form);
    fd.append('action', action);
    fd.append('count', c++);
    fd.append('uuid', uuid)
    console.log(fd.get('csrfmiddlewaretoken'));
    return await fetch('', {
        method: 'POST',
        body: fd,
        credentials: 'same-origin',
    })
}
//post('AUTOSAVE')
//c--;