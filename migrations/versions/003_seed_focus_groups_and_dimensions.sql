-- ================================
-- DIMENSIONS (7)
-- ================================
INSERT INTO dimensions
(dimension_id, platform, dimension_name, dimension_code, description, display_order)
VALUES
('dim_data_infra', 'pe_org_air', 'Data Infrastructure', 'DATA_INFRA', 'Core data platforms and pipelines', 1),
('dim_ai_gov', 'pe_org_air', 'AI Governance', 'AI_GOV', 'Model governance, risk, controls', 2),
('dim_tech_stack', 'pe_org_air', 'Technology Stack', 'TECH_STACK', 'Core enterprise tech stack', 3),
('dim_talent', 'pe_org_air', 'Talent', 'TALENT', 'AI and data talent maturity', 4),
('dim_leadership', 'pe_org_air', 'Leadership', 'LEADERSHIP', 'Executive sponsorship and strategy', 5),
('dim_use_cases', 'pe_org_air', 'Use Cases', 'USE_CASES', 'Production AI use cases', 6),
('dim_culture', 'pe_org_air', 'Culture', 'CULTURE', 'Data-driven culture', 7);

-- ================================
-- FOCUS GROUPS (7 PE sectors)
-- IDs must start with pe_
-- ================================
INSERT INTO focus_groups
(focus_group_id, platform, group_name, group_code, group_description, display_order)
VALUES
('pe_manufacturing', 'pe_org_air', 'Manufacturing', 'MANUFACTURING', 'Industrial & manufacturing firms', 1),
('pe_financial_services', 'pe_org_air', 'Financial Services', 'FINANCIAL_SERVICES', 'Banks, insurers, asset managers', 2),
('pe_healthcare', 'pe_org_air', 'Healthcare', 'HEALTHCARE', 'Providers, pharma, life sciences', 3),
('pe_technology', 'pe_org_air', 'Technology', 'TECHNOLOGY', 'Software & platform companies', 4),
('pe_retail', 'pe_org_air', 'Retail', 'RETAIL', 'Consumer & retail businesses', 5),
('pe_energy', 'pe_org_air', 'Energy', 'ENERGY', 'Energy & utilities', 6),
('pe_professional_services', 'pe_org_air', 'Professional Services', 'PROFESSIONAL_SERVICES', 'Consulting & services firms', 7);