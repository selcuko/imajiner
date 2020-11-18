$status = document.getElementById('sessions-status');
$csrf = document.getElementById('csrf');

const setStatus = (text) => $status.childNodes[0].data = text

const terminateSession = (key) => {
    const fd = new FormData($csrf);
    fd.append('session_key', key);
    fetch('', {
        method: 'POST',
        body: fd,
    })
    .then(response => {
        if (response.ok) {
            $status.innerText = gettext('Session terminated successfully.');
            $terminated = document.getElementById(key);
            $terminated.remove()
        } else {
            $status.innerText = gettext('Some error occured and session did not terminated.')
        }
        $status.classList.add('show');
    })
}