# Scripts/rank_investors.py

def type_rank(investors_df):
    investor_type_rank = {
        # Tier 1: Highest Maturity
        'PE/Buyout': 10,
        'Special Purpose Acquisition Company (SPAC)': 10,
        'Growth/Expansion': 9,
        'Asset Manager': 9,
        'Mutual Fund': 9,
        
        # Tier 2: Strong Maturity
        'Corporate Venture Capital': 8,
        'Sovereign Wealth Fund': 8,
        'Corporation': 7,
        'Secondary Buyer': 7,
        'Investment Bank': 7, # Added from analysis
        
        # Tier 3: Moderate/Mixed
        'Venture Capital': 6,
        'Hedge Fund': 6,
        'Lender/Debt Provider': 5,
        'Family Office': 5,
        'Mezzanine': 5,
        
        # Tier 4: Early Stage
        'Angel Group': 4,
        'Accelerator/Incubator': 3,
        'Angel (individual)': 2,
        
        # Tier 5: Earliest Stage
        'University': 1,
        'Government': 1,
        
        # Tier 6: Neutral/No Signal
        'Limited Partner': 0,
        'Fund of Funds': 0,
        'Other': 0,
        'Other Private Equity': 0,
        'Holding Company': 0,
        'Merchant Banking Firm': 0,
        'Real Estate': 0,
        'Infrastructure': 0,
        'Impact Investing': 0,
        'Not-For-Profit Venture Capital': 0,
        'PE-Backed Company': 0,
        'VC-Backed Company': 0
    }

    investors_df['Investor Type Rank'] = investors_df['Primary Investor Type'].map(investor_type_rank).fillna(0)

def exit_multiple(investors_df):
    # Create mask for companies with known Total Exits and Total Investments
    valid_mask = (investors_df['Total Exits'] > 0) & (investors_df['Total Investments'] > 0)

    # Apply Exit Multiple to companies that meet the valid mask requirements
    investors_df.loc[valid_mask, 'Exit Multiple'] = (
        investors_df.loc[valid_mask, 'Total Exits'] / investors_df.loc[valid_mask, 'Total Investments'])

    # Set invalid mask companies to 0
    investors_df.loc[~valid_mask, 'Exit Multiple'] = 0

def investor_age_score(investors_df):
    """
    Creates a score for an investor's age based on buckets.
    For investors, older is generally better as it signals experience and stability,
    but with diminishing returns at the top end.
    """
    # Using the current year, 2025
    current_year = 2025
    investors_df['Age'] = current_year - investors_df['Year Founded']

    def assign_score(age):
        if age > 15:
            return 10  # Very established, legendary status
        elif 8 <= age <= 15:
            return 8   # Highly experienced, multiple successful fund cycles
        elif 3 <= age < 8:
            return 5   # Established, likely on 2nd or 3rd fund
        else: # 0-2 years
            return 2   # New and relatively unproven
            
    investors_df['Investor Age Score'] = investors_df['Age'].apply(assign_score).fillna(0)


def quartile_ranking(investors_df):
    import pandas as pd

    # Perform Quartile Ranking on the following columns
    cols = [
        "# of Investment Professionals",
        "AUM",
        "Total Investments",
        "Total Exits"
    ]

    """Create a mask for each column on values of 0, since in the orginal dataset,
     the are no values of 0, instead there are only missing values. I cannot be certain that they actually represent
      values of 0, so instead I treat them seperately """
    mask_per_column = {col: investors_df[col] != 0 for col in cols}


    for col, mask in mask_per_column.items():
        # Run qcut without labels to get bin count
        bins = pd.qcut(
            investors_df.loc[mask, col],
            q=10,
            duplicates='drop'
        )

        num_bins = bins.cat.categories.size  # Actual number of bins created

        # Now apply qcut again with matching labels
        investors_df.loc[mask, f'{col} QRank'] = pd.qcut(
            investors_df.loc[mask, col],
            q=10,
            labels=list(range(1, num_bins + 1)),
            duplicates='drop'
        ).astype(int)

        # Assign 0 to zero/missing rows
        investors_df.loc[~mask, f'{col} QRank'] = 0


def weighted_rank(investors_df):
    from sklearn.preprocessing import MinMaxScaler
    investors_df['Weighted Investor Score'] = (
        investors_df['Exit Multiple'] * 3.5 +
        investors_df['Investor Type Rank'] * 2.5 +
        investors_df['Total Exits QRank'] * 1.5 +
        investors_df['Investor Age Score'] * 1.0 + 
        investors_df['Total Investments QRank'] * 1.0 +
        investors_df['# of Investment Professionals QRank'] * 0.5 +
        investors_df['AUM QRank'] * 0.5
    )


    # Instantiate the scaler to map scores to a 0-100 range
    scaler = MinMaxScaler(feature_range=(0, 100))
    
    # Apply the scaler to the raw weighted score
    # The input to fit_transform must be 2D, hence the double brackets
    investors_df['Investor Score Final'] = scaler.fit_transform(
        investors_df[['Weighted Investor Score']]
    )