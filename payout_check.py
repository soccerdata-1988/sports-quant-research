def payout_consistency_check(home_odds, draw_odds, away_odds):
    inv_h = 1.0 / home_odds
    inv_d = 1.0 / draw_odds
    inv_a = 1.0 / away_odds
    total_inv = inv_h + inv_d + inv_a
    payout_rate = total_inv
    prob_h = inv_h / total_inv
    prob_d = inv_d / total_inv
    prob_a = inv_a / total_inv
    is_consistent = abs(prob_h + prob_d + prob_a - 1.0) < 1e-6

    return {
        "payout_rate": round(payout_rate, 4),
        "normalized_prob": [round(prob_h, 4), round(prob_d, 4), round(prob_a, 4)],
        "is_consistent": is_consistent
    }

if __name__ == "__main__":
    print(payout_consistency_check(1.80, 3.50, 4.20))

