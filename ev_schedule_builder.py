# Define SOC requirement schedule by hour
def get_soc_req(hour):
    if hour < 8:
        return 0.8
    else:
        return 0

# Apply the SOC requirement schedule to each row
df['SOC_req'] = df['hour'].apply(get_soc_req)

# Display the updated DataFrame
df.head()

# Define EV driving loss schedule by hour
def get_driving_loss(hour):
    # 9am and 6pm: SOC drops by 0.2 (20%)
    if hour == 9 or hour == 18:
        return 0.2
    else:
        return 0.0

# Apply the driving loss schedule to each row
df['driving_loss'] = df['hour'].apply(get_driving_loss)

# Display the updated DataFrame
df.head(12)

cols_to_drop = ['month', 'day', 'hour']
df.drop(columns=[col for col in cols_to_drop if col in df.columns], inplace=True)

df.to_csv('ev_schedule.csv', index=False)
