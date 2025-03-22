import { renderMap } from './components/GridRenderer.js';
import { ParkingController } from './controllers/ParkingController.js';

const initialMap = window.initialMap;
const controller = new ParkingController(initialMap);

renderMap(initialMap);
console.log(initialMap);
controller.bindClick();
