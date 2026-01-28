-- ============================================
-- SEED SECTOR CALIBRATION PARAMETERS
-- ============================================

INSERT INTO focus_group_calibrations
(focus_group_id, parameter_name, parameter_value, description)
VALUES

-- Manufacturing
('pe_manufacturing', 'h_r_baseline', 70, 'Baseline human readiness score'),
('pe_manufacturing', 'ebitda_multiplier', 1.1, 'Lower EBITDA sensitivity'),
('pe_manufacturing', 'position_factor_delta', 0.12, 'Lower org agility'),
('pe_manufacturing', 'talent_concentration_threshold', 0.30, 'Talent spread wider'),

-- Technology
('pe_technology', 'h_r_baseline', 80, 'Higher baseline readiness'),
('pe_technology', 'ebitda_multiplier', 1.4, 'Higher EBITDA leverage'),
('pe_technology', 'position_factor_delta', 0.18, 'Faster org movement'),
('pe_technology', 'talent_concentration_threshold', 0.20, 'Talent is concentrated');