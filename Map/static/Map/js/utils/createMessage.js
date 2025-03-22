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

    document.body.appendChild(msg);
    return msg;
}
