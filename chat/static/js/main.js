$(document).ready(function(load) {

    function get_chats() {
        $.getJSON("/chats/", function(data) {
            var chats = []
            $.each(data, function(key, val) {
                chats.push("<li href='/chats/'" + key + "'>" + val + "</li>");
            });

            html = ''
            for (var i = 0; i < chats.length; i++) {
                html += chats[i]
            }
            $("#chats ul").append(html)
        });
    }
    get_chats()

    var chatName = $('#chatName')
    var webSocket = new WebSocket('ws://' + window.location.host + '/ws/chats/');

    webSocket.onmessage = function(message) {
        var data = JSON.parse(message.data)
        $("#chats ul").append("<li href='/chats/'" + data.chat_id + "'>" + data.chat_name + "</li>");
    }

    $('#newChatBtn').click(function(e) {
        webSocket.send(JSON.stringify({'name': chatName.val()}))
        $('#chatName').val('');
    })
});