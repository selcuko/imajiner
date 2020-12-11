async function fingerprintDevice() {
    return await Fingerprint2.getPromise()
        .then(components => {
            var values = components.map(function (component) {
                return component.value
            })
            return Fingerprint2.x64hash128(values.join(''), 31);
        })
}


$shadow.input.onkeyup = (e) => {
    if ($shadow.input.value.length < 5) {
        handle.shadow.waiting();
        return;
    }
    handle.shadow.checking();

    const fd = new FormData($shadow.form);
    fd.set('action', 'username-availability')

    fetch('', {
            method: 'POST',
            body: fd,
        })
        .then(response => response.json())
        .then(json => {
            handle.shadow.availability(json.available);
        })
        .catch(error => handle.shadow.error());
}


function checkShadowRecords() {
    handle.shadow.identifying();

    fingerprintDevice()
        .then(fingerprint => {
            $shadow.fingerprint = fingerprint;

            const fd = new FormData($shadow.form);
            fd.append('fingerprint', fingerprint);
            fd.append('action', 'shadow-check');

            fetch('', {
                    method: 'POST',
                    body: fd,
                })
                .then(response => {
                    return response.json();
                })
                .then(json => {
                    const found = json.found;
                    if (auto && found) $shadow.button.click();
                    $shadow.action = found ? 'shadow-login' : 'shadow-register';
                    if (found) handle.shadow.found(json);
                    else handle.shadow.waiting();
                })
                .catch(error => handle.shadow.error());
        });
}

$shadow.button.onclick = (e) => {
    e.preventDefault();

    if ($shadow.action === null) {
        $shadow.button.disabled = true;
        handle.shadow.warn();
        return;
    } else {
        $shadow.button.disabled = false;
    }

    handle.shadow.onclick();

    const fd = new FormData($shadow.form);
    fd.append('action', $shadow.action);
    fd.append('fingerprint', $shadow.fingerprint);

    fetch('', {
            method: 'POST',
            body: fd,
        })
        .then(response => {
            return response.json();
        })
        .then(json => {
            handle.shadow.postclick(json);
        })

    if ($shadow.button.disabled) handle.shadow.warn();

}


if (window.requestIdleCallback) {
    requestIdleCallback(() => {
        checkShadowRecords();
    })
} else {
    setTimeout(checkShadowRecords, 500);
}