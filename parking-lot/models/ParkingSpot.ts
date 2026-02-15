import SpotType from '../enums/SpotType.ts'
import VehicleType from '../enums/VehicleType.ts';
import Vehicle from './Vehicle.ts';

class ParkingSpot {
  private occupied = false;
  private vehicle: Vehicle | null = null;

  constructor(
    public readonly id: string,
    public readonly type: SpotType
  ) {}

  canFit(vehicle: Vehicle): boolean {
    console.log("Checking if vehicle can fit in spot")
    if (this.occupied) {
      console.log("Spot is occupied")
      return false;
    }

    switch (vehicle.type) {
      case VehicleType.BIKE:
        console.log("Vehicle is bike")
        return true;
      case VehicleType.CAR:
        console.log("Vehicle is car")
        return this.type !== SpotType.SMALL;
      case VehicleType.BUS:
        console.log("Vehicle is bus")
        return this.type === SpotType.LARGE;
    }
  }

  park(vehicle: Vehicle) {
    console.log("Parking vehicle in spot")
    if (!this.canFit(vehicle)) {
      console.log("Vehicle cannot fit in this spot")
      throw new Error('Vehicle cannot fit in this spot')
    }
    this.vehicle = vehicle;
    this.occupied = true;
    console.log("Vehicle parked in spot")
  }

  unpark(): Vehicle | null {
    console.log("Unparking vehicle from spot")
    if (!this.occupied) {
      console.log("Spot is already empty")
      throw new Error('Spot is already empty')
    }

    const vehicle = this.vehicle;
    this.vehicle = null;
    this.occupied = false;
    console.log("Vehicle unparked from spot")
    return vehicle;
  }

  isFree(): boolean {
    console.log("Checking if spot is free")
    return !this.occupied;
  }
}

export default ParkingSpot;
