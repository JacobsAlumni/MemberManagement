import './index.css';

const total_donations = document.getElementById('total-donations') as HTMLDivElement;
const new_donations = document.getElementById('current-donations') as HTMLDivElement;


function formatAmount(amount: number) {
    const inEuros = amount / 100;

    return `${inEuros.toFixed(2)} €`
}


const socket = new WebSocket('ws://' + window.location.host + window.location.pathname);
socket.onmessage = function (event) {
    const {
        amounts: {
            total,
            current
        }
    } = JSON.parse(event.data)

    total_donations.innerHTML = "";
    total_donations.appendChild(
        document.createTextNode(`${formatAmount(total)} donated since 2020`)
    )

    if(current){
        const li = document.createElement('li')
        li.innerHTML = `<li>${formatAmount(current)}</li>`

        new_donations.appendChild(li)
    }
}