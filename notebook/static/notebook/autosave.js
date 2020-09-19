const $form  = document.getElementById('form');
const $textarea = document.getElementById('id_body');
const $status = document.getElementById('status');
const $title = document.getElementById('id_title');

const intervalMs = 3000;
const intervalId = setInterval(f, intervalMs);

let last = {
    value: $textarea.value,
    title: null,
    fetch: null,
};

$form.onsubmit = function (e){
    e.preventDefault();
    post('SUBMIT');
}

$textarea.disabled = new Boolean($title.value);

$status.innerText = "Seni bekliyorum."
function f(){
    titleChanged = $title.value !== last.title;
    if ($textarea.value !== last.value || titleChanged){
        if (titleChanged) {
            if ($title.value === '') $textarea.disabled = true;
            else if($textarea.disabled) $textarea.disabled = false;
            document.title = $title.value + ' | Imajiner.';
            last.title = $title.value;
        }
        post('AUTOSAVE');
    }
}

let c = 0;

async function post(action='SUBMIT'){
    if (action === 'SUBMIT' && last.fetch === null){
        await post('AUTOSAVE');
    }
    $status.innerText = 'Eşleniyor.'

    const fd = new FormData($form);
    fd.append('action', action);
    fd.append('count', c++);
    if (file) {
        console.log('appended file')
        fd.append('audio', file)
    } else console.log('no file selected')

    return await fetch('', {
        method: 'POST',
        body: fd,
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
                //setTimeout(()=>{window.location.replace(response.url);}, 500);
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