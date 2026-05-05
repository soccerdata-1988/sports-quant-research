import math

def poisson_probability(lmbda, k):
    return (math.pow(lmbda, k) * math.exp(-lmbda)) / math.factorial(k)

def match_outcome_probabilities(home_lmbda, away_lmbda, max_goals=5):
    home_win, draw, away_win = 0.0, 0.0, 0.0
    for h in range(max_goals+1):
        for a in range(max_goals+1):
            prob = poisson_probability(home_lmbda, h) * poisson_probability(away_lmbda, a)
            if h > a:
                home_win += prob
            elif h == a:
                draw += prob
            else:
                away_win += prob
    return round(home_win, 4), round(draw, 4), round(away_win, 4)

if __name__ == "__main__":
    print(match_outcome_probabilities(1.6, 1.1))
