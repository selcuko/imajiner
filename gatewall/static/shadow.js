const $shadowButton = document.getElementById('shadow-button');
const $shadowForm = document.getElementById('shadow-register');
const $shadowUser = $shadowForm.querySelector('.username');
let clientFingerprint = null;
let shadowAction = null;
$shadowButton.disabled = true;


async function fingerprintDevice() {
    return await Fingerprint2.getPromise()
        .then(components => {
            var values = components.map(function (component) { return component.value })
            return Fingerprint2.x64hash128(values.join(''), 31);
        })
}


function checkShadowRecords() {

    fingerprintDevice()
    .then(fingerprint => {
        clientFingerprint = fingerprint;
        const fd = new FormData($shadowForm);
        fd.append('fingerprint', fingerprint);
        fd.append('action', 'shadow-check');
        fetch('', {
            method: 'POST',
            body: fd,
        })
        .then(response => response.json())
        .then(json => {
            const found = json.found;
            action = found ? 'login' : 'register';
            if (auto&&found) $shadowButton.click();
            if (found) handleShadowButton(found, username=json.username);
            else handleShadowButton(found);
        });
    });
}

function handleShadowButton(found, username=null){
    $shadowButton.disabled = false;
    if (found) {
        $shadowUser.disabled = true;
        $shadowUser.value = username;
        $shadowButton.innerText = interpolate(gettext('proceed as %(username)s'), {username: username}, true).toUpperCase();
    } else {
        
    }
}

$shadowButton.onclick = (e) => {
    e.preventDefault();
    if (!action) return;
    const fd = new FormData($shadowForm);
    fd.append('action', `shadow-${action}`);
    fd.append('fingerprint', clientFingerprint);
    fetch('', {
        method: 'POST',
        body: fd,
    }).then(response => {
        if (response.ok) redirect();
        else {
            // bir şeyler ters gitti
        };
    })
}


if (window.requestIdleCallback){
    requestIdleCallback(() => {
        checkShadowRecords();
    })
} else {
    setTimeout(checkShadowRecords, 500);
}