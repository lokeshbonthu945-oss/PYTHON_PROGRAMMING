class RailwayFareCalculator:

    def __init__(self, reservation_fee=25.0):
        # Distance Slabs: (Max Distance, Rate per KM)
        # float('inf') represents distances above 500 km
        self.distance_slabs = [
            (200, 1.50),  # 0 to 200 km -> $1.50/km
            (500, 1.25),  # 201 to 500 km -> $1.25/km
            (float("inf"), 1.00),  # 501+ km -> $1.00/km
        ]

        # Travel Class Multipliers
        self.class_multipliers = {
            "Sleeper": 1.0,
            "AC_3Tier": 1.75,
            "AC_2Tier": 2.25,
            "AC_1Tier": 3.00,
        }

        self.reservation_fee = reservation_fee

    def _get_base_rate(self, distance):
        for limit, rate in self.distance_slabs:
            if distance <= limit:
                return rate
        return self.distance_slabs[-1][1]

    def _get_concession_multiplier(self, age):
        if age < 12:
            return 0.50  # 50% discount for children
        elif age >= 60:
            return 0.60  # 40% discount for senior citizens
        return 1.00  # Regular adult fare

    def calculate_trip_fare(self, trip_distance, travel_class, passengers):
        if travel_class not in self.class_multipliers:
            raise ValueError(f"Invalid travel class: {travel_class}")

        base_rate = self._get_base_rate(trip_distance)
        class_multiplier = self.class_multipliers[travel_class]

        itemized_results = []
        total_revenue = 0.0
        total_refunds = 0.0

        for p in passengers:
            name = p["name"]
            age = p["age"]
            is_cancelled = p.get("is_cancelled", False)

            # Raw distance cost adjusted for class
            raw_fare = trip_distance * base_rate * class_multiplier

            # Apply age concession
            concession_multiplier = self._get_concession_multiplier(age)
            discounted_fare = raw_fare * concession_multiplier

            # Add reservation fee
            net_ticket_price = discounted_fare + self.reservation_fee

            passenger_record = {
                "name": name,
                "age": age,
                "category": (
                    "Child"
                    if age < 12
                    else ("Senior Citizen" if age >= 60 else "Adult")
                ),
                "raw_fare": round(raw_fare, 2),
                "discounted_fare": round(discounted_fare, 2),
                "reservation_fee": self.reservation_fee,
                "status": "Cancelled" if is_cancelled else "Confirmed",
            }

            if is_cancelled:
                # 20% cancellation penalty on ticket price, reservation fee non-refundable
                penalty = net_ticket_price * 0.20
                refund_amount = net_ticket_price - penalty
                passenger_record["penalty"] = round(penalty, 2)
                passenger_record["refund_amount"] = round(refund_amount, 2)
                total_refunds += refund_amount
            else:
                passenger_record["final_payable"] = round(net_ticket_price, 2)
                total_revenue += net_ticket_price

            itemized_results.append(passenger_record)

        return {
            "trip_distance_km": trip_distance,
            "travel_class": travel_class,
            "base_rate_per_km": base_rate,
            "passengers": itemized_results,
            "total_net_revenue": round(total_revenue, 2),
            "total_refunds_issued": round(total_refunds, 2),
        }


# --- Sample Execution ---
if __name__ == "__main__":
    calculator = RailwayFareCalculator(reservation_fee=30.0)

    # Trip configuration
    distance_km = 450  # Falls in the 201-500 km slab ($1.25/km base rate)
    selected_class = "AC_3Tier"  # Multiplier: 1.75

    # Group passenger list
    passenger_list = [
        {"name": "Arthur Pendelton", "age": 42, "is_cancelled": False},  # Adult
        {"name": "Evelyn Pendelton", "age": 63, "is_cancelled": False},  # Senior
        {"name": "Leo Pendelton", "age": 9, "is_cancelled": False},  # Child
        {
            "name": "Marcus Vance",
            "age": 35,
            "is_cancelled": True,
        },  # Cancelled ticket
    ]

    report = calculator.calculate_trip_fare(
        distance_km, selected_class, passenger_list
    )

    print("=== RAILWAY FARE & RESERVATION CALCULATOR REPORT ===")
    print(f"Distance: {report['trip_distance_km']} km | Class: {report['travel_class']}")
    print(f"Base Rate: ${report['base_rate_per_km']}/km\n")

    print("--- PASSENGER ITEMIZATION ---")
    for p in report["passengers"]:
        print(f"Passenger: {p['name']} ({p['category']}, Age {p['age']})")
        print(f"  - Status: {p['status']}")
        if p["status"] == "Confirmed":
            print(f"  - Discounted Fare: ${p['discounted_fare']}")
            print(f"  - Reservation Fee: ${p['reservation_fee']}")
            print(f"  - Payable Total:   ${p['final_payable']}")
        else:
            print(f"  - Cancellation Penalty: ${p['penalty']}")
            print(f"  - Refund Issued:        ${p['refund_amount']}")
        print()

    print("--- FINANCIAL SUMMARY ---")
    print(f"Total Net Revenue (Confirmed): ${report['total_net_revenue']}")
    print(f"Total Refunds Issued (Cancelled): ${report['total_refunds_issued']}")
