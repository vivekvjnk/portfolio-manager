# Resources & Research Repository (`resources/`)

This directory serves as the workspace repository for detailed market observations, technical analysis deep-dives, sector research, and backtest results.

## Directory Structure
Organized by date or topic folder:
```text
resources/
├── YYYY-MM-DD/
│   ├── market_regime_analysis.md
│   ├── stock_deep_dive_<symbol>.md
│   └── sector_rotation_review.md
└── strategy_notes/
    └── pullback_continuation_patterns.md
```

## Knowledge Distillation Lifecycle
1. **Draft & Observe**: Record raw observations, price charts, indicator tweaks, or stock research in `resources/`.
2. **Validate & Test**: Test the observation over multiple trading sessions or market conditions.
3. **Graduate to ECP**: Once an observation or procedure is stable, reliable, and verified, distill it into the appropriate ECP in `.agents/skills/`:
   - Operational workflow / decision rules → `.agents/skills/<package>/SKILL.md`
   - Data specs / rubrics → `.agents/skills/<package>/references/`
   - Calculation scripts → `.agents/skills/<package>/tools/`
