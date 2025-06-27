# Scripts/csv_preprocessing.py

def preprocess_company_profile(company_df_filtered):
    # Fill or drop missing values as needed

    # 1. Fill Revenue with 0 
    company_df_filtered['Revenue'] = company_df_filtered['Revenue'].fillna(0).astype(float)

    # 2. Fill Revenue Growth % with 0
    company_df_filtered['Revenue Growth %'] = company_df_filtered['Revenue Growth %'].fillna(0).astype(float)

    # 3. Fill missing Business Status with 'Unknown'
    company_df_filtered['Business Status'] = company_df_filtered['Business Status'].fillna('Unknown')

    # 4. Fill missing Active Investors with 'Unknown'
    company_df_filtered['Active Investors'] = company_df_filtered['Active Investors'].fillna('Unknown')

    # 5. Fill Last Financing Size with 0
    company_df_filtered['Last Financing Size'] = company_df_filtered['Last Financing Size'].fillna(0).astype(float)

    # 6. Fill Last Financing Valuation with 0
    company_df_filtered['Last Financing Valuation'] = company_df_filtered['Last Financing Valuation'].fillna(0).astype(float)

    # 7. Fill Website with 'Unknown'
    company_df_filtered['Website'] = company_df_filtered['Website'].fillna('Unknown')

    # 8. Fill LinkedIn URL with 'Unknown'
    company_df_filtered['LinkedIn URL'] = company_df_filtered['LinkedIn URL'].fillna('Unknown')

    # 9. Fill Acquirers with 'Unknown'
    company_df_filtered['Acquirers'] = company_df_filtered['Acquirers'].fillna('Unknown')

    # 10. Fill Total Clinical Trials with 0
    company_df_filtered['Total Clinical Trials'] = company_df_filtered['Total Clinical Trials'].fillna(0).astype(float)

    # 11. Fill Year Founded with 0
    company_df_filtered['Year Founded'] = company_df_filtered['Year Founded'].fillna(0).astype(float)

    # 12. Fill Total Patent Documents with 0
    company_df_filtered['Total Patent Documents'] = company_df_filtered['Total Patent Documents'].fillna(0).astype(float)

    # 13. Fill Active Patent Documents
    company_df_filtered['Active Patent Documents'] = company_df_filtered['Active Patent Documents'].fillna(0).astype(float)

    return company_df_filtered

def preproces_deals(deals_df_filtered):

    # 1. Fill Deal Size with 0
    deals_df_filtered['Deal Size'] = deals_df_filtered['Deal Size'].fillna(0)

    # Fill Investors with 'Unknown'
    deals_df_filtered['Investors'] = deals_df_filtered['Investors'].fillna('Unknown')

    # Fill # Investors with 0
    deals_df_filtered['# Investors'] = deals_df_filtered['# Investors'].fillna(0)

    # Fill Lead/Sole Investors with 'None'
    deals_df_filtered['Lead/Sole Investors'] = deals_df_filtered['Lead/Sole Investors'].fillna('None')

    # Fill Deal Synopsis with 'Unknown'
    deals_df_filtered['Deal Synopsis'] = deals_df_filtered['Deal Synopsis'].fillna('Unknown')

    for index, deal in deals_df_filtered.iterrows():
        if deal['# Investors'] > 1 and deal['Investors'] != 'Unknown':
            deals_df_filtered.at[index, 'Investors'] = deal['Investors'].split(',')
        else:
            deals_df_filtered.at[index, 'Investors'] = [deal['Investors']]


    return deals_df_filtered

def preprocess_investors(investors_df_filtered):
    # 1. Fill Investor Legal Name with 'Unknown'
    investors_df_filtered['Investor Legal Name'] = investors_df_filtered['Investor Legal Name'].fillna('Unknown')

    # 2. Fill Description with 'None'
    investors_df_filtered['Description'] = investors_df_filtered['Description'].fillna('None')

    # 3. Fill # of Investment Professionals with 0
    investors_df_filtered['# of Investment Professionals'] = investors_df_filtered['# of Investment Professionals'] \
                                                                                .fillna(0)
    
    # 4. Fill Year Founded with 2026 - leads age column to be negative 
    investors_df_filtered['Year Founded'] = investors_df_filtered['Year Founded'].fillna(2026)

    # 5. Fill Website with 'Unknown'
    investors_df_filtered['Website'] = investors_df_filtered['Website'].fillna('Unknown')

    # 6. Fill AUM with 0
    investors_df_filtered['AUM'] = investors_df_filtered['AUM'].fillna(0)

    # 7. Fill Total Investments with 0
    investors_df_filtered['Total Investments'] = investors_df_filtered['Total Investments'].fillna(0)

    # 8. Fill Total Exits with 0 
    investors_df_filtered['Total Exits'] = investors_df_filtered['Total Exits'].fillna(0)

    # Add 'Age' column
    investors_df_filtered['Age'] = 2025 - investors_df_filtered['Year Founded']

    # Clean Investors column
    investors_df_filtered['Investors'] = investors_df_filtered['Investors']\
                            .apply(lambda x: x.split("(")[0] if isinstance(x, str) else x)

    return investors_df_filtered