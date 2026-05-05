import math

def betfair_to_implied_rating(bf_home, bf_draw, bf_away, margin_coeff=1.0638):
    book_h = bf_home * margin_coeff
    book_d = bf_draw * margin_coeff
    book_a = bf_away * margin_coeff
    inv_h, inv_d, inv_a = 1/book_h, 1/book_d, 1/book_a
    total_inv = inv_h + inv_d + inv_a
    prob_h = inv_h / total_inv
    prob_d = inv_d / total_inv
    prob_a = inv_a / total_inv
    if prob_h <= 0 or prob_a <= 0:
        delta = 99.99 if prob_h > prob_a else -99.99
    else:
        delta = 25 * math.log10(prob_h / prob_a)
    base_h_prob = 1 / (1 + math.pow(10, -delta / 25))
    base_a_prob = 1 - base_h_prob - prob_d
    return (
        round(delta, 2),
        round(1/base_h_prob, 2),
        round(1/prob_d, 2),
        round(max(1/base_a_prob, 1.01), 2)
    )

if __name__ == "__main__":
    print(betfair_to_implied_rating(1.80, 3.50, 4.20))
