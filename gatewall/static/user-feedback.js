const message = {
    success: ''
}

const getIcon = (i, spin=false) => `<i class="fas fa-2x${spin ? " fa-spin " : " "}${i}"></i>`;
const getText = (t, m=true) => `<p style="margin:0; margin-left:${m?'.5em':'0'};">${t}</p>`;

const handleButtonShadowFound = (btn, username=null) => {
    if (typeof btn === 'string') btn = document.getElementsById(btn);
    btn.innerHTML = getIcon('fa-check');
    if (typeof username === 'string') btn.innerHTML += getText('recognized, proceed');
    btn.style.color = 'darkblue';
    btn.style.borderColor = 'darkblue';
}

const handleButtonShadowRegister = (btn) => {
    if (typeof btn === 'string') btn = document.getElementsById(btn);
    btn.innerHTML = getIcon('fa-user-circle');
    btn.innerHTML += getText('register');
}

const handleButtonLoading = (btn, message=null) => {
    if (typeof btn === 'string') btn = document.getElementsById(btn);
    btn.innerHTML = '<i class="fas fa-2x fa-spin fa-circle-notch"></i>';
    if (typeof message === 'string') btn.innerHTML += ('<p style="margin:0; margin-left:.5em;">' + message +' </p>');
}