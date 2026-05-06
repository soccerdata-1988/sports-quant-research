import math

# ==================================================
# 第一层：精密广义实力 TrueTS
# ==================================================
def true_team_strength(league_base: float,
                       squad_strength: float,
                       home_advantage: float,
                       form_rating: float,
                       fatigue: float,
                       h2h_bias: float) -> float:
    """
    计算球队精密广义实力 TrueTS
    权重：league_base 0.4, squad_strength 0.2, home_advantage 0.15, form_rating 0.15, fatigue 0.05, h2h_bias 0.05
    """
    ts = (league_base * 0.4) + \
         (squad_strength * 0.2) + \
         (home_advantage * 0.15) + \
         (form_rating * 0.15) + \
         (fatigue * 0.05) + \
         (h2h_bias * 0.05)
    return round(ts, 2)


# ==================================================
# 第二层：精密概率映射（TrueTS → 真实胜平负概率，无抽水）
# ==================================================
def true_probability(delta_ts: float) -> tuple[float, float, float]:
    """
    输入：主客队广义实力差 delta_ts = home_ts - away_ts
    输出：无抽水的真实主胜、平局、客胜概率
    """
    # 核心参数（训练固化）
    k = 0.45
    base_draw = 0.32
    draw_drop = -0.015

    # 1. 主胜客胜基础概率（逻辑斯蒂映射）
    p_home_raw = 1 / (1 + math.exp(-k * delta_ts))
    p_away_raw = 1 / (1 + math.exp(k * delta_ts))

    # 2. 平局概率：随实力差增大而线性下降
    p_draw = max(base_draw + draw_drop * abs(delta_ts), 0.18)

    # 3. 归一化，保证三者和为1
    total = p_home_raw + p_away_raw + p_draw
    p_home = p_home_raw / total
    p_draw = p_draw / total
    p_away = p_away_raw / total

    return round(p_home, 4), round(p_draw, 4), round(p_away, 4)


# ==================================================
# 第三层：机构理论欧赔（含抽水）
# ==================================================
def fair_odds_from_prob(prob: float, margin: float = 0.08) -> float:
    """
    根据无抽水概率和目标抽水，计算理论欧赔
    margin: 机构目标抽水（主胜≈7.5%，平局≈10%，客胜≈8.5%）
    """
    if prob <= 0:
        return 100.0
    return round(1 / (prob * (1 - margin)), 2)


def true_odds(p_home: float, p_draw: float, p_away: float) -> tuple[float, float, float]:
    """
    计算机构理论欧赔（含不同位置的抽水结构）
    """
    oh = fair_odds_from_prob(p_home, margin=0.075)
    od = fair_odds_from_prob(p_draw, margin=0.10)
    oa = fair_odds_from_prob(p_away, margin=0.085)
    return oh, od, oa


# ==================================================
# 第四层：庄家结构识别 + 凯利校验
# ==================================================
def implied_probability(odds: list[float]) -> list[float]:
    """从欧赔反推隐含概率（含抽水）"""
    return [1 / o for o in odds]


def kelly_value(our_prob: float, bookie_odds: float, kelly_factor: float = 0.10) -> float:
    """
    计算凯利值（标准：>0.12为保护，<0.08为诱盘）
    """
    if bookie_odds <= 1:
        return 0.0
    b = bookie_odds - 1
    q = 1 - our_prob
    kelly = (b * our_prob - q) / b
    return round(kelly * kelly_factor, 3)


def market_structure_analysis(our_p: tuple[float, float, float],
                             our_odds: tuple[float, float, float],
                             bookie_odds: tuple[float, float, float]) -> dict:
    """
    对比理论赔率与实际盘口，识别机构结构
    """
    ph, pd, pa = our_p
    oh, od, oa = our_odds
    bh, bd, ba = bookie_odds

    kelly_h = kelly_value(ph, bh)
    kelly_d = kelly_value(pd, bd)
    kelly_a = kelly_value(pa, ba)

    def get_signal(kv):
        if kv > 0.12:
            return "保护"
        elif kv < 0.08:
            return "诱盘"
        else:
            return "平衡"

    return {
        "kelly_home": kelly_h,
        "kelly_draw": kelly_d,
        "kelly_away": kelly_a,
        "signal_home": get_signal(kelly_h),
        "signal_draw": get_signal(kelly_d),
        "signal_away": get_signal(kelly_a)
    }


# ==================================================
# 第五层：综合决策引擎（最终闭环）
# ==================================================
def final_decision_engine(league_base_home: float,
                         squad_home: float,
                         home_adv_home: float,
                         form_home: float,
                         fatigue_home: float,
                         h2h_home: float,
                         league_base_away: float,
                         squad_away: float,
                         home_adv_away: float,
                         form_away: float,
                         fatigue_away: float,
                         h2h_away: float,
                         bookie_odds: tuple[float, float, float]) -> dict:
    """
    完整调用五层模型，输出最终决策
    """
    # 第一层：计算双方广义实力
    ts_home = true_team_strength(league_base_home, squad_home, home_adv_home, form_home, fatigue_home, h2h_home)
    ts_away = true_team_strength(league_base_away, squad_away, home_adv_away, form_away, fatigue_away, h2h_away)

    # 第二层：真实概率
    delta = ts_home - ts_away
    p_home, p_draw, p_away = true_probability(delta)

    # 第三层：理论赔率
    theo_home, theo_draw, theo_away = true_odds(p_home, p_draw, p_away)

    # 第四层：市场结构与凯利校验
    analysis = market_structure_analysis((p_home, p_draw, p_away),
                                        (theo_home, theo_draw, theo_away),
                                        bookie_odds)

    # 第五层：综合决策
    signals = [analysis["signal_home"], analysis["signal_draw"], analysis["signal_away"]]
    if "保护" in signals:
        main_bet = ["主胜", "平局", "客胜"][signals.index("保护")]
    elif "诱盘" in signals:
        # 避开诱盘方向，选择最平衡的
        k_values = [analysis["kelly_home"], analysis["kelly_draw"], analysis["kelly_away"]]
        idx = k_values.index(min(k_values))
        main_bet = ["主胜", "平局", "客胜"][idx]
    else:
        # 平衡盘，选理论概率最高的
        probs = [p_home, p_draw, p_away]
        idx = probs.index(max(probs))
        main_bet = ["主胜", "平局", "客胜"][idx]

    return {
        "true_ts_home": ts_home,
        "true_ts_away": ts_away,
        "delta_ts": delta,
        "true_prob": (p_home, p_draw, p_away),
        "theoretical_odds": (theo_home, theo_draw, theo_away),
        "market_analysis": analysis,
        "recommended_bet": main_bet
    }
