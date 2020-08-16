const $shadowButton = document.getElementById('shadow-button');
const $shadowForm = document.getElementById('shadow-register');
let clientFingerprint = null;
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
            if (found) handleShadowButton(found, username=json.username);
            else handleShadowButton(found);
        });
    });
}

function handleShadowButton(found, username=null){
    $shadowButton.disabled = false;
    if (found) {
        $shadowForm.querySelector('.username').value = username;
        $shadowButton.innerText = `${username} olarak devam et`;
    } else {
        
    }
}

$shadowButton.onclick = (e) => {
    e.preventDefault();
    const fd = new FormData($shadowForm);
    fd.append('action', 'shadow-register');
    fd.append('fingerprint', clientFingerprint);
    fetch('', {
        method: 'POST',
        body: fd,
    })
}


if (window.requestIdleCallback){
    requestIdleCallback(() => {
        checkShadowRecords();
    })
} else {
    setTimeout(checkShadowRecords, 500);
}