import os.path
import sys
import pandas as pd
from merge import merge_data
from errors import calc_errors
from summary import calc_summary_stats
from scale import scale_actuals
from write_Excel import write_Excel

CURRENT_PATH = os.path.abspath(os.path.dirname(__file__))
INPUT_PATH = os.path.abspath(f"{CURRENT_PATH}/../input_data")
OUTPUT_PATH = os.path.abspath(f"{CURRENT_PATH}/../output_data")

actuals = pd.read_csv(f"{INPUT_PATH}/actuals.csv")
baselines = pd.read_csv(f"{INPUT_PATH}/baselines.csv")
changes = pd.read_csv(f"{INPUT_PATH}/baseline_changes.csv")
GDP = pd.read_csv(f"{INPUT_PATH}/actual_GDP.csv")
print("Input data read")

scaled_actuals = scale_actuals(actuals, GDP)
dfs = (actuals, baselines, changes, GDP)

if len(sys.argv[1:]) == 0:
    components = ["outlay", "revenue", "deficit", "debt"]
else:
    components = sys.argv[1:]

for component in components:
    assert_message = "You passed an invalid argument to src/main.py.\nPlease try again."
    assert component in ["outlay", "revenue", "deficit", "debt"], assert_message

    print(f"Analyzing {component} data")
    projection_data = merge_data(dfs, component)
    projection_errors = calc_errors(projection_data, component)
    summary_stats = calc_summary_stats(projection_errors, component)
    print("    Projection errors and summary stats calculated")

    projection_errors.to_csv(
        f"{OUTPUT_PATH}/{component}_projection_errors.csv",
        index=False,
        float_format="%.3f",
    )
    summary_stats.to_csv(
        f"{OUTPUT_PATH}/{component}_projection_errors_summary_stats.csv",
        index=False,
        float_format="%.1f",
    )
    scaled_actuals.loc[(scaled_actuals["component"] == component), :].to_csv(
        f"{OUTPUT_PATH}/{component}_actuals_pct_GDP.csv",
        index=False,
        float_format="%.1f",
    )
    print("    Output data written")

print("\nProgram finished successfully.")
print(f"Results files were written to: {OUTPUT_PATH}.\n")

write_Excel()
