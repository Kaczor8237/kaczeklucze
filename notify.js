// notify.js – automatyczne powiadomienie na Discorda + backup mailto
// Wrzuć ten plik w ten sam folder co index.html

(function () {
    // Twój webhook – już wklejony!
    const DISCORD_WEBHOOK = "https://discordapp.com/api/webhooks/1442620699846906110/EvWSgx3luRc8dhj7QxNNtZBR8BahcTjbi33KQs7BaWl6lL207hH_YEgE9TsNPWJTp822";

    function sendToDiscord(game, price) {
        const data = {
            embeds: [{
                title: "NOWE ZAMÓWIENIE!",
                description: "Ktoś właśnie chce kupić grę!",
                color: 16763955, // żółty kaczy
                fields: [
                    { name: "Gra", value: game, inline: false },
                    { name: "Cena", value: price + " zł", inline: true },
                    { name: "Godzina", value: new Date().toLocaleString('pl-PL'), inline: true }
                ],
                footer: { text: "KACZE KLUCZE • KWAK KWAK MOTHERFUCKER" },
                thumbnail: { url: "https://kaczeklucze-bot.github.io/kaczeklucze/logo.png" }
            }]
        };

        fetch(DISCORD_WEBHOOK, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data)
        });
    }

    // Nadpisujemy Twoją funkcję openModal
    const originalOpenModal = window.openModal || function() {};
    window.openModal = function(game, price) {
        // Twoje normalne rzeczy (modal + PayPal)
        originalOpenModal(game, price);

        // NATYCHMIASTOWE POWIADOMIENIE NA DISCORDA
        sendToDiscord(game, price);

        // Backup: otwiera mailto (na wszelki wypadek)
        const mailto = `mailto:kacze.klucze@gmail.com?subject=ZAMÓWIENIE: ${encodeURIComponent(game)} – ${price} zł&body=${encodeURIComponent(
            "Ktoś właśnie kliknął KUP TERAZ!\n\nGra: " + game + "\nCena: " + price + " zł\nGodzina: " + new Date().toLocaleString('pl-PL') + "\n\nCzekam na wpłatę!"
        )}`;
        window.open(mailto, '_blank');
    };
})();
