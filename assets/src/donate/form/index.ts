import './index.css';

const total_donations = document.getElementById('total-donations') as HTMLDivElement;
const new_donations = document.getElementById('current-donations') as HTMLDivElement;
const live_display = document.getElementById('live-display') as HTMLDivElement

const thankYous = [
    "Very generous.",
    "Thank You!",
    "Much appreciated!"
]


function numberWithDots(x: string) {
    return x.toString().replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ".");
}

function formatAmount(amount: number) {
    const inEuros = (amount / 100).toLocaleString('de')


    return `${inEuros} €`
}

const prot = window.location.protocol.replace("http", "ws")

const socket = new WebSocket(prot + '//' + window.location.host + window.location.pathname);

socket.onclose = function () {
    live_display.classList.add("uk-hidden")
}

socket.onmessage = function (event) {
    live_display.classList.remove("uk-hidden")

    const {
        amounts: {
            total,
            current,
            for_target
        }
    } = JSON.parse(event.data)

    total_donations.innerHTML = "";
    total_donations.appendChild(
        document.createTextNode(`${formatAmount(total)} donated since 2020`)
    )

    if(current){
        const li = document.createElement('li')
        li.innerHTML = formatAmount(current)

        if(for_target) {
            li.innerHTML += ` for ${for_target}`
        }

        li.innerHTML += `. ${thankYous[Math.floor(Math.random() * thankYous.length)]}`

        new_donations.appendChild(li)
    }
}