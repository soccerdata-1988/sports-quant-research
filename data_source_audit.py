def check_okooo_data(odds, kelly):
    inv_odds = [1/o for o in odds]
    inv_kelly = [1/k for k in kelly]
    odds_sum = sum(inv_odds)
    kelly_sum = sum(inv_kelly)
    return {
        "odds_payout": round(odds_sum, 4),
        "kelly_payout": round(kelly_sum, 4),
        "is_synchronized": abs(odds_sum - kelly_sum) < 0.05
    }

def check_500w_data(odds_list):
    unique_payouts = set()
    for odds in odds_list:
        payout = sum(1/o for o in odds)
        unique_payouts.add(round(payout, 4))
    return {
        "payout_values": list(unique_payouts),
        "has_consistent_payout": len(unique_payouts) == 1
    }

if __name__ == "__main__":
    print(check_okooo_data([1.80, 3.50, 4.20], [0.95, 0.93, 1.05]))

