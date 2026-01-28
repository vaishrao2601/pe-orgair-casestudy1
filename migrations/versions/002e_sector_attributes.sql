-- Manufacturing Sector Attributes
CREATE TABLE org_attributes_manufacturing (
    organization_id UUID PRIMARY KEY REFERENCES organizations(organization_id),
    ot_systems VARCHAR(100)[],
    it_ot_integration VARCHAR(20),
    scada_vendor VARCHAR(100),
    mes_system VARCHAR(100),
    plant_count INTEGER,
    automation_level VARCHAR(20),
    iot_platforms VARCHAR(100)[],
    digital_twin_status VARCHAR(20),
    edge_computing BOOLEAN DEFAULT FALSE,
    supply_chain_visibility VARCHAR(20),
    demand_forecasting_ai BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Financial Services Sector Attributes
CREATE TABLE org_attributes_financial_services (
    organization_id UUID PRIMARY KEY REFERENCES organizations(organization_id),
    regulatory_bodies VARCHAR(50)[],
    charter_type VARCHAR(50),
    model_risk_framework VARCHAR(50),
    mrm_team_size INTEGER,
    model_inventory_count INTEGER,
    algo_trading BOOLEAN DEFAULT FALSE,
    fraud_detection_ai BOOLEAN DEFAULT FALSE,
    credit_ai BOOLEAN DEFAULT FALSE,
    aml_ai BOOLEAN DEFAULT FALSE,
    aum_billions DECIMAL(12,2),
    total_assets_billions DECIMAL(12,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Healthcare Sector Attributes
CREATE TABLE org_attributes_healthcare (
    organization_id UUID PRIMARY KEY REFERENCES organizations(organization_id),
    hipaa_certified BOOLEAN DEFAULT FALSE,
    hitrust_certified BOOLEAN DEFAULT FALSE,
    fda_clearances VARCHAR(100)[],
    fda_clearance_count INTEGER DEFAULT 0,
    ehr_system VARCHAR(100),
    ehr_integration_level VARCHAR(20),
    fhir_enabled BOOLEAN DEFAULT FALSE,
    clinical_ai_deployed BOOLEAN DEFAULT FALSE,
    imaging_ai BOOLEAN DEFAULT FALSE,
    org_type VARCHAR(50),
    bed_count INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Technology Sector Attributes
CREATE TABLE org_attributes_technology (
    organization_id UUID PRIMARY KEY REFERENCES organizations(organization_id),
    tech_category VARCHAR(50),
    primary_language VARCHAR(50),
    cloud_native BOOLEAN DEFAULT TRUE,
    github_org VARCHAR(100),
    github_stars_total INTEGER,
    open_source_projects INTEGER,
    ml_platform VARCHAR(100),
    llm_integration BOOLEAN DEFAULT FALSE,
    ai_product_features INTEGER,
    gpu_infrastructure BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Retail Sector Attributes
CREATE TABLE org_attributes_retail (
    organization_id UUID PRIMARY KEY REFERENCES organizations(organization_id),
    retail_type VARCHAR(50),
    store_count INTEGER,
    ecommerce_pct DECIMAL(5,2),
    cdp_vendor VARCHAR(100),
    loyalty_program BOOLEAN DEFAULT FALSE,
    loyalty_members INTEGER,
    personalization_ai BOOLEAN DEFAULT FALSE,
    recommendation_engine VARCHAR(100),
    demand_forecasting BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Energy Sector Attributes
CREATE TABLE org_attributes_energy (
    organization_id UUID PRIMARY KEY REFERENCES organizations(organization_id),
    energy_type VARCHAR(50),
    regulated BOOLEAN DEFAULT FALSE,
    scada_systems VARCHAR(100)[],
    ami_deployed BOOLEAN DEFAULT FALSE,
    smart_grid_pct DECIMAL(5,2),
    generation_capacity_mw DECIMAL(12,2),
    grid_optimization_ai BOOLEAN DEFAULT FALSE,
    predictive_maintenance BOOLEAN DEFAULT FALSE,
    renewable_pct DECIMAL(5,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Professional Services Sector Attributes
CREATE TABLE org_attributes_professional_services (
    organization_id UUID PRIMARY KEY REFERENCES organizations(organization_id),
    firm_type VARCHAR(50),
    partnership_model VARCHAR(50),
    partner_count INTEGER,
    professional_staff INTEGER,
    km_system VARCHAR(100),
    document_ai BOOLEAN DEFAULT FALSE,
    knowledge_graph BOOLEAN DEFAULT FALSE,
    client_ai_services BOOLEAN DEFAULT FALSE,
    internal_ai_tools BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);