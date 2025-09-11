
# Define EV availability schedule by hour
def get_ev_avail(hour):
    if 0 <= hour < 8:
        return 0.8
    elif 8 <= hour < 18:
        return 0.4
    else:
        return 0.8


# Define SOC requirement schedule by hour
def get_soc_req(hour):
    if hour == 8:
        return 0.8
    else:
        return 0
df['SOC_req'] = df['hour'].apply(get_soc_req)


# Define EV driving loss schedule by hour
def get_driving_loss(hour):
    # 9am and 6pm: SOC drops by 0.2 (20%)
    if hour == 9 or hour == 18:
        return 0.2
    else:
        return 0.0
df['driving_loss'] = df['hour'].apply(get_driving_loss)


cols_to_drop = ['month', 'day', 'hour']
df.drop(columns=[col for col in cols_to_drop if col in df.columns], inplace=True)

df.to_csv('Data/ev_schedule.csv', index=False)
