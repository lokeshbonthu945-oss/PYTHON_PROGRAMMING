class ElectricityBillingSystem:

    def __init__(
        self, slabs, fixed_charge=50.0, tax_rate=0.05, anomaly_threshold=0.35
    ):
        """Slabs format: List of tuples -> [(upper_limit, rate_per_unit), ...]

        Use float('inf') for the final open-ended tier.
        """
        self.slabs = slabs
        self.fixed_charge = fixed_charge
        self.tax_rate = tax_rate
        self.anomaly_threshold = anomaly_threshold

    def calculate_monthly_bill(self, units):
        energy_charge = 0.0
        remaining_units = units
        previous_limit = 0

        for limit, rate in self.slabs:
            if remaining_units <= 0:
                break
            slab_range = (
                limit - previous_limit
                if limit != float("inf")
                else float("inf")
            )
            units_in_slab = min(remaining_units, slab_range)
            energy_charge += units_in_slab * rate
            remaining_units -= units_in_slab
            previous_limit = limit

        tax = energy_charge * self.tax_rate
        total_bill = energy_charge + self.fixed_charge + tax

        return {
            "units": units,
            "energy_charge": round(energy_charge, 2),
            "fixed_charge": self.fixed_charge,
            "tax": round(tax, 2),
            "total_bill": round(total_bill, 2),
        }

    def analyze_household_trends(self, monthly_records):
        analyzed_results = []
        previous_units = None

        for month, units in monthly_records.items():
            bill_info = self.calculate_monthly_bill(units)
            bill_info["month"] = month

            status = "Normal"
            pct_increase = 0.0

            if previous_units is not None and previous_units > 0:
                pct_increase = (units - previous_units) / previous_units
                if pct_increase >= self.anomaly_threshold:
                    status = f"⚠️ UNUSUAL INCREASE (+{pct_increase*100:.1f}%)"
                else:
                    status = (
                        f"Stable ({pct_increase*100:+.1f} compared to last month)"
                    )
            else:
                status = "Baseline Month"

            bill_info["status"] = status
            analyzed_results.append(bill_info)
            previous_units = units

        return analyzed_results


# --- Sample Execution ---
if __name__ == "__main__":
    # Slab structure:
    # 0 - 100 units @ $3.5 per unit
    # 101 - 300 units @ $5.0 per unit
    # 301+ units @ $7.5 per unit
    tier_slabs = [(100, 3.5), (300, 5.0), (float("inf"), 7.5)]

    billing_system = ElectricityBillingSystem(
        slabs=tier_slabs, fixed_charge=60.0, tax_rate=0.08
    )

    # Historical consumption data across several months
    household_consumption = {
        "January": 210,
        "February": 195,
        "March": 220,
        "April": 215,
        "May": 420,  # Sudden sharp increase (e.g., AC usage / appliance fault)
        "June": 440,
    }

    report = billing_system.analyze_household_trends(household_consumption)

    print("=== PROGRESSIVE ELECTRICITY BILLING & TREND ANALYSIS ===")
    for record in report:
        print(f"\nMonth: {record['month']} ({record['units']} kWh)")
        print(f"  - Energy Charge: ${record['energy_charge']}")
        print(f"  - Fixed Charge:  ${record['fixed_charge']}")
        print(f"  - Taxes (8%):    ${record['tax']}")
        print(f"  - Total Bill:    ${record['total_bill']}")
        print(f"  - Trend Status:  {record['status']}")
