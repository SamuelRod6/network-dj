function editPost(id) {
    const post = document.getElementById(`post-${id}`);
    
    const content = post.querySelector('p[name="content"]').innerHTML;
    post.querySelector('p[name="content"]').style.display = 'none';
    
    const edit = post.querySelector('div[name="edit-window"]');
    
    const textBox = document.createElement('input');
    textBox.className = 'form-control';
    textBox.type = 'text';
    textBox.placeholder = 'Edit your post'
    textBox.value = content;
    edit.append(textBox);

    const saveButton = document.createElement('button');
    saveButton.className = 'btn btn-success';
    saveButton.innerHTML = 'Save';
    edit.append(saveButton);
    saveButton.addEventListener('click', () => {
        post.querySelector('p[name="content"]').style.display = 'block';
        edit.innerHTML = '';
        post.querySelector('p[name="content"]').innerHTML = textBox.value;   
        fetch(`/edit/${id}`, {
            method: 'POST',
            body: JSON.stringify({
                content: textBox.value
            })
        })
        .then(response => response.json())
        .then(result => {
            console.log(result);
        });
    });

    const cancelButton = document.createElement('button');
    cancelButton.className = 'btn btn-default';
    cancelButton.innerHTML = 'Cancel';
    edit.append(cancelButton);
    cancelButton.addEventListener('click', () => {
        post.querySelector('p[name="content"]').style.display = 'block';
        edit.innerHTML = '';
    });
}


function likePost(id, likes) {
    const post = document.getElementById(`post-${id}`);

    if (likes) {
        const button = post.querySelector('button[name="dislike"]')
        button.className = 'btn btn-primary btn-sm';
        button.name = 'like';
        button.innerHTML = 'Like';
        button.setAttribute('onclick', `likePost(${id}, false)`);

        const likesCounter = post.querySelector('p[name="likes"]');
        var count = likesCounter.innerHTML.replace('Likes', '').trim();
        likesCounter.innerHTML = parseInt(count)-1 + " Likes";

        fetch(`/like/${id}`, {
            method: 'POST',
            body: JSON.stringify({
                like: false
            })
        })

    }
    else {
        const button = post.querySelector('button[name="like"]')
        button.className = 'btn btn-danger btn-sm';
        button.name = 'dislike';
        button.innerHTML = 'Dislike';
        button.setAttribute('onclick', `likePost(${id}, true)`);

        const likesCounter = post.querySelector('p[name="likes"]');
        var count = likesCounter.innerHTML.replace('Likes', '').trim();
        likesCounter.innerHTML = parseInt(count)+1 + " Likes";

        fetch(`/like/${id}`, {
            method: 'POST',
            body: JSON.stringify({
                like: true
            })
        })
    }
}