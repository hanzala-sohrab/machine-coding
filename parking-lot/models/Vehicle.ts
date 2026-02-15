import VehicleType from '../enums/VehicleType.ts';

class Vehicle {
  constructor(
    public readonly licenseNumber: string,
    public readonly type: VehicleType
  ) {}
}

export default Vehicle;
