import ParkingFloor from "../models/ParkingFloor.ts";
import Vehicle from "../models/Vehicle.ts";
import ParkingSpot from "../models/ParkingSpot.ts";

export interface ParkingStrategy {
  findSpot(
    floors: ParkingFloor[],
    vehicle: Vehicle
  ): ParkingSpot | undefined;
}
