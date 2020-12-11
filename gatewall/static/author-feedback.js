handle.author = {
    text: (t) => {
        $author.text.innerText = t;
    },
    icon: (i) => {
        $author.icon.classList = `fas ${i}`;
    },
    status: (s) => {
        $author.status.innerText = s;
    },
}
handle.author.checking = () => {
    $author.button.disabled = true;
    handle.author.normalize();
    handle.author.text(gettext('checking'));
    handle.author.icon('fa-spin fa-circle-notch');
    handle.author.status(gettext('checking username availability'));
}

handle.author.register = () => {
    $author.button.disabled = false;
    handle.author.normalize();
    handle.author.text(gettext('register'));
    handle.author.icon('fa-user-plus');
    handle.author.status(gettext('you can register a new author user'));
}

handle.author.waiting = () => {
    handle.author.normalize();
    handle.author.text(gettext('waiting for you'));
    handle.author.icon('fa-spin fa-circle-notch');
    handle.author.status(gettext('type username to check if it is available (min 5 chars)'));
}

handle.author.postclick = (json) => {
    if ($author.action === 'author-register' && json.authenticated) {
        handle.author.success();
        handle.author.text(gettext('registered'));
        handle.author.icon('fa-check');
        handle.author.status(gettext('now you are one of us'));
        setTimeout(()=>redirect(), 1000);
    } else if ($author.action === 'author-register' && !json.authenticated) {
        handle.author.warn();
        handle.author.text(gettext('error'));
        handle.author.icon('fa-times');
        handle.author.status(gettext('something went wrong'));
    } else if ($author.action === 'author-login' && json.authenticated) {
        handle.author.success();
        handle.author.text(gettext('authenticated'));
        handle.author.icon('fa-check');
        handle.author.status(gettext('cleared access level 5'));
        setTimeout(()=>redirect(), 1000);
    } else if ($author.action === 'author-login' && !json.authenticated) {
        handle.author.warn();
        handle.author.text(gettext('incorrect credentials'));
        handle.author.icon('fa-times');
        handle.author.status(gettext('the credentials you provided did not work'));
    }
    return json.authenticated;
}

handle.author.saving = () => {
    handle.author.text(gettext('saving'));
    handle.author.icon('fa-spin fa-circle-notch');
    handle.author.status(gettext('registering your brand new account'));
}

handle.author.error = (network) => {
    handle.author.warn();
    if (network){
        handle.author.text(gettext('network error'));
        handle.author.icon('fa-times');
        handle.author.status(gettext('network error: we cannot access our servers'));
    } else {
        handle.author.text(gettext('error'));
        handle.author.icon('fa-times');
        handle.author.status(gettext('unknown error occured'));
    }
}


handle.author.login = () => {
    handle.author.success();
    handle.author.text(gettext('logging in'));
    handle.author.icon('fa-spin fa-circle-notch');
    handle.author.status(gettext('you will be logged in in no time'));
}

handle.author.retry = () => {
    handle.author.normalize();
    handle.author.text(gettext('okay now retry'));
    handle.author.icon('fa-check');
    handle.author.status(gettext('password is longer than 6 chars'));
}


handle.author.warn = () => {
    $author.button.style.color = "white";
    $author.button.style.backgroundColor = "red";
}

handle.author.success = () => {
    $author.button.style.color = "white";
    $author.button.style.backgroungColor = "green";
}

handle.author.normalize = () => {
    $author.button.style.color = "white";
    $author.button.style.backgroundColor = "black";
}

handle.author.onclick = () => {
    if ($author.action === 'author-register') handle.author.saving();
    else if ($author.action === 'author-login') handle.author.login();
    else handle.author.waiting();
}

handle.author.action = (json) => {
    $author.button.disabled = false;
    if (!json.available) {
        handle.author.text(gettext('log in'));
        handle.author.icon('fa-user-circle');
        handle.author.status(gettext('there is a user registered with that name'));
        handle.author.normalize();
    } else {
        handle.author.text(gettext('register'));
        handle.author.icon('fa-user-plus');
        handle.author.status(gettext('this username is available for newcomers'));
        handle.author.normalize();
    }
}