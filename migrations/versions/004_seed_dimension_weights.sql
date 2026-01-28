-- ============================================
-- SEED DIMENSION WEIGHTS PER FOCUS GROUP
-- Weights must sum to 1.0 per focus group
-- ============================================

INSERT INTO focus_group_dimension_weights
(focus_group_id, dimension_id, weight, weight_rationale)
VALUES

-- Manufacturing
('pe_manufacturing', 'dim_ai_gov', 0.10, 'Governance less critical in OT-heavy environments'),
('pe_manufacturing', 'dim_tech_stack', 0.25, 'Strong dependence on industrial tech stack'),
('pe_manufacturing', 'dim_talent', 0.20, 'Engineering talent is key'),
('pe_manufacturing', 'dim_leadership', 0.15, 'Leadership alignment matters'),
('pe_manufacturing', 'dim_use_cases', 0.20, 'AI use cases drive ROI'),
('pe_manufacturing', 'dim_culture', 0.10, 'Culture evolves slower'),

-- Technology
('pe_technology', 'dim_ai_gov', 0.15, 'AI governance critical'),
('pe_technology', 'dim_tech_stack', 0.30, 'Core value driver'),
('pe_technology', 'dim_talent', 0.20, 'Talent density matters'),
('pe_technology', 'dim_leadership', 0.10, 'Founder leadership'),
('pe_technology', 'dim_use_cases', 0.15, 'Product AI usage'),
('pe_technology', 'dim_culture', 0.10, 'Innovation culture');