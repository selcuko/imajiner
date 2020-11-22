const $form = document.getElementById('form');
const $textarea = document.getElementById('id_body');
const $status = document.getElementById('status');
const $title = document.getElementById('id_title');
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
    title: document.title,
    fetch: null,
};

let currentTitle = last.title;
let countFetched = 0;
let publicUrl = null;
let fetchOnProgress = false;
let toBeSubmitted = false;
let submitSucceed = false;

$form.onsubmit = function (e) {
    e.preventDefault();
    if (submitSucceed) location.href = publicUrl;
    if (fetchOnProgress) toBeSubmitted = true;
    else post('SUBMIT');
}

$status.innerText = statusMessage.waiting;


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
    currentTitle = $title.value ? $title.value : titleDefault;
    titleChanged = currentTitle !== last.title;
    if ($textarea.value !== last.value || titleChanged) {
        if (titleChanged) document.title = currentTitle + titleSuffix;
        post('AUTOSAVE');
    }
    last.value = $textarea.value;
    last.title = currentTitle;
}



async function post(action = 'SUBMIT') {
    if (fetchOnProgress) return;
    req.began();
    $status.innerText = statusMessage.syncing;

    if (action === 'SUBMIT' && last.fetch === null) {
        await post('AUTOSAVE');
    }

    // generate request body
    const fd = new FormData($form);
    fd.append('action', action);
    fd.append('count', countFetched++);
    //fd.set('title', currentTitle);

    await fetch('', {
        method: 'POST',
        body: fd,
        credentials: 'same-origin',
    })
        .then(response => {
            if (!response.ok) $status.innerText = statusMessage.responseNotOk;
            if (action == actionCodes.SUBMIT) {
                $status.innerText = statusMessage.processing;
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
                    $status.innerText = statusMessage.languageNotOk;
                    $submit.value = statusMessage.proceedAnyway;
                }
                else {
                    $status.innerText = interpolate(gettext('Declared. You will be redirected soon.'), true);
                    setTimeout(() => { location.href = json.publicUrl }, 1000);
                }
            }
            else if (action == actionCodes.AUTOSAVE) {
                // autosaved
                $status.innerText = statusMessage.autosaveOk;
            }
        })
    req.ended();
    if (toBeSubmitted) post('SUBMIT');
}

