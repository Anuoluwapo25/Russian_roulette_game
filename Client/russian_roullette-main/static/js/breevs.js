let tg = window.Telegram.WebApp;

tg.expand();

function sendMessage() {
    tg.sendData("Hello from Mini App!");
}

tg.onEvent('mainButtonClicked', function(){
    tg.sendData("Main button was clicked");
});

tg.ready();