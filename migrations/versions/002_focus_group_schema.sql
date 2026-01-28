-- ============================================
-- FOCUS GROUPS MASTER TABLE
-- ============================================
CREATE TABLE focus_groups (
    focus_group_id VARCHAR(50) PRIMARY KEY,
    platform VARCHAR(20) NOT NULL CHECK (platform IN ('pe_org_air', 'individual_air')),
    group_name VARCHAR(100) NOT NULL,
    group_code VARCHAR(30) NOT NULL,
    group_description TEXT,
    display_order INTEGER NOT NULL,
    icon_name VARCHAR(50),
    color_hex VARCHAR(7),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (platform, group_code)
);

-- ============================================
-- DIMENSIONS TABLE (PE Org-AI-R: 7 Dimensions)
-- ============================================
CREATE TABLE dimensions (
    dimension_id VARCHAR(50) PRIMARY KEY,
    platform VARCHAR(20) NOT NULL,
    dimension_name VARCHAR(100) NOT NULL,
    dimension_code VARCHAR(50) NOT NULL,
    description TEXT,
    min_score DECIMAL(5,2) DEFAULT 0,
    max_score DECIMAL(5,2) DEFAULT 100,
    display_order INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (platform, dimension_code)
);

-- ============================================
-- FOCUS GROUP DIMENSION WEIGHTS
-- ============================================
CREATE TABLE focus_group_dimension_weights (
    weight_id SERIAL PRIMARY KEY,
    focus_group_id VARCHAR(50) NOT NULL REFERENCES focus_groups(focus_group_id),
    dimension_id VARCHAR(50) NOT NULL REFERENCES dimensions(dimension_id),
    weight DECIMAL(4,3) NOT NULL CHECK (weight >= 0 AND weight <= 1),
    weight_rationale TEXT,
    effective_from DATE NOT NULL DEFAULT CURRENT_DATE,
    effective_to DATE,
    is_current BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (focus_group_id, dimension_id, effective_from)
);

CREATE INDEX idx_weights_current ON focus_group_dimension_weights(focus_group_id, is_current)
    WHERE is_current = TRUE;

-- ============================================
-- FOCUS GROUP CALIBRATIONS
-- ============================================
CREATE TABLE focus_group_calibrations (
    calibration_id SERIAL PRIMARY KEY,
    focus_group_id VARCHAR(50) NOT NULL REFERENCES focus_groups(focus_group_id),
    parameter_name VARCHAR(100) NOT NULL,
    parameter_value DECIMAL(10,4) NOT NULL,
    parameter_type VARCHAR(20) DEFAULT 'numeric',
    description TEXT,
    effective_from DATE NOT NULL DEFAULT CURRENT_DATE,
    effective_to DATE,
    is_current BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (focus_group_id, parameter_name, effective_from)
);