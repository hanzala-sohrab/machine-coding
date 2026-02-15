import Ticket from "../models/Ticket.ts"
import ParkingFloor from "../models/ParkingFloor.ts";
import type { ParkingStrategy } from "../strategies/ParkingStrategy.ts";
import Vehicle from "../models/Vehicle.ts";

class ParkingLot {
  private tickets = new Map<string, Ticket>();

  constructor(
    private floors: ParkingFloor[],
    private parkingStrategy: ParkingStrategy
  ) {}

  park(vehicle: Vehicle) {
    const spot = this.parkingStrategy.findSpot(this.floors, vehicle);
    if (!spot) {
      throw new Error("No available spots");
    }

    spot.park(vehicle);
    const ticket = new Ticket(
      `T-${Date.now()}`,
      vehicle,
      spot,
      new Date(),
    );

    this.tickets.set(ticket.ticketId, ticket);
    return ticket;
  }

  unpark(ticketId: string): Vehicle | null {
    const ticket = this.tickets.get(ticketId);
    if (!ticket) {
      throw new Error('Invalid ticket');
    }

    const vehicle = ticket.parkingSpot.unpark();
    this.tickets.delete(ticketId);
    return vehicle;
  }
}

export default ParkingLot;
