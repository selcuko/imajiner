$author.input.onkeyup = (e) => {
    if ($author.input.length < 5) {
        handle.author.waiting();
        $author.button.disabled = true;
        return;
    }
    handle.author.checking();
    const fd = new FormData($author.form);
    fd.append('action', 'username-availability');

    fetch('', {
            method: 'POST',
            body: fd,
        })
        .then(response => response.json())
        .then(json => {
            $author.action = json.available ? 'author-register' : 'author-login';
            $author.button.disabled = false;
            handle.author.action(json);
        });
}

$author.password.onkeyup = (e) => {
    if ($author.password.value.length < 6) {
        $author.button.disabled = true;
        return;
    } else if ($author.tooshort){
        $author.button.disabled = false;
        handle.author.retry();
        $author.tooshort = false;
    }
    
}

$author.button.onclick = (e) => {
    e.preventDefault();

    if ($author.password.value.length < 6) {
        $author.tooshort = true;
        handle.author.warn();
        handle.author.text(gettext('fill out password'));
        handle.author.icon('fa-info-circle');
        handle.author.status(gettext('password is too short, I want at least 6 chars'));
        return;
    }

    handle.author.onclick();

    const fd = new FormData($author.form);
    fd.append('action', $author.action);

    fetch('', {
            method: 'POST',
            body: fd,
        })
        .then(response => {
            return response.json();
        })
        .then(json => {
            handle.author.postclick(json);
        })
        .catch(error => {
            handle.author.error(network = true);
        })
}