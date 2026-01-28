CREATE TABLE organizations (
    organization_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    -- Identity
    legal_name VARCHAR(255) NOT NULL,
    display_name VARCHAR(255),
    ticker_symbol VARCHAR(10),
    cik_number VARCHAR(20),
    duns_number VARCHAR(20),

    -- Sector Assignment
    focus_group_id VARCHAR(50) NOT NULL REFERENCES focus_groups(focus_group_id),

    -- Industry Classification
    primary_sic_code VARCHAR(10),
    primary_naics_code VARCHAR(10),

    -- Firmographics
    employee_count INTEGER,
    annual_revenue_usd DECIMAL(15,2),
    founding_year INTEGER,
    headquarters_country VARCHAR(3),
    headquarters_state VARCHAR(50),
    headquarters_city VARCHAR(100),
    website_url VARCHAR(500),

    -- Status
    status VARCHAR(20) DEFAULT 'active' CHECK (status IN ('active', 'inactive', 'archived')),

    -- Metadata
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by VARCHAR(100),

    CONSTRAINT chk_org_pe_platform CHECK (focus_group_id LIKE 'pe_%')
);

CREATE INDEX idx_org_focus_group ON organizations(focus_group_id);
CREATE INDEX idx_org_ticker ON organizations(ticker_symbol) WHERE ticker_symbol IS NOT NULL;