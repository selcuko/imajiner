handle.shadow = {
    text: (t) => {
        $shadow.text.innerText = t;
    },
    icon: (i) => {
        $shadow.icon.classList = `fas ${i}`;
    },
    status: (s) => {
        $shadow.status.innerText = s;
    },
}
handle.shadow.checking = () => {
    $shadow.button.disabled = true;
    handle.shadow.normalize();
    handle.shadow.text(gettext('checking'));
    handle.shadow.icon('fa-spin fa-circle-notch');
    handle.shadow.status(gettext('checking username availability'));
}

handle.shadow.identifying = () => {
    handle.shadow.normalize();
    handle.shadow.text(gettext('identifying'));
    handle.shadow.icon('fa-spin fa-circle-notch');
    handle.shadow.status(gettext('seeing whether we recognize you'));
}

handle.shadow.register = () => {
    $shadow.button.disabled = false;
    handle.shadow.normalize();
    handle.shadow.text(gettext('register'));
    handle.shadow.icon('fa-user-plus');
    handle.shadow.status(gettext('you can register a new shadow user'));
}

handle.shadow.found = (json) => {
    $shadow.input.value = json.username;
    $shadow.input.disabled = true;
    $shadow.button.disabled = false;
    handle.shadow.success();
    handle.shadow.text(gettext('proceed'));
    handle.shadow.icon('fa-user-circle');
    handle.shadow.status(`you are recognized as ${json.username}.`);
}

handle.shadow.waiting = () => {
    handle.shadow.normalize();
    handle.shadow.text(gettext('waiting for you'));
    handle.shadow.icon('fa-spin fa-circle-notch');
    handle.shadow.status(gettext('type username to check if it is available (min 5 chars)'));
}

handle.shadow.postclick = (json) => {
    handle.shadow.success();
    $shadow.input.value = json.username;
    if ($shadow.action === 'shadow-register') {
        handle.shadow.text(gettext('registered'));
        handle.shadow.icon('fa-check');
        handle.shadow.status(gettext('now you are one of us'));
        setTimeout(()=>redirect(), 1000);
    } else if ($shadow.action === 'shadow-login') {
        handle.shadow.text(gettext('authenticated'));
        handle.shadow.icon('fa-check');
        handle.shadow.status(gettext('cleared access level 5'));
        setTimeout(()=>redirect(), 1000);
    }
}

handle.shadow.saving = () => {
    handle.shadow.text(gettext('saving'));
    handle.shadow.icon('fa-spin fa-circle-notch');
    handle.shadow.status(gettext('registering your brand new account'));
}

handle.shadow.error = (network) => {
    handle.shadow.warn();
    if (network){
        handle.shadow.text(gettext('network error'));
        handle.shadow.icon('fa-times');
        handle.shadow.status(gettext('network error: we cannot access our servers'));
    } else {
        handle.shadow.text(gettext('error'));
        handle.shadow.icon('fa-times');
        handle.shadow.status(gettext('unknown error occured'));
    }
}

handle.shadow.login = () => {
    handle.shadow.success();
    handle.shadow.text(gettext('logging in'));
    handle.shadow.icon('fa-spin fa-circle-notch');
    handle.shadow.status(gettext('you will be logged in in no time'));
}


handle.shadow.warn = () => {
    $shadow.button.style.color = "red";
    $shadow.button.style.borderColor = "red";
}

handle.shadow.success = () => {
    $shadow.button.style.color = "green";
    $shadow.button.style.borderColor = "green";
}

handle.shadow.normalize = () => {
    $shadow.button.style.color = "black";
    $shadow.button.style.borderColor = "black";
}

handle.shadow.onclick = () => {
    if ($shadow.action === 'shadow-register') handle.shadow.saving();
    else if ($shadow.action === 'shadow-login') handle.shadow.login();
    else handle.shadow.waiting();
}

handle.shadow.availability = (available) => {
    $shadow.button.disabled = !available;
    if (available) {
        handle.shadow.text(gettext('register'));
        handle.shadow.icon('fa-user-plus');
        handle.shadow.status(gettext('this username is available'));
        handle.shadow.success();
    } else {
        handle.shadow.text(gettext('unavailable'));
        handle.shadow.icon('fa-ban');
        handle.shadow.status(gettext('username is not available'));
        handle.shadow.warn();
    }
}