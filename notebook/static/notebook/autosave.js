const $form = document.getElementById('form');
const $textarea = document.getElementById('id_body');
const $status = document.getElementById('status');
const $title = document.getElementById('id_title');
const $submit = document.getElementById('submit-button');
let currentTitle = null;

const intervalMs = 5000;
const intervalId = setInterval(autosaveSketch, intervalMs);

let last = {
    value: $textarea.value,
    title: null,
    fetch: null,
};

const capitalize = (s) => {
    if (typeof s !== 'string') return ''
    return s.charAt(0).toUpperCase() + s.slice(1)
  }

$form.onsubmit = function (e) {
    e.preventDefault();
    post('SUBMIT');
}

$status.innerText = gettext("I'm waiting for you.")
function autosaveSketch() {
    currentTitle = $title.value ? $title.value : capitalize(gettext('entitled narrative'));
    titleChanged = currentTitle !== last.title;
    if ($textarea.value !== last.value || titleChanged) {
        if (titleChanged) document.title = currentTitle + ' • Imajiner'
        post('AUTOSAVE');
    }
}

let c = 0;

async function post(action = 'SUBMIT') {
    if (action === 'SUBMIT' && last.fetch === null) {
        await post('AUTOSAVE');
    }
    $status.innerText = capitalize(gettext('syncing')) + '...';

    const fd = new FormData($form);
    fd.append('action', action);
    fd.append('count', c++);
    fd.set('title', currentTitle);

    return await fetch('', {
        method: 'POST',
        body: fd,
        credentials: 'same-origin',
    })
    .then(response => {
        if (!(response.status === 200 || response.status === 302)) {
            $status.innerText = gettext('I have encountered an error. It is my fault and anything you wrote probably did not synced nor saved.');
        } else {
            last.value = $textarea.value;
            last.fetch = c;
            if (action === 'SUBMIT') {
                clearInterval(intervalId);
                $status.innerText = gettext('Declared. You will be redirected soon.');
                setTimeout(() => { window.location.replace(response.url); }, 500);
            } else {
                $status.innerText = capitalize(gettext('changes saved.'));
            }
        }
        response.json();
    })
    .then(json => {
        console.log(json);
    })
    .catch(error => {
        console.log(error);
        $status.innerText = gettext('I have encountered an error. It is probably your internet connection and anything you wrote probably did not synced nor saved.')
    })
}