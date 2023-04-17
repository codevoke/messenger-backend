/*
const socket = io();
socket.on('connect', function () {
    let id = getCookie('id')
    let data = {
        'id': id
    }
    socket.emit('connect', data)
});
socket.on('new_chat', function (data) {


});

socket.on('confirm_new_chat', function (){
    return {'confirm': true};
});
*/
// search listener and handler


// - - - - - EVENTS - - - - - 


const search_input = document.querySelector('.menu-search')

search_input.oninput = function () {
    console.log(search_input.value)
}
