function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


function tagPost(slug){
    slug =slug;
    let data = new FormData();
    let payload = {};
    payload[slug] = 1;
    data.append('payload', JSON.stringify(payload));
    data.append('action', 'TAGDELTA')
    data.append('csrfmiddlewaretoken', getCookie('csrftoken'));

    fetch('', {
        credentials: 'same-origin', 
        method:"POST", 
        body: data,
    })
}