python
def transform_data(loans_df, alerts_df):
    # Join data on application_id
    merged_df = loans_df.merge(alerts_df, on='application_id', how='left', suffixes=('', '_fraud'))
    merged_df['is_fraud'] = merged_df['reason'].notnull()
    return merged_df[['application_id', 'user_id', 'credit_score', 'loan_amount', 'risk_level', 'is_fraud']]
