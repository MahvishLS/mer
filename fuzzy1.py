import numpy as np
import matplotlib.pyplot as plt

def low_rainfall(rain):
    """Low rainfall membership function."""
    if rain <= 50:
        return 1.0
    elif 50 < rain <= 100:
        return (100 - rain) / 50
    else:
        return 0.0

def moderate_rainfall(rain):
    """Moderate rainfall membership function."""
    if 75 < rain <= 125:
        return (rain - 75) / 50
    elif 125 < rain <= 175:
        return (175 - rain) / 50
    else:
        return 0.0

def high_rainfall(rain):
    """High rainfall membership function."""
    if rain <= 150:
        return 0.0
    elif 150 < rain <= 200:
        return (rain - 150) / 50
    else:
        return 1.0

rain_values = np.linspace(0, 300, 300)

low_vals      = [low_rainfall(r) for r in rain_values]
moderate_vals = [moderate_rainfall(r) for r in rain_values]
high_vals     = [high_rainfall(r) for r in rain_values]

plt.figure(figsize=(8, 5))
plt.plot(rain_values, low_vals,      label="Low Rainfall", color='blue')
plt.plot(rain_values, moderate_vals, label="Moderate Rainfall", color='orange')
plt.plot(rain_values, high_vals,     label="High Rainfall", color='green')

plt.title("Fuzzy Membership Functions for Rainfall")
plt.xlabel("Rainfall (mm/month)")
plt.ylabel("Membership Degree (0 to 1)")
plt.ylim(0, 1.05)
plt.legend()
plt.grid(True)
plt.show()
