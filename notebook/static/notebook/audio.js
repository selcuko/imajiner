const audioPrimary = document.getElementById('audio-primary');
const audioSecondary = document.getElementById('audio-secondary');
const audioInput = document.getElementById('audio-input');

const audioPrimaryIcon = audioPrimary.children[0];
const audioPrimaryText = audioPrimary.children[1];
const audioSecondaryIcon = audioSecondary.children[0];

let selected = false;


audioInput.onchange = (e) => {
    selected = true;
    const file = e.target.files[0];
    if (!file) return;
    audioPrimaryText.innerText = truncate(file.name);

    changeIcon(audioPrimaryIcon, 'alternate sync');
    changeIcon(audioSecondaryIcon, 'delete');
}

audioSecondary.onclick = (e) => {
    if (selected) { 
        selected = false;
        audioPrimaryText.innerText = 'Ses ekle...yeniden';
        changeIcon(audioPrimaryIcon, 'paperclip');
        changeIcon(audioSecondaryIcon, 'microphone');
        return;
    } else {
        /* voice record */
    }
}


const changeIcon = (i, name) => i.classList.value = `${name} icon`;

const truncate = (text, length=16) => text.length <= length ? text : `${text.slice(0, 9)}...${text.slice(-9)}`;