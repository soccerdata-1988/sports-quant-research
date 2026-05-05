def kelly_fixed_filter(kelly_list, tolerance=0.01):
    if not kelly_list:
        return None
    avg = sum(kelly_list) / len(kelly_list)
    std_dev = (sum((k - avg)**2 for k in kelly_list) / len(kelly_list))**0.5
    return round(avg, 4) if std_dev < tolerance else None

def batch_kelly_analysis(home_k, draw_k, away_k, tolerance=0.01):
    return {
        "home": kelly_fixed_filter(home_k, tolerance),
        "draw": kelly_fixed_filter(draw_k, tolerance),
        "away": kelly_fixed_filter(away_k, tolerance)
    }

if __name__ == "__main__":
    print(batch_kelly_analysis([0.95,0.92,0.98], [0.93,0.93,0.93], [1.05,1.10,1.02]))

