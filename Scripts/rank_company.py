# Scripts/rank_company.py

def status_rank(companies_df):
    """
    Ranks companies based on their Business Status. This new version uses a more
    granular map to handle the detailed statuses found in the cleaned dataset.
    """
    status_map = {
        # Tier 1: Commercial Success (Highest Signal)
        'Profitable': 10,
        'Generating Revenue/Not Profitable': 9,
        'Generating Revenue': 8,

        # Tier 2: Late-Stage Validation (Strong Signal)
        'Clinical Trials - Phase 2': 7,
        'Product In Beta Test': 7,

        # Tier 3: Mid-Stage R&D (Moderate Signal)
        'Clinical Trials - Phase 1': 5,
        'Clinical Trials - General': 5,
        'Product Development': 4,

        # Tier 4: Early Stage (Low Signal)
        'Startup': 3,
        'Stealth': 2,
        'Restart': 2,

        # Tier 5: Negative / Stalled (Very Low Signal)
        'Bankruptcy: Admin/Reorg': 1,
        
        # Tier 6: Failure or No Signal
        'Unknown': 0,
        'Out of Business': 0,
        'Bankruptcy: Liquidation': 0
    }
    
    companies_df['Business Status Rank'] = companies_df['Business Status'].map(status_map).fillna(0)

def age_score(companies_df):
    """
    Calculates the company's age at acquisition and assigns a score.
    The score rewards companies in a "prime" age range (5-12 years),
    as being too young or too old can be negative signals.
    """
    acquisition_year = 2025
    companies_df['Age'] = acquisition_year - companies_df['Year Founded']

    def assign_score(age):
        if 5 <= age <= 12:
            return 10 # Prime maturity window
        elif 2 < age < 5:
            return 6  # Still developing
        elif age > 12:
            return 4  # Potentially stagnated
        else: # 0-2 years
            return 2  # Very early stage
            
    companies_df['Age Score'] = companies_df['Age'].apply(assign_score)

def quartile_ranking(companies_df):
    import pandas as pd
    """
    Applies quartile ranking (1-10 deciles) to key numerical columns to normalize them.
    This prevents outliers from dominating the score.
    """
    cols_to_rank = [
        'Revenue',
        'Revenue Growth %',
        'Last Financing Size',
        'Last Financing Valuation',
        'Total Patent Documents',
        'Active Patent Documents',
        'Total Clinical Trials'
    ]

    for col in cols_to_rank:
        # Create a mask to handle rows with 0, which won't be ranked
        valid_mask = companies_df[col] > 0
        
        if valid_mask.sum() > 0:
            # Use qcut for decile ranking (1-10)
            # Use drop_duplicates to handle skewed data
            bins = pd.qcut(companies_df.loc[valid_mask, col], q=10, duplicates='drop')
            num_bins = bins.cat.categories.size

            labels = list(range(1, num_bins + 1))
            
            companies_df.loc[valid_mask, f'{col} QRank'] = pd.qcut(
                companies_df.loc[valid_mask, col],
                q=10,
                labels=labels,
                duplicates='drop'
            ).astype(int)

        # Fill non-valid (0 or NaN) rows with a score of 0
        companies_df[f'{col} QRank'] = companies_df[f'{col} QRank'].fillna(0)


def weighted_company_score(companies_df):
    from sklearn.preprocessing import MinMaxScaler
    """
    Calculates the final weighted score based on all engineered features.
    The weights are chosen based on the presumed strength of each signal.
    """
    # Define the weights for each component of the score
    weights = {
        'Business Status Rank': 3.5,
        'Revenue QRank': 3.0,
        'Total Clinical Trials QRank': 3.0, # Very strong signal for life sciences
        'Last Financing Valuation QRank': 2.5,
        'Last Financing Size QRank': 2.0,
        'Revenue Growth % QRank': 1.5,
        'Total Patent Documents QRank': 1.5,
        'Age Score': 1.0,
        'Active Patent Documents QRank': 0.5
    }
    
    # Initialize score column
    companies_df['Weighted Company Score'] = 0
    
    # Calculate the weighted sum
    for col, weight in weights.items():
        companies_df['Weighted Company Score'] += companies_df[col] * weight

    # Normalize the final score to a 0-100 scale for easy interpretation
    scaler = MinMaxScaler(feature_range=(0, 100))
    companies_df['Company Score'] = scaler.fit_transform(
        companies_df[['Weighted Company Score']]
    )