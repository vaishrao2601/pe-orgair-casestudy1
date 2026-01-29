## Case Study 1 – Foundation Validation

### Database
- PostgreSQL running via Docker
- Tables created successfully
- Seed data validated

### Counts
- focus_groups: 7
- dimensions: 7

### Status
✔ Platform foundation validated

This repository represents Case Study 1 for the PE OrgAIR platform.

### Phase 0 – Foundation (Completed)
- Project initialized from Labs 1 & 2
- Dockerized PostgreSQL database
- Schema migrations and seed data
- Environment configuration validation
- Database connectivity verified

### Phase 1 – Configuration & Sector Modeling (In Progress)
- Sector configuration service
The sector configuration API guarantees:
    - sector_id
    - sector_name
    - sector_code
    - dimension_weights (normalized, sum = 1.0)
    - calibration parameters (typed decimals)
    - Cache behavior validated (DB hit → cache hit → invalidation reload)


- Dimension weights and calibrations
- Cache-backed configuration retrieval

### Phase 2 – Scoring & Evaluation (Planned)
- OrgAIR scoring logic
- Dimension aggregation
- Validation and constraints

### Phase 3 – API & Observability (Planned)
- REST endpoints
- Logging and metrics
- Performance validation


