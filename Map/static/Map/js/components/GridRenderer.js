import { colorMap } from '../utils/constant.js';

export function renderMap(mapData, containerId = 'grid') {
    const container = document.getElementById(containerId);
    container.innerHTML = '';
    mapData.forEach((row, x) => {
        row.forEach((cell, y) => {
            const div = document.createElement('div');
            div.className = 'grid-item';
            div.style.backgroundColor = colorMap.get(cell);
            div.dataset.x = x;
            div.dataset.y = y;
            container.appendChild(div);
        });
    });
}
