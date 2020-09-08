const taglib = {};

taglib.register = (tag) => {
  tag.onclick = (e) => {
    e.preventDefault();
    const fd = new FormData($e.form);
    fd.set('action', 'tag-step');
    fd.set('name', e.target.id);

    //const tag = e.target;
    const count = tag.children[0]
    const countInt = parseInt(count.innerText);
    count.innerText = countInt + 1;

    fetch('', {
      method: 'POST',
      body: fd,
    })
  }
}

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
window.onclick = function (event) {
  if (event.target == modal) {
    modal.close();
  }
}

const $e = {};
$e.add = document.getElementById('tag-add');
$e.tags = document.getElementById('tag-list');
$e.display = Array.from(document.querySelectorAll('.tag-display'));
$e.vars = new FormData(document.getElementById('template-vars'));
$e.form = document.getElementById('tag-add-form');

$e.add.onclick = modal.show;

$e.display.map((display) => { taglib.register(display); })

$e.form.onsubmit = (e) => {
  e.preventDefault();
  const fd = new FormData($e.form);
  fd.append('action', 'tag-create');

  fetch('', {
    method: 'POST',
    body: fd,
  }).then(response => {
    const newtag = document.createElement('a');
    newtag.appendChild(document.createTextNode(fd.get('name') + ' ('));

    const cn = document.createElement('small');
    cn.appendChild(document.createTextNode('1'));
    newtag.appendChild(cn);
    newtag.appendChild(document.createTextNode(')'))
    $e.tags.insertBefore(newtag, $e.tags.children[$e.tags.children.length - 1]);
    console.log(newtag.children);
    taglib.register(newtag);
    modal.close();
  })
}