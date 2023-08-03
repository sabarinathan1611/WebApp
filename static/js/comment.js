 // Receive new comments
 socket.on('comment', function(data) {
    var comment = document.createElement('p');
    comment.textContent = data.username + ': ' + data.comment; // Include username
    document.querySelector('#comment-container').appendChild(comment);
})
 idd=1

// Send comment
document.querySelector('#comment-form').addEventListener('submit', function(e) {
    e.preventDefault();
    var input = document.querySelector('#comment-input');
    var comment = input.value.trim();
    var messageId = idd;
    console.log(messageId);
    if (comment !== '') {
        socket.emit('comment', { 'comment': comment, 'message_id': messageId });
        input.value = '';
        document.querySelector('#message-id-input').value = '';
    }
});