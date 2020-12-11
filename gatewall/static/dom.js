const $shadow = {
    button: document.getElementById('shadow-button'),
    icon: document.getElementById('shadow-button-icon'),
    text: document.getElementById('shadow-button-text'),
    status: document.getElementById('shadow-message'),
    form: document.getElementById('shadow-form'),
    input: document.getElementById('shadow-input'),
    action: null,
    fingerprint: null,
}

const $author = {
    button: document.getElementById('author-button'),
    icon: document.getElementById('author-button-icon'),
    text: document.getElementById('author-button-text'),
    status: document.getElementById('author-message'),
    form: document.getElementById('author-form'),
    input: document.getElementById('author-input'),
    password: document.getElementById('author-password'),
    tooshort: false,
    action: null,
}

const handle = {};
