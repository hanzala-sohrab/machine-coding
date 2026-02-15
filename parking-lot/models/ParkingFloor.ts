import ParkingSpot from "./ParkingSpot.ts";
import Vehicle from "./Vehicle.ts";

class ParkingFloor {
  constructor(
    public readonly floorNumber: number,
    private spots: ParkingSpot[]
  ) {}

  findSpot(vehicle: Vehicle): ParkingSpot | undefined {
    return this.spots.find((spot) => spot.canFit(vehicle));
  }

  getAvailableCount(): number {
    return this.spots.filter((spot) => spot.isFree()).length;
  }

  getSpots(): readonly ParkingSpot[] {
    return this.spots;
  }
}

export default ParkingFloor;
