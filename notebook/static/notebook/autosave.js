const $form  = document.getElementById('form');
const $textarea = document.getElementById('id_body');
const $status = document.getElementById('status');
const $title = document.getElementById('id_title');

const intervalMs = 3000;
const intervalId = setInterval(f, intervalMs);

let last = {
    value: $textarea.value,
    fetch: null,
};

$form.onsubmit = function (e){
    e.preventDefault();
    post('SUBMIT');
}

$status.innerText = "Seni bekliyorum."
function f(){
    if ($textarea.value !== last.value){
        post('AUTOSAVE');
    }
}

let c = 0;
const uuid = Date.now() + Math.random();

async function post(action='SUBMIT'){
    if (action === 'SUBMIT' && last.fetch === null){
        await post('AUTOSAVE');
    }
    $status.innerText = 'Eşleniyor.'

    const fd = new FormData($form);
    fd.append('action', action);
    fd.append('count', c++);
    fd.append('uuid', uuid);

    return await fetch('', {
        method: 'POST',
        body: fd,
        //redirect: 'manual',
        credentials: 'same-origin',
    })
    .then(response => {
        console.log(response.url);
        if (!(response.status === 200 || response.status === 302)) $status.innerText = 'Hata verdim. Sorun bende ve yazdıkların muhtemelen yedeklenemedi.';
        else {
            last.value = $textarea.value;
            last.fetch = c;
            if (action === 'SUBMIT') {
                clearInterval(intervalId);
                $status.innerText = 'Bildirge yayınlandı. Birazdan yönlendirileceksiniz.'
                setTimeout(()=>{window.location.replace(response.url);}, 500);
            } else {
                $status.innerText = 'Değişiklikler kaydedildi.'
            }
        }
    })
    .catch(error => {
        console.log(error);
        $status.innerText = 'Hata verdim. Muhtemelen internet bağlantınla ilgili ve yazdıkların kaydedilmedi.';
    })
}