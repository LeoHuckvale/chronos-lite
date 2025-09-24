# chronos-lite 🔋🪶

Being a simple model of a battery energy storage system, participating in half-hourly and hourly wholesale markets.


## TODO

- [ ] Project plan 👇
- [ ] MVP
    - [ ] Development framework
        - [ ] taskipy
        - [ ] jupyter
    - [ ] QA framework
        - [ ] Git pre-commit hook
        - [ ] Unit tests
        - [ ] Syntax
        - [ ] Types
        - [ ] Code quality
    - [ ] Data model
        - [ ] Market
        - [ ] Battery
    - [ ] Feature development
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
        - [ ] Output financial summary
            - [ ] Operational costs
            - [ ] Import costs
            - [ ] Export revenue
            - [ ] Capex
            - [ ] Net profit over data period
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
