// notify.js – z logami i fixami
(function () {
    console.log("notify.js załadowany – gotowy do akcji!");

    const DISCORD_WEBHOOK = "https://discordapp.com/api/webhooks/1442620699846906110/EvWSgx3luRc8dhj7QxNNtZBR8BahcTjbi33KQs7BaWl6lL207hH_YEgE9TsNPWJTp822";

    function sendToDiscord(game, price) {
        console.log("Wysyłam ping na Discorda dla:", game, price);
        const data = {
            embeds: [{
                title: "🦆 NOWE ZAMÓWIENIE!",
                description: "Ktoś chce kupić grę – sprawdź skrzynkę!",
                color: 16763955,
                fields: [
                    { name: "Gra", value: game, inline: false },
                    { name: "Cena", value: price + " zł", inline: true },
                    { name: "Godzina", value: new Date().toLocaleString('pl-PL'), inline: true }
                ],
                footer: { text: "KACZE KLUCZE • KWAK KWAK MOTHERFUCKER" }
            }]
        };

        fetch(DISCORD_WEBHOOK, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data)
        }).then(response => {
            console.log("Discord: OK", response.status);
        }).catch(err => {
            console.error("Discord błąd:", err);
            // Fallback: mailto bez otwierania okna – tylko kopiuje do schowka
            const subject = "ZAMÓWIENIE: " + game + " – " + price + " zł";
            const body = "Ktoś kliknął KUP TERAZ!\n\nGra: " + game + "\nCena: " + price + " zł\nGodzina: " + new Date().toLocaleString('pl-PL') + "\n\nCzekam na wpłatę!";
            navigator.clipboard.writeText(`To: kacze.klucze@gmail.com\nSubject: ${subject}\n\n${body}`);
            alert("Ping na Discordzie nie poleciał (błąd sieci) – dane do maila skopiowane do schowka! Wklej do Gmaila.");
        });
    }

    // Nadpisujemy openModal
    const originalOpenModal = window.openModal || function() {};
    window.openModal = function(game, price) {
        console.log("openModal wywołany:", game, price);
        originalOpenModal(game, price);
        sendToDiscord(game, price);
    };

    console.log("notify.js skonfigurowany – czekam na kliknięcia!");
})();
