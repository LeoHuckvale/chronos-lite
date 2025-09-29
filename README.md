# chronos-lite 🔋🪶

Being a simple model of a battery energy storage system, participating in half-hourly and hourly wholesale markets.

## Log

1. Implemented a simple model in Jupyter notebook, in order to familiarise myself with linopy.
    This model only considers the battery interacting with the 30min market, and not subject to degradation.

## Decisions

- ~~Use Gurobi solver, because it's an MIQP problem.~~ Actually it's not, I'd just mistakenly added the decision
    variables as factors in the objective.
- ~~Limit to max 50 timesteps, because Gurobi limits to 200 variables without a license.~~
- Allow rounding error on validation of (charge rate * discharge rate) <= 1e8.

## TODO

- [x] Project plan 👇
- [x] Algorithm prototyping
    - [x] Simple model, arbitrage with one market
    - [x] Arbitrage with two markets
- [ ] MVP
    - [x] Development framework
        - [x] taskipy
        - [x] jupyter
    - [ ] QA framework
        - [ ] Git pre-commit hook
        - [x] Unit tests
        - [x] Syntax
        - [x] Types
        - [x] Code quality
    - [ ] Architecture
        - [ ] Data model
            - [ ] Market
            - [ ] Battery
        - [ ] Optimisation model
        - [ ] Financial calculations
            - [ ] Operational costs
            - [ ] Import costs
            - [ ] Export revenue
            - [ ] Capex
            - [ ] Net profit over data period
        - [ ] Operational outputs, visualisations
        - [ ] Execution script
    - [ ] Feature validation
        - [ ] Battery can charge from a market
        - [ ] Battery can discharge to a market
        - [ ] Battery commits capacity to entire market time interval
        - [ ] Battery pays for charging
        - [ ] Battery is paid for discharging
            - For example, if the battery chose to commit 5 MW of discharging into Market 1 when the market price is
                50 £/MWh, it would be paid £125 (5 MW * 0.5h * 50 £/MWh).
        - [ ] Battery can export any amount of power up to its maximum discharge rate for any duration
        - [ ] Battery cannot discharge beyond stored energy
        - [ ] Battery can import any amount power up to maximum charge rate for any duration
        - [ ] Battery cannot charge beyond storage capacity
        - [ ] Battery cannot sell same unit of energy to both markets
        - [ ] Battery can divide power across both markets
            - For example, a battery with a 5 MW maximum discharge rate and 5 MWh of energy stored
                could commit 2 MW of discharge into Market 1 for two half-hour intervals, and 3 MW of
                discharge into Market 2 for its 1 hour interval, but it could not commit 5 MW to both markets at
                the same time, and could not discharge more than 5 MWh of energy over that interval
        - [ ] Battery cannot charge and discharge at the same time
- [ ] Extra credit
    - [ ] Documentation
        - [ ] Sphinx framework
        - [ ] Divio structure
        - [ ] Design decisions / rationale
    - [ ] Feature development
        - [ ] Track battery charge/discharge cycles
        - [ ] Model battery degradation over time
    - [ ] CI/CD
        - [ ] Choose GitHub/GitLab
        - [ ] Provision runner
        - [ ] Configure
- [ ] Nice-to-haves
    - [ ] Model markets as a separate model dimension
    - [ ] Use plotly instead of matplotlib
    - [x] Add .editorconfig
    - [ ] Add vertical ticks at 30/60 mins for charge/discharge plots
    - [x] Remove unnecessary dependency on linopy[solvers] (just need linopy and highspy)
    - [ ] Utilise full dataset and incorporate data cleaning
    - [ ] Add pandera/pydantic schemas/data models to validate data inputs
