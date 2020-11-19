const $feedbackForm = document.getElementById('mc-form');

$feedbackForm.onsubmit = (e) => {
    e.preventDefault();
    const fd = new FormData($feedbackForm);
    fd.append('location', document.location.href);
    fd.append('referer', document.referrer);
    fd.append('ua', navigator.userAgent);

    fetch($feedbackForm.action, {
        method: 'POST',
        body: fd,
    })
}