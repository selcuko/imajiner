const $feedbackForm = document.getElementById('mc-form');
const $feedbackStatus = document.getElementById('fb-status');

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
    .then(response => {
        $feedbackStatus.innerText = response.ok 
        ? gettext('Feedback sent successfully.')
        : gettext('Oh no! I encountered an error whilst sending your report.')
        $feedbackStatus.parentNode.style.display = '';
    })
}