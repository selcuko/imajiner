const taglib = {};

const section = document.getElementById("content");
const modal = document.getElementById("myModal");
const span = document.querySelector(".close");

modal.close = (e) => {
  modal.style.display = "none";
  section.style.filter = "none";
  section.style.overflow = "auto";
};
modal.show = (e) => {
  modal.style.display = "block";
  section.style.filter = "blur(3px)";
  section.style.overflow = "hidden";
}

span.onclick = modal.close;
window.onclick = function(event) {
  if (event.target == modal) {
    modal.close();
  }
}

const $e = {};
$e.add = document.getElementById('tag-add');
$e.display = Array.from(document.querySelectorAll('.tag-display'));
$e.vars = new FormData(document.getElementById('template-vars'));
$e.form = document.getElementById('tag-add-form');

$e.add.onclick = modal.show;

$e.display.map( (display) => {
    display.onclick = (e) => {
        e.preventDefault();
        const fd = new FormData($e.form);
        fd.set('action', 'tag-step');
        fd.set('name', e.target.id);

        const tag = e.target;
        const count = tag.children[0]
        const countInt = parseInt(count.innerText);
        count.innerText = countInt+1;

        fetch('', {
          method: 'POST',
          body: fd,
        })
    }
})

$e.form.onsubmit = (e) => {
    e.preventDefault();
    const fd = new FormData($e.form);
    fd.append('action', 'tag-create');

    fetch('', {
        method: 'POST',
        body: fd,
    })
}