// Material Design functionality
mdc.textField.MDCTextField.attachTo(document.querySelector('.name'))
mdc.textField.MDCTextField.attachTo(document.querySelector('.room'))
mdc.ripple.MDCRipple.attachTo(document.querySelector('.signin'))
mdc.ripple.MDCRipple.attachTo(document.querySelector('.send'))

// Hide Chatroom on start
$(document).ready(function () {
  $('#chatroom').hide();
});

// Initialize Socket.io
var socket = io();

// On sign in
$('#signin').submit(e => {
  e.preventDefault();
  const name = $('#name').val();
  const room = $('#room').val();
  socket.emit('login', {name, room}, (error) => {
    if (error) {
      console.log(error);
    }
    $('#signin').hide();
    setChatroom(room)
    $('#chatroom').show();
  });
});

// Send chat message
$('#chat').submit(e => {
  e.preventDefault();
  const msg = $('#msg').val();
  socket.emit('sendMessage', msg, (error) => {
    if (error) {
      console.log(error);
    }
  });
  $('#msg').val('');
});

// Listen for new messages
socket.on('message', (msg) => {
  log(msg.user, msg.text);
});

// Listen for notifications
socket.on('notification', (msg) => {
  log(msg.title, msg.description);
});

// Helper function to set chatroom name
function setChatroom(room) {
  $('#chatroom h1').append(room);
}

// Helper function to print to chatroom
function log(name, msg) {
  $('#messages').append(`<li> <strong>${name}</strong>: ${msg}`);
  window.scrollTo(0, document.body.scrollHeight);
}
