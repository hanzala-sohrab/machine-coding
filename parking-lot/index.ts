import SpotType from "./enums/SpotType.ts";
import VehicleType from "./enums/VehicleType.ts";
import ParkingFloor from "./models/ParkingFloor.ts";
import ParkingSpot from "./models/ParkingSpot.ts";
import Vehicle from "./models/Vehicle.ts";
import ParkingLot from "./services/ParkingLot.ts";
import FirstAvailableStrategy from "./strategies/FirstAvailableStrategy.ts";

console.log("Parking Lot System");

console.log("Creating parking floor");
const floors = new ParkingFloor(1, [
  new ParkingSpot("1A", SpotType.SMALL),
  new ParkingSpot("1B", SpotType.MEDIUM),
  new ParkingSpot("1C", SpotType.LARGE),
]);
console.log("Parking floor created");

console.log("Creating parking lot");
const lot = new ParkingLot([floors], new FirstAvailableStrategy());
console.log("Parking lot created");

console.log("Creating car");
const car = new Vehicle("KA-01-HH-1234", VehicleType.CAR);
console.log("Car created");

console.log("Parking car");
const ticket = lot.park(car);
console.log("Ticket created", ticket?.ticketId);

console.log("Unparking car");
lot.unpark(ticket.ticketId);
console.log("Ticket unparked", ticket?.ticketId);
