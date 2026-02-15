import Vehicle from "./Vehicle.ts";
import ParkingSpot from "./ParkingSpot.ts";

class Ticket {
  constructor(
    public readonly ticketId: string,
    public readonly vehicle: Vehicle,
    public readonly parkingSpot: ParkingSpot,
    public readonly entryTime: Date,
  ) {}
}

export default Ticket;
