import ParkingFloor from "../models/ParkingFloor.ts";
import ParkingSpot from "../models/ParkingSpot.ts";
import Vehicle from "../models/Vehicle.ts";
import type { ParkingStrategy } from "./ParkingStrategy.ts";

class FirstAvailableStrategy implements ParkingStrategy {
  findSpot(floors: ParkingFloor[], vehicle: Vehicle): ParkingSpot | undefined {
    for (const floor of floors) {
      const spot = floor.findSpot(vehicle);
      if (spot) {
        return spot;
      }
    }
  }
}

export default FirstAvailableStrategy;
