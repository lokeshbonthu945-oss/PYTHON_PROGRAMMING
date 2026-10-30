class WarehouseReconciliationSystem:

    def __init__(self, default_safety_buffer=20, default_target_stock=100):
        self.default_safety_buffer = default_safety_buffer
        self.default_target_stock = default_target_stock

    def reconcile_inventory(self, inventory_records):
        reconciliation_results = []
        replenishment_orders = []

        for item in inventory_records:
            prod_id = item["product_id"]
            name = item["name"]
            opening = item["opening_stock"]
            incoming = item["incoming"]
            dispatched = item["dispatched"]
            actual_physical = item["actual_physical_stock"]
            min_safety = item.get("min_safety_stock", self.default_safety_buffer)
            target_stock = item.get("target_stock", self.default_target_stock)

            # 1. Calculate Expected Closing Stock
            expected_closing = opening + incoming - dispatched

            # 2. Compute Discrepancy (Actual vs Expected)
            discrepancy = actual_physical - expected_closing

            if discrepancy < 0:
                status = f"⚠️ SHORTAGE ({abs(discrepancy)} units missing)"
            elif discrepancy > 0:
                status = f"➕ SURPLUS (+{discrepancy} unrecorded units)"
            else:
                status = "✅ Balanced (Matched perfectly)"

            # 3. Evaluate Replenishment Needs
            reorder_qty = 0
            needs_reorder = False
            if actual_physical < min_safety:
                needs_reorder = True
                reorder_qty = max(0, target_stock - actual_physical)
                replenishment_orders.append({
                    "product_id": prod_id,
                    "name": name,
                    "current_stock": actual_physical,
                    "suggested_reorder_qty": reorder_qty,
                })

            reconciliation_results.append({
                "product_id": prod_id,
                "name": name,
                "opening_stock": opening,
                "incoming": incoming,
                "dispatched": dispatched,
                "expected_closing": expected_closing,
                "actual_physical_stock": actual_physical,
                "discrepancy": discrepancy,
                "audit_status": status,
                "needs_replenishment": needs_reorder,
                "reorder_quantity": reorder_qty,
            })

        return reconciliation_results, replenishment_orders


# --- Sample Execution ---
if __name__ == "__main__":
    warehouse_system = WarehouseReconciliationSystem()

    # Sample inventory data across multiple warehouse SKUs
    warehouse_inventory = [
        {
            "product_id": "SKU-101",
            "name": "Wireless Ergonomic Mouse",
            "opening_stock": 150,
            "incoming": 200,
            "dispatched": 280,
            "actual_physical_stock": 68,  # Expected: 150+200-280 = 70 (-2 discrepancy)
            "min_safety_stock": 50,
            "target_stock": 150,
        },
        {
            "product_id": "SKU-102",
            "name": "Mechanical Gaming Keyboard",
            "opening_stock": 80,
            "incoming": 50,
            "dispatched": 110,
            "actual_physical_stock": 20,  # Expected: 80+50-110 = 20 (Balanced)
            "min_safety_stock": 30,  # Falls below safety stock -> Needs replenishment
            "target_stock": 100,
        },
        {
            "product_id": "SKU-103",
            "name": "UltraWide 4K Monitor 27-inch",
            "opening_stock": 45,
            "incoming": 30,
            "dispatched": 35,
            "actual_physical_stock": 42,  # Expected: 45+30-35 = 40 (+2 surplus)
            "min_safety_stock": 15,
            "target_stock": 60,
        },
        {
            "product_id": "SKU-104",
            "name": "USB-C Multiport Hub",
            "opening_stock": 300,
            "incoming": 100,
            "dispatched": 395,
            "actual_physical_stock": 3,  # Expected: 300+100-395 = 5 (-2 shortage)
            "min_safety_stock": 25,  # Critical low stock -> Reorder required
            "target_stock": 200,
        },
    ]

    report, purchase_orders = warehouse_system.reconcile_inventory(warehouse_inventory)

    print("=== WAREHOUSE INVENTORY RECONCILIATION REPORT ===")
    for item in report:
        print(f"\nProduct: {item['name']} ({item['product_id']})")
        print(f"  - Opening: {item['opening_stock']} | Incoming: +{item['incoming']} | Dispatched: -{item['dispatched']}")
        print(f"  - Expected Closing: {item['expected_closing']} | Physical Count: {item['actual_physical_stock']}")
        print(f"  - Discrepancy Status: {item['audit_status']}")
        if item["needs_replenishment"]:
            print(f"  ⚠️ REPLENISHMENT ALERT: Stock below safety threshold! Suggested Order: {item['reorder_quantity']} units")

    print("\n--- GENERATED PURCHASE ORDERS (REPLENISHMENT LIST) ---")
    if purchase_orders:
        for po in purchase_orders:
            print(f"• Reorder {po['suggested_reorder_qty']} units of {po['name']} ({po['product_id']})")
    else:
        print("No replenishment orders required at this time.")
