def calculate_acwr(acute_load, chronic_load):
    if chronic_load <= 0:
        return 1.0
    return round(acute_load / chronic_load, 2)

def simplified_fatigue_coefficient(days_interval, consecutive_matches, travel_km):
    coeff = 1.0
    if days_interval < 3:
        coeff *= 1.15
    if consecutive_matches > 3:
        coeff *= 1.10
    if travel_km > 500:
        coeff *= 1.08
    return round(coeff, 2)

if __name__ == "__main__":
    print(calculate_acwr(120, 100))
    print(simplified_fatigue_coefficient(2, 4, 600))

