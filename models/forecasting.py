import pandas as pd
import numpy as np

MATERIALS = ["Copper", "Aluminum", "PVC", "XLPE", "HDPE"]

def get_materials():

    return MATERIALS

def get_forecast(material: str, horizon_days: int = 30) -> pd.DataFrame:
    """
    now its just dummy func 
    """
    dates = pd.date_range("2025-01-01", periods=horizon_days)

    # Dummy actual
    actual = np.random.randint(80, 120, size=horizon_days)

    # forcecast=dummy+Some Noise
    forecast = actual + np.random.randint(-10, 10, size=horizon_days)

    df = pd.DataFrame(
        {
            "date": dates,
            "actual": actual,
            "forecast": forecast,
        }
    )
    return df