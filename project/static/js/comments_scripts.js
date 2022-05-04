document.addEventListener("DOMContentLoaded", function(event) {
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    document.getElementsByClassName('add-comment-form')[0].onsubmit = async (event) => {
        event.preventDefault();

        form = event.target
        product_id = window.location.href.split('-').slice(-1)[0]
        const csrftoken = getCookie('csrftoken');
        url = form.action;

        let response = await fetch(url, {
            method: "POST",
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({
                'product_id': product_id,
                'content': form.content.value,
            })
        })
        .then(response => response.json())
        .then(data => addCommentRender(data));
    }
    async function replyFormEventHandler(event){
        event.preventDefault();

        form = event.target
        parent_id = event.target.id.split('__')[1]
        product_id = window.location.href.split('?')[0].split('-').slice(-1)[0]

        const csrftoken = getCookie('csrftoken');
        url = form.action;

        const response = await fetch(url, {
            method: "POST",
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({
                'product_id': product_id,
                'parent_id': parent_id,
                'content': form.content.value,
            })
        })
        data = await response.json()

        addCommentRender(data)
    }
    function addCommentRender(data){
        toastr.success(data['message']);

        comment = document.createElement('div')
        comment.id = `comment-${data['id']}`
        comment.classList.add('comment')

        comment.innerHTML =
        `<div class="comment__body">
            <div class="comment__head">
                <div class="comment__user">${data['username']}</div>
                <div class="comment__date">${data['calculated_date']}</div>
            </div>
            <div class="comment__content">${data['content']}</div>
            <div class="comment__controls">
                <div class="comment__reply">ответить</div>
                    <div class="comment__rating__wrap">
                    <div class="comment__like"></div>
                    <div class="comment__rating">${data['rating']}</div>
                <div class="comment__dislike"></div>
            </div>
        </div>`

        if (data['comment_is_root_node']){
            comments = document.getElementsByClassName('comments')[0]
            comments.prepend(comment)
            textarea = comments.parentElement.querySelector('.add__comment__form__wrap textarea')
            textarea.value = ''
        }
        else{
            parent = document.getElementById(`comment-${data['parent_id']}`)
            if(data['parent_was_leaf_node']){
                children = document.createElement('div')
                children.classList.add('comment__children')
                parent.appendChild(children)
            }
            else{
                children = parent.querySelector('div.comment__children')
            }
            children.prepend(comment)
        }

        comment.querySelector('div.comment__reply').addEventListener('click', replyButtonOpenEventHandler);
        comment.querySelector('div.comment__like').addEventListener('click', likeButtonEventHandler);
        comment.querySelector('div.comment__dislike').addEventListener('click', dislikeButtonEventHandler);
        checkEdited()
    }

    var reply_buttons = document.getElementsByClassName('comment__reply');
    function replyButtonOpenEventHandler(event){
        event.target.innerText = 'отмена'
        event.target.removeEventListener('click', replyButtonOpenEventHandler)
        event.target.addEventListener('click', replyButtonCloseEventHandler)

        checkEdited()

        comment = event.target.parentElement.parentElement.parentElement
        comment.classList.add('is-edited')
        let parent_id = comment.id.split('-')[1]
        url_add_form = `${document.location.protocol}//${document.location.host}/comments/add_comment`

        comment__reply = document.createElement('div')
        comment__reply.classList.add('reply__comment__form__wrap')

        comment__reply.innerHTML =
        `<form action="${url_add_form}" method="post" class="add-comment-form" id="comment__${parent_id}__reply">
            <textarea name="content" class="content-control" id="id_reply_${parent_id}"
                placeholder="Введите комментарий:" required></textarea>
            <input type="submit" value="Отправить">
         </form>`

        comment__body = event.target.parentElement.parentElement
        comment__body.appendChild(comment__reply)

        comment__reply.querySelector('textarea').focus()

        comment__reply.children[0].addEventListener('submit', replyFormEventHandler)
    }
    function replyButtonCloseEventHandler(event){
        comment = event.target.parentElement.parentElement.parentElement
        comment.classList.remove('is-edited')
        comment__reply = event.target
        comment__reply.innerText = 'ответить'
        comment__reply.removeEventListener('click', replyButtonCloseEventHandler)
        comment__reply.addEventListener('click', replyButtonOpenEventHandler)
        reply__wrap = comment__reply.parentElement.nextElementSibling
        reply__wrap.remove()
    }
    function checkEdited(){
        comments = document.getElementsByClassName('comment')
        is_edited = false
        index = 0
        for (var i = 0; i < reply_buttons.length; i++) {
            if(comments[i].classList.contains('is-edited')){
                is_edited = true
                index = i
                break
            }
        }
        if(is_edited){
            comment = comments[index]
            comment.classList.remove('is-edited')
            comment__reply = comment.querySelector('div.comment__reply')
            comment__reply.innerText = 'ответить'
            comment__reply.removeEventListener('click', replyButtonCloseEventHandler)
            comment__reply.addEventListener('click', replyButtonOpenEventHandler)
            reply__wrap = comment__reply.parentElement.nextElementSibling
            reply__wrap.remove()
        }
    }
    for (var i = 0; i < reply_buttons.length; i++) {
        reply_buttons[i].addEventListener('click', replyButtonOpenEventHandler);
    }

    var like_buttons = document.getElementsByClassName('comment__like');
    var dislike_buttons = document.getElementsByClassName('comment__dislike');

    async function likeButtonEventHandler(event){
        comment = event.target.parentElement.parentElement.parentElement.parentElement
        comment_id = comment.id.split('-')[1]

        const csrftoken = getCookie('csrftoken');
        url = `${document.location.protocol}//${document.location.host}/comments/toggle_comment_vote`

        const response = await fetch(url, {
            method: "POST",
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({
                'comment_id': comment_id,
                'opinion': 'like',
            })
        })
        data = await response.json()

        event.target.classList.toggle('voted')
        event.target.parentElement.querySelector('.comment__dislike').classList.remove('voted')
        event.target.parentElement.querySelector('.comment__rating').innerText = data['rating']
    }
    async function dislikeButtonEventHandler(event){
        comment = event.target.parentElement.parentElement.parentElement.parentElement
        comment_id = comment.id.split('-')[1]

        const csrftoken = getCookie('csrftoken');
        url = `${document.location.protocol}//${document.location.host}/comments/toggle_comment_vote`

        const response = await fetch(url, {
            method: "POST",
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({
                'comment_id': comment_id,
                'opinion': 'dislike',
            })
        })
        data = await response.json()

        event.target.classList.toggle('voted')
        event.target.parentElement.querySelector('.comment__like').classList.remove('voted')
        event.target.parentElement.querySelector('.comment__rating').innerText = data['rating']
    }

    for (var i = 0; i < like_buttons.length; i++) {
        like_buttons[i].addEventListener('click', likeButtonEventHandler);
    }
    for (var i = 0; i < dislike_buttons.length; i++) {
        dislike_buttons[i].addEventListener('click', dislikeButtonEventHandler);
    }
})