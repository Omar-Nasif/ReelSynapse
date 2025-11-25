import pandas as pd
import numpy as np

def get_inventory_snapshot() -> pd.DataFrame:
    materials = ["Copper", "Aluminum", "PVC", "XLPE", "HDPE"]

    current_stock = np.random.randint(5, 50, size=len(materials))
    safety_stock = np.random.randint(10, 30, size=len(materials))
    reorder_point = safety_stock + np.random.randint(5, 15, size=len(materials))

    status = []
    for c, r, s in zip(current_stock, reorder_point, safety_stock):
        if c < s:
            status.append("Critical")
        elif c < r:
            status.append("Low")
        else:
            status.append("OK")

    df = pd.DataFrame(
        {
            "Material": materials,
            "Current Stock (tons)": current_stock,
            "Safety Stock (tons)": safety_stock,
            "Reorder Point (tons)": reorder_point,
            "Status": status,
        }
    )
    return df


def run_scenario(
    base_demand: float,
    price_change_pct: int,
    demand_change_pct: int,
    lead_time_change_pct: int,
) -> dict:
    demand_factor = 1 + demand_change_pct / 100.0
    price_factor = 1 + price_change_pct / 100.0
    lead_time_factor = 1 + lead_time_change_pct / 100.0

    new_demand = base_demand * demand_factor
    new_cost_index = new_demand * price_factor
    shortage_risk = max(0, demand_change_pct + lead_time_change_pct / 2)

    return {
        "new_demand": new_demand,
        "estimated_cost_index": new_cost_index,
        "shortage_risk_pct": shortage_risk,
        "price_factor": price_factor,
        "demand_factor": demand_factor,
        "lead_time_factor": lead_time_factor,
    }