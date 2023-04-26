import os.path
import pandas as pd
import errors
from scale_actuals import scale_actuals


# Set directory paths
CURRENT_PATH = os.path.abspath(os.path.dirname(__file__))
INPUT_PATH = f"{CURRENT_PATH}/../input_data"
OUTPUT_PATH = f"{CURRENT_PATH}/../output_data"

# Read in all the data
actuals = pd.read_csv(f"{INPUT_PATH}/actual_outlays.csv")
baselines = pd.read_csv(f"{INPUT_PATH}/baseline_outlays.csv")
changes = pd.read_csv(f"{INPUT_PATH}/baseline_outlays_changes.csv")
GDP = pd.read_csv(f"{INPUT_PATH}/actual_GDP.csv")

# Merge data, calc errors, and calc summary stats and scaled actuals
projection_data = errors.merge_data(actuals, baselines, changes)
projection_errors = errors.calc_errors(projection_data)
summary_stats = errors.calc_summary_stats(projection_errors)
scaled_actuals = scale_actuals(actuals, GDP)

# Write out csv data files
projection_errors.to_csv(f"{OUTPUT_PATH}/projection_errors.csv",
    index=False, float_format="%.1f"
)

summary_stats.to_csv(f"{OUTPUT_PATH}/projection_errors_summary_stats.csv",
    index=False, float_format="%.1f"
)

scaled_actuals.to_csv(f"{OUTPUT_PATH}/actual_outlays_pct_GDP.csv",
    index=False, float_format="%.1f"
)
