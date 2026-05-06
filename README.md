# sports-quant-research
Python tools sports odds analysis
# Sports Quantitative Research
A collection of Python tools for sports odds analysis, rating modeling, and data validation.

## 📂 Project Structure
- `payout_check.py`: Odds-Probability-Payout closed-loop consistency check
- `kelly_static_filter.py`: Fixed-position Kelly filter for stable risk-control signals
- `betfair_rating_reverse.py`: Betfair odds to implied team rating & strength difference
- `acwr_fatigue_model.py`: ACWR workload ratio + simplified fatigue coefficient
- `poisson_5in1_model.py`: Poisson-based match outcome probability calculator
- `data_source_audit.py`: Structural defect detection for OKOOO and other odds data

## 🚀 Core Methodologies
1.  **Odds Consistency Validation**: Detect stitched, unsynchronized, or intercepted data
2.  **Kelly Static Analysis**: Identify bookmaker's stable pricing signals
3.  **Implied Rating Reverse-Engineering**: Derive fundamental strength from raw exchange odds
4.  **Fatigue & Workload Modeling**: Estimate match fitness using schedule and travel data
5.  **Poisson Outcome Forecasting**: Simulate goal distributions to calculate win/draw/loss probabilities

## 📧 Contact
Email: dataanalyst@example.com
---
## Update Notice
Project ongoing & continuously updated.
More sports rating conversion、fatigue correction and market reverse modules will be added subsequently.


# Football Quantitative Odds Analysis Model
A 5-layer, locally runnable Python model for football odds analysis, built on 8 years of hands-on experience in sports data analysis.

## Project Overview
This model reconstructs the full logic of bookmaker pricing and market structure analysis, with a focus on noise filtering and reliable signal extraction.

### 5-Layer Architecture
1. **True Team Strength (TrueTS)**  
   Calculates precise generalized strength based on league tier, squad strength, home advantage, form, fatigue, and head-to-head bias.
2. **Probability Mapping**  
   Converts strength difference into win/draw/loss probabilities without bookmaker margin.
3. **Theoretical Fair Odds**  
   Applies structured margin to generate "true" opening odds, simulating bookmaker pricing logic.
4. **Market Structure & Kelly Criterion**  
   Compares theoretical vs. real odds to identify protection and trap signals.
5. **Final Decision Engine**  
   Integrates all layers to output actionable betting recommendations.

## Features
- Fully local, no external dependencies or API calls
- Built-in noise filtering to eliminate unreliable signals
- Transparent and reproducible logic, with every parameter documented

## Quick Start
```bash
python example_usage.py
