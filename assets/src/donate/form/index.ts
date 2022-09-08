import './index.css';

const live_display = document.getElementById('live-display') as HTMLDivElement
const donation_totals = document.getElementById('donation_totals') as HTMLUListElement
const recent_donation = document.getElementById('recent-donation') as HTMLSpanElement
const id_amount_0 = document.getElementById('id_amount_0') as HTMLDivElement

// force english locale for the amount input!
// this *should* be the default, but we want to make sure.
const LOCALE = 'en'
id_amount_0?.setAttribute('lang', LOCALE)


const currencyNames: Record<string, string> = {
    'eur': '€',
    'usd': '$',
}

/** formatAmount formats an amount of a specific currency to a string */
function formatAmount(amount: number, currency: string): string {
    const inFull = (amount / 100).toLocaleString(LOCALE)
    const curName = currencyNames[currency] ?? currency
    return `${inFull} ${curName}`
}

/** An event representing a new donation */
type DonationEvent = {
    amounts: {
        total: Record<string, number>;
        current?: {amount: number, currency: string};
        for_target: string | null;
    }
}

const prot = window.location.protocol.replace("http", "ws")

const socket = new WebSocket(prot + '//' + window.location.host + window.location.pathname)

socket.onclose = function () {
    live_display.classList.add("uk-hidden")
}


const thankYous = [
    "Very generous.",
    "Thank You!",
    "Much appreciated!"
]

socket.onmessage = function (event) {
    live_display.classList.remove("uk-hidden")

    const {
        amounts: {
            total,
            current,
            for_target
        }
    } = JSON.parse(event.data) as DonationEvent

    donation_totals.innerHTML = '';
    Array.from(Object.entries(total))
        .sort(([a1, c1], [a2, c2]) => c1 - c2)
        .forEach(([cur, am]) => {
            const li = document.createElement('li')
            li.appendChild(
                document.createTextNode(formatAmount(am, cur))
            )
            donation_totals.appendChild(li)
        })
    
    if (!current) return
    const { amount, currency } = current;

    let text = formatAmount(amount, currency)
    if (for_target) {
        text += ` for ${for_target}`
    }
    text += `. ${thankYous[Math.floor(Math.random() * thankYous.length)]}`

    recent_donation.innerHTML = ""
    recent_donation.append(
        document.createTextNode(text)
    )
}