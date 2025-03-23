import { createParkingMessage } from '../utils/createMessage.js';
import { createLoader } from '../utils/createLoader.js';
import { api } from '../services/api.js';
import { renderMap } from '../components/GridRenderer.js';
import { showErrorMessage } from '../components/PopNotice.js';
import { logManager } from './LogManager.js';


export class ParkingController {
    constructor(initialMap) {
        this.map = initialMap;
        this.loader = createLoader();
        this.exitBtn = document.getElementById('exitBtn');
        this.initExitBtn();
    }

    initExitBtn() {
        this.exitBtn.onclick = async () => {
            this.loader.show();
            const data = await api.reset();
            if (data.status === 'success') renderMap(data.map);
            this.exitBtn.style.display = 'none';
            this.loader.hide();
        };
    }

    bindClick(containerId = 'grid') {
        document.getElementById(containerId).onclick = (e) => {
            const target = e.target.closest('.grid-item');
            if (!target) return;

            const { x, y } = target.dataset;
            const cellStatus = this.map[x][y];
            if (!['occupy', 'free'].includes(cellStatus)) return;

            document.querySelectorAll('.parking-message').forEach(m => m.remove());

            const rect = target.getBoundingClientRect();
            const msg = createParkingMessage(cellStatus, { x, y }, {
                onPark: () => this.handleParking({ x, y }),
                onFind: () => this.handleFinding({ x, y })
            });

            msg.style.top = `${rect.top + window.scrollY}px`;
            msg.style.left = `${rect.right + 10 + window.scrollX}px`;

            e.stopPropagation();
        };
    }

    async handleParking(coords) {
        this.loader.show();
        const data = await api.parking(coords);

        if (data.status === 'success') {
            renderMap(data.map);

            logManager.addEntry('🟢 PATH DETAILS:');
            data.path.forEach((cells, index) => {
                logManager.addEntry(`第 ${index + 1} 步: (${cells.map(c => c.join(',')).join(' | ')})`, {
                    cells: cells  // 👈 保存用于按钮点击
                });
            });
        }else {
            showErrorMessage(data.message);
        }
        this.loader.hide();
        this.exitBtn.style.display = 'block';

        document.querySelectorAll('.parking-message').forEach(m => m.remove());
    }

    async handleFinding(coords) {
        this.loader.show();
        const data = await api.finding(coords);
        if (data.status === 'success') {
            renderMap(data.map);
        }
        this.loader.hide();
        this.exitBtn.style.display = 'block';

        document.querySelectorAll('.parking-message').forEach(m => m.remove());
    }
}
