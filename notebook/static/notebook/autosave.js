const $form = document.getElementById('form');
const $textarea = document.getElementById('id_body');
const $status = document.getElementById('status');
const $sketchesUrl = document.getElementById('sketches-url');
const $title = document.getElementById('id_title');
const $leftSketch = document.getElementById('sketch-button');
const $submit = document.getElementById('submit-button');
const intervalMs = 5000;
const intervalId = setInterval(autosave, intervalMs);

const actionCodes = {
    SUBMIT: 'SUBMIT',
    AUTOSAVE: 'AUTOSAVE',
    REVERT: 'REVERT',
    PROCEED: 'PROCEED',
}

const last = {
    value: $textarea.value,
    title: $title.value,
    fetch: null,
};

let currentTitle = last.title;
let countFetched = 0;
let publicUrl = null;
let fetchOnProgress = false;
let toBeSubmitted = false;
let submitSucceed = false;
let stopFetch = false;


$leftSketch.onclick = (e) => {
    e.preventDefault();
    post('AUTOSAVE');
    location.href = $sketchesUrl.value;
}

$form.onsubmit = function (e) {
    e.preventDefault();
    $title.readonly = true;
    $textarea.readonly = true;
    clearInterval(intervalId);
    if (submitSucceed) {
        location.href = publicUrl;
        return;
    }
    if (fetchOnProgress) toBeSubmitted = true;
    else post('SUBMIT');
}

$status.innerText = statusMessage.waiting();


const req = {
    began: () => {
        fetchOnProgress = true;
        $submit.disabled = true;
    },
    ended: () => {
        fetchOnProgress = false;
        $submit.disabled = false;
        
    }
}

function autosave() {
    titleChanged = $title.value !== last.title;
    valueChanged = $textarea.value !== last.value;
    console.log(titleChanged, valueChanged);
    if (valueChanged || titleChanged) {
        if (titleChanged) document.title = $title.value + titleSuffix;
        post('AUTOSAVE');
    }
    last.value = $textarea.value;
    last.title = $title.value;
}



async function post(action = 'SUBMIT') {
    if (fetchOnProgress) return;
    req.began();
    $status.innerText = statusMessage.syncing();

    if (action === 'SUBMIT' && last.fetch === null) {
        await post('AUTOSAVE');
    }

    // generate request body
    const fd = new FormData($form);
    fd.append('action', action);
    fd.append('count', countFetched++);
    //fd.set('title', currentTitle);
    console.log('Fetching', fd);
    await fetch('', {
        method: 'POST',
        body: fd,
        credentials: 'same-origin',
    })
        .then(response => {
            if (!response.ok) $status.innerText = statusMessage.responseNotOk();
            if (action == actionCodes.SUBMIT) {
                $status.innerText = statusMessage.processing();
                if (response.ok) submitSucceed = true;
                return response.json();
            }
            return 0;
        })
        .then(json => {
            console.log(json)
            if (action == actionCodes.SUBMIT) {
                // user submitted the narrative and server processed it. here are the results.
                language = json.language;
                if (!language) {
                    publicUrl = json.publicUrl;
                    $status.innerText = statusMessage.languageNotOk();
                    $submit.value = statusMessage.proceedAnyway();
                }
                else {
                    $status.innerText = interpolate(gettext('Declared. You will be redirected soon.'), true);
                    setTimeout(() => { location.href = json.publicUrl }, 1000);
                }
            }
            else if (action == actionCodes.AUTOSAVE) {
                // autosaved
                $status.innerText = statusMessage.autosaveOk();
            }
        })
    req.ended();
    if (toBeSubmitted) post('SUBMIT');
}

