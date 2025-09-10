# read in a shapefile of US counties, MUST SELECT the .shp!
us_county = gpd.read_file('Data/US_COUNTY_SHPFILE/US_county_cont.shp')
tx_county = us_county[us_county['STATE_NAME'] == 'Texas']

not_ERCOT_counties = ["Dallam", "Sherman", "Hansford", "Ochiltree", "Lipscomb", "Hartley", "Moore", "Hutchinson", "Hemphill",
                      "Bailey", "Lamb", "Cochran", "Hockley", "Terry", "Yoakum", "Gaines",
                      "El Paso", "Hudspeth",
                      "Bowie", "Morris", "Cass", "Camp", "Upshur", "Marion", "Gregg", "Harrison", "Panola", "Shelby", "San Augustine", "Sabine", "Trinity", "San Jacinto", "Polk", "Tyler", "Jasper", "Newton", "Liberty", "Hardin", "Orange", "Jefferson"]

ERCOT_counties = tx_county[~tx_county['NAME'].isin(not_ERCOT_counties)]
ERCOT_counties_df = pd.DataFrame(ERCOT_counties)

ercot_mapping = ERCOT_counties_df.set_index('NAME')['FIPS'].to_dict()


county_region_map = pd.read_csv("Data/ercot_county_region_map.csv")


base_folder = "Data/nrel_tempo_raw"
folders = ["efs", "evs_2035", "ref"]
output_folder = "Data/nrel_tempo_ercot"

for folder in folders:
    folder_path = os.path.join(base_folder, folder)
    output_folder_path = os.path.join(output_folder, folder)
    os.makedirs(output_folder_path, exist_ok=True)  # Ensure output subfolder exists

    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        if file_name.endswith(".parquet"):
            print(f"Processing file: {file_path}")
            df = pd.read_parquet(file_path)
        # Sort by time_est to ensure correct order
        df = df.sort_values(['time_est', 'county'], ascending=[True, True]).reset_index(drop=True)

        # Create t mapping: map each unique time_est to a number 1..N
        unique_times = pd.Series(df['time_est'].unique()).sort_values().reset_index(drop=True)
        time_to_t = {ts: i + 1 for i, ts in unique_times.items()}

        # Apply mapping
        df['t'] = df['time_est'].map(time_to_t)

        # Remove t last hour if all values are NaN
        last_t = max(time_to_t.values())
        if df[df['t'] == last_t]['value'].isnull().all():
            df = df[df['t'] != last_t]
          
        cols = list(df.columns)
        if 't' in cols:
            cols.insert(1, cols.pop(cols.index('t')))
            df = df[cols]
          
        df['county'] = df['county'].astype(int)
        merged = df.merge(county_region_map, left_on="county", right_on="FIPS", how="left")
        merged = merged.drop(columns=['county'])

      
        # Save tt DataFrame with t column to tt same file
        output_file_path = os.path.join(output_folder_path, file_name)
        merged.to_parquet(output_file_path, index=False)
