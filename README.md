# chronos-lite 🔋🪶

Being a simple model of a battery energy storage system, participating in half-hourly and hourly wholesale markets.

## Instructions

Clone the project:

```
git clone git@github.com:LeoHuckvale/chronos-lite.git
cd chronos-lite
```

Run the example notebook and follow instructions therein:

```
uv run jupyter notebook example.ipynb
```

## Development tasks

Run the QA framework (tests + linting + typechecks)

```
uv run task qa
```

## Approach

1. Implemented a prototype in Jupyter notebook `00-prototype-linopy.ipynb`, in order to familiarise myself with linopy,
    as well as to experiment with and understand the mathematics of the model.
    a. This model initially only considered the battery interacting with the 30min market, not subject to degradation.
    b. Later I extended this to cover both 30 and 60min markets, with additional constraints.
2. Set up a package structure, organising data loading and model construction into separate modules.
3. Re-implemented prototype code into module structure with tests.

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
    - [x] Bugs
        - [x] Fix battery efficiency/losses
    - [x] Features
        - [x] Data model
            - [x] Market
            - [x] Battery
        - [x] Optimisation model
        - [x] Financial calculations
            - [x] Operational costs
            - [x] Import costs
            - [x] Export revenue
            - [x] Capex
            - [x] Net profit over data period
        - [x] Operational outputs, visualisations
        - [x] Execution script/notebook
    - [ ] Feature validation
        - [x] Battery can charge from a market
        - [x] Battery can discharge to a market
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
- [ ] Technical debt
  - [ ] Ensure that hourly data still aligns correctly if half-hourly data starts at a second half-hour, e.g. 00:30
- [ ] Nice-to-haves
    - [ ] Model markets as a separate model dimension
    - [ ] Use plotly instead of matplotlib
    - [x] Add .editorconfig
    - [ ] Add vertical ticks at 30/60 mins for charge/discharge plots
    - [x] Remove unnecessary dependency on linopy[solvers] (just need linopy and highspy)
    - [ ] Utilise full dataset and incorporate data cleaning
    - [ ] Add pandera/pydantic schemas/data models to validate data inputs
    - [ ] Add bad input data examples to test validation
    - [ ] Refine error codes on Ruff: include doc checks
