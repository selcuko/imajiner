const $logout = document.getElementById('logout-button');
const $form = document.getElementById('form');

$logout.onclick = () => {
    const fd = new FormData($form);
    fd.append('action', 'logout');
    fetch('', {
        method: 'POST',
        body:fd,
    })
    .then(response => location.reload());
}