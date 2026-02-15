import SpotType from "./enums/SpotType.ts";
import VehicleType from "./enums/VehicleType.ts";
import ParkingFloor from "./models/ParkingFloor.ts";
import ParkingSpot from "./models/ParkingSpot.ts";
import Vehicle from "./models/Vehicle.ts";
import ParkingLot from "./services/ParkingLot.ts";
import FirstAvailableStrategy from "./strategies/FirstAvailableStrategy.ts";

const floors = new ParkingFloor(1, [
  new ParkingSpot("1A", SpotType.SMALL),
  new ParkingSpot("1B", SpotType.MEDIUM),
  new ParkingSpot("1C", SpotType.LARGE),
]);

const lot = new ParkingLot([floors], new FirstAvailableStrategy());

const car = new Vehicle("KA-01-HH-1234", VehicleType.CAR);
const ticket = lot.park(car);

lot.unpark(ticket.ticketId);
