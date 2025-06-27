# scripts/csv_filtering.py

def filter_company_profile(company_df):
    # Select columns that are relevant for assessing R&D maturity
    columns_of_interest = [
        'Company ID', 'Companies', 'Revenue', 'Business Status', 'Revenue Growth %', 
        'Last Financing Size', 'Website', 'LinkedIn URL',
        'Last Financing Valuation', 'Total Patent Documents', 'Active Patent Documents',
        'Acquirers', 'Active Investors', 'Total Clinical Trials', 'Year Founded'
    ]

    company_df_filtered = company_df[columns_of_interest]

    # Check for any missing values and handle them appropriately 
    company_df_filtered = company_df_filtered.dropna(subset=['Company ID'])  # Drop rows without company info

    # Clean known non-numeric values like 'upgrade'
    for col in ['Revenue', 'Revenue Growth %', 'Last Financing Size', 
                'Last Financing Valuation', 'Total Patent Documents', 
                'Active Patent Documents', 'Active Investors', 
                'Total Clinical Trials', 'Year Founded']:
        if col in company_df_filtered.columns:
            company_df_filtered = company_df_filtered[~company_df_filtered[col].astype(str).str.lower()\
                                                      .str.contains('upgrade', na=False)]
    
    return company_df_filtered

def filter_deals(deals_df):
    # Select the columns that will be used for maturity assessment
    columns_of_interest = [
        'Company ID', 'Deal Type', 'Deal Size', 'Investors', '# Investors',
        'Lead/Sole Investors', 'Deal No.', 'Deal Synopsis'
    ]

    deals_df_filtered = deals_df[columns_of_interest]

    # Drop rows without company info
    deals_df_filtered = deals_df_filtered.dropna(subset=['Company ID'])

    return deals_df_filtered

def filter_investors(investors_df):
    # Select colunns that will be used to assess prominance of the Investor
    columns_of_interest = [
        'Investor ID', 'Investors', 'Investor Legal Name', 'Description', 'Primary Investor Type',
        '# of Investment Professionals', 'Year Founded', 'Website', 'AUM', 'Total Investments', 
        'Total Exits'
    ]
    investors_df_filtered = investors_df[columns_of_interest]

    #Drop rows without Investor info
    investors_df_filtered = investors_df_filtered.dropna(subset=['Investors'])

    return investors_df_filtered
