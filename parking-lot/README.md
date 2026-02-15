# Parking Lot

A low-level design (LLD) implementation of a Parking Lot system in TypeScript, following **SOLID** principles and the **Strategy** design pattern.

## Features

- Multi-floor parking support
- Vehicle type-based spot allocation (Bike, Car, Bus)
- Spot size compatibility (Small, Medium, Large)
- Pluggable parking strategies (e.g., First Available)
- Ticket-based park/unpark flow

## Architecture

```
parking-lot/
├── enums/
│   ├── SpotType.ts          # SMALL | MEDIUM | LARGE
│   └── VehicleType.ts       # BIKE | CAR | BUS
├── models/
│   ├── ParkingFloor.ts      # Floor with a collection of spots
│   ├── ParkingSpot.ts       # Spot with type, occupancy & vehicle fitting logic
│   ├── Ticket.ts            # Issued on parking, used for unparking
│   └── Vehicle.ts           # Vehicle with license number & type
├── services/
│   └── ParkingLot.ts        # Core service: park & unpark operations
├── strategies/
│   ├── ParkingStrategy.ts   # Strategy interface
│   └── FirstAvailableStrategy.ts  # Picks the first available fitting spot
├── index.ts                 # Entry point / demo
└── package.json
```

## Spot Allocation Rules

| Vehicle | Small Spot | Medium Spot | Large Spot |
|---------|-----------|-------------|------------|
| Bike    | ✅        | ✅          | ✅         |
| Car     | ❌        | ✅          | ✅         |
| Bus     | ❌        | ❌          | ✅         |

## Usage

```bash
npm start
```

### Example

```typescript
import SpotType from "./enums/SpotType.ts";
import VehicleType from "./enums/VehicleType.ts";
import ParkingFloor from "./models/ParkingFloor.ts";
import ParkingSpot from "./models/ParkingSpot.ts";
import Vehicle from "./models/Vehicle.ts";
import ParkingLot from "./services/ParkingLot.ts";
import FirstAvailableStrategy from "./strategies/FirstAvailableStrategy.ts";

const floor = new ParkingFloor(1, [
  new ParkingSpot("1A", SpotType.SMALL),
  new ParkingSpot("1B", SpotType.MEDIUM),
  new ParkingSpot("1C", SpotType.LARGE),
]);

const lot = new ParkingLot([floor], new FirstAvailableStrategy());

const car = new Vehicle("KA-01-HH-1234", VehicleType.CAR);
const ticket = lot.park(car);

lot.unpark(ticket.ticketId);
```

## Design Patterns

- **Strategy Pattern** — `ParkingStrategy` interface allows swapping parking algorithms without modifying `ParkingLot`. Add a new strategy by implementing the interface.
- **Single Responsibility** — Each class has a focused purpose (spot fitting logic, ticket management, floor traversal, etc.)

## Prerequisites

- Node.js v22+ (uses native TypeScript support with `--experimental-transform-types` for enum support)
