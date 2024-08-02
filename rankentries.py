import pandas as pd

def rank_criteria(row):
    if row['N. Attributed $ARR'] > 0:
        return 1, 'N. Attributed $ARR'
    elif row['Number of Opportunities'] > 0:
        return 2, 'Number of Opportunities'
    elif row['Onshape Primary Plan'] == "EDU Enterprise":
        return 3, 'Onshape Primary Plan'
    elif row['EDU Verified'] == 1:
        return 4, 'EDU Verified'
    else:
        return 5, 'Created Date'

def rank_entries(df):
    """Determines the master account"""
    if df.empty:
        raise ValueError("The DataFrame is empty.")
    df = df.copy()  # Ensure we are working with a copy to avoid SettingWithCopyWarning
    df['Created Date'] = pd.to_datetime(df['Created Date'], errors='coerce')
    df['rank'], df['deciding_factor'] = zip(*df.apply(rank_criteria, axis=1))
    criteria = ['N. Attributed $ARR', 'Number of Opportunities', 'Onshape Primary Plan', 'EDU Verified', 'Created Date']
    
    def resolve_ties(tied_df, criteria):
        for crit in criteria:
            if crit == 'Created Date':
                return tied_df.loc[tied_df[crit].idxmin()]
            else:
                if crit in tied_df.columns:
                    filtered_df = tied_df[tied_df[crit].notnull() & (tied_df[crit] != 0)]
                    if not filtered_df.empty:
                        if len(filtered_df) == 1:
                            return filtered_df.iloc[0]
                        tied_df = filtered_df
        return tied_df.iloc[0]

    min_rank_df = df[df['rank'] == df['rank'].min()]
    first_rank_entry = resolve_ties(min_rank_df, criteria) if len(min_rank_df) > 1 else min_rank_df.iloc[0]
    return first_rank_entry
