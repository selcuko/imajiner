const taglib = {};

const $e = {};
$e.add = document.getElementById('tag-add');
$e.display = new Array(document.querySelectorAll('.tag-display'));
$e.form = new FormData(document.getElementById('template-vars'));

$e.add.onclick = (e) => {
    e.preventDefault();
    console.log(`Add slug on ${$e.form.get('narrative-slug')}`);
};

$e.display.map( (display) => {
    display.onclick = (e) => {
        e.preventDefault();
        console.log(`Interact [${e.target.id}] on ${$e.form.get('narrative-slug')}`);

    }
})