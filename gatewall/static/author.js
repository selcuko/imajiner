const $authorForm = document.getElementById('author-register');
const $authorButton = $authorForm.querySelector('.btn');
const $username = $authorForm.querySelector('.username');

let lastUsername = null;
let buttonAction = null;

function usernameTypeCallback(){
    if ($username.value.length < 6){
        lastUsername = $username.value;
        $authorButton.innerText = 'Bekliyor';
    } else if ($username.value !== lastUsername){
        lastUsername = $username.value;
        checkUsernameAvailability($username.value)
        .then(available => {
            buttonAction = available ? 'register' : 'login';
            handleAuthorButton(available);
        })
    } else {
        //$authorButton.disabled = true;
        //$authorButton.innerText = 'Bekliyor'
    }
}


async function checkUsernameAvailability(username){
    const fd = new FormData($authorForm);
    fd.append('action', 'author-check');
    return await fetch('', {
        method: 'POST',
        body: fd,
    })
    .then(response => response.status === 200);
}

function handleAuthorButton(available){
    if (available){
        $authorButton.innerText = 'Kaydol';
    } else {
        $authorButton.innerText = 'Giriş yap';
    }
}


$authorButton.onclick = (e) => {
    e.preventDefault();
    const fd = new FormData($authorForm);
    fd.append('action', `author-${buttonAction}`);
    fetch('', {
        method: 'POST',
        body: fd,
    })
    .then(response => {
        if (response.ok) redirect();
        else $authorButton.innerText = 'Pardon kimsiniz?'
    })
}

const intervalId = setInterval(usernameTypeCallback, 1000);


