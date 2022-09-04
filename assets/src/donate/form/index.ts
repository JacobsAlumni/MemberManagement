const total_donations = document.getElementById('total_donations') as HTMLDivElement;

const socket = new WebSocket('ws://' + window.location.host + window.location.pathname);
socket.onmessage = function(event) {
    total_donations.innerHTML = "";
    total_donations.appendChild(
        document.createTextNode(JSON.stringify(event.data))
    )
}