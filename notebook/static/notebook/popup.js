const tagAddForm = document.getElementById('tag-add-form');
const tagAddModal = $('.semantic.modal');
const tagAddButton = document.getElementById('tag-add-button');

tagAddButton.onclick = (e) => {
    tagAddModal.modal('show');
}