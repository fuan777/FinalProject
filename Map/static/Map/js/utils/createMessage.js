export function createParkingMessage(status, { x, y }, handlers) {
    const msg = document.createElement('div');
    msg.className = 'parking-message';
    msg.innerHTML = `
        <p>Status: ${status}</p>
        <button class="park-btn">Parking</button>
        <button class="find-btn">Finding</button>
    `;

    msg.querySelector('.park-btn').onclick = handlers.onPark;
    msg.querySelector('.find-btn').onclick = handlers.onFind;

    document.addEventListener('click', function(event) {
        if (event.target !== msg && !msg.contains(event.target)) {
            msg.remove();
        }
    });

    document.body.appendChild(msg);
    return msg;
}
