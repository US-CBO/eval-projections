# An Evaluation of CBO's Projections of Outlays from 1984 to 2021
The code and data in this repository allow users to replicate the results in CBO's Visual Report
 [*An Evaluation of CBO's Projections of Outlays from 1984 to 2021*](https://www.cbo.gov/publication/58613) by Aaron Feinstein, Analyst in CBO's Budget Analysis Division.

## How to Install the Code and Data
Follow these three steps to install the code and data associated with the **Evaluation of CBO's Projections of Outlays** analysis on your computer:

1. **Install the Anaconda distribution of Python**  
Download and install the Anaconda distribution of Python from Anaconda's [Installation page](https://docs.anaconda.com/anaconda/install/index.html).
</br></br>The **Evaluation of Outlay Projections** analysis was conducted using Python 3.8 on computers running Windows 10, although the analysis should run on other operating systems as well.
</br></br>The external packages used in the analysis were managed using Anaconda's built-in package manager, `conda`. To replicate the results in this repository, you will need to use `conda` to create a virtual environment that loads the same versions of Python and external packages used when the analysis was conducted. All the external packages (and their versions) are documented in the `environment.yml` file in the project’s root directory. That file is used to create a virtual environment that matches the one used when the analysis was conducted. This is done in step 3, below.

2. **Download the repository ("repo") from GitHub**  
There are several options for how to get the code and data from GitHub to your computer:

    * If you have `git` installed on your computer, you can `clone` a copy of the repo to your computer. This is done by entering the following command at the commandline:
    `git clone https://github.com/us-cbo/eval-outlays.git`

    * If you also have a GitHub account, you should first `fork` a copy of the repo to your own GitHub account and then `clone` it to your computer with the command:
    `git clone https://github.com/<your-GitHub-account-name>/eval-outlays.git`.

    * If you don’t have git installed on your computer, you can [download a zip file](https://github.com/us-cbo/eval-outlays/archive/refs/heads/main.zip) containing the entire repo and then unzip that file in a directory on your computer.

3. **Create the virtual environment**  
Once you have installed the Anaconda distribution of Python and you have downloaded a copy of the repo to your computer, follow these steps to create a virtual environment that will make sure you have all the appropriate dependencies to run the analysis:

    * Open the `Anaconda Prompt` application, which comes as part of the Anaconda installation

    * Navigate to the root directory where you cloned or downloaded the repository on your computer using the change directory (`cd`) command:
    `cd path/to/your/copy/of/CBO-eval-outlays`
    (The last subdirectory name, `CBO-eval-outlays`, is just a suggested name; you may name the subdirectory anything you wish.)

    * Create a virtual environment that matches the one used to conduct the **Evaluation of CBO's Projections of Outlays** analysis with the command:
    `conda env create -f environment.yml`
    (That command will create a virtual environment on your computer named `CBO-eval-outlays` and may take several minutes to complete.)

    * `activate` the newly created virtual environment with the command:
    `conda activate CBO-eval-outlays`
    (To replicate the results in the `/output_data/` directory, the code needs to be run from within that virtual environment.)

    * When you are finished working in the **CBO-eval-outlays** environment, `deactivate` the virtual environment from the Anaconda Prompts with the command:
    `conda deactivate`
    (This will return your computer to the `base` conda environment.)

## How to Run the Evaluation of CBO's Projections of Outlays Analysis
Once the above steps have been followed, and with the `CBO-eval-outlays` virtual environment activated you can run the analysis with the following command typed into the `Anaconda Prompt` from the root of the project directory:
`python src/main.py`

The analysis produces three output files, which will be written to the `/output_data/` directory.

1. `actual_outlays_pct_GDP.csv`  
This output file shows the actual outlays for each outlay category for each year through 2021.

2. `projection_errors.csv`  
This output file shows the projection errors for each outlay category for each projection year (1st to 11th) and for each year through 2021.

3. `projection_errors_summary_stats.csv`  
This output file calculates summary statistics (average error, average absolute error, root mean square error, and two-thirds spread of errors) for the individual projection errors in the `projection_errors.csv` file.

> When you are finished working with the repository, deactivate the virtual environment by typing: `conda deactivate` at the Anaconda Prompt.

## Input Data Descriptions
The input data for the analysis consists of four files.

1. `actual_GDP`  
This file contains GDP data for fiscal years 1989 to 2022. These data reflect historical information available as of February 2023 and are shown in billions of dollars.

2. `actual_outlays`  
This file contains actual outlay data for each outlay category and subcategory analyzed in this report. For Total Outlays, data include fiscal years 1984 to 2021. For every other category, data include fiscal years 1989 to 2021. These data reflect historical information as of the release of the President's 2024 Budget and are shown in billions of dollars.

3. `baseline_outlays`  
This file contains baseline outlay projections for each outlay category and subcategory analyzed in this report. Data are shown in billions of dollars.

    * For Total Outlays, data are from the Spring baselines from 1984 to 1991 and then each baseline since January 1992.
    * For Total Mandatory, Total Discretionary, Net Interest, Social Security, Medicare, Medicaid, and Other Mandatory outlays, data are from each baseline since January 1992.
    * For Defense Discretionary and Nondefense Discretionary outlays, data are from each baseline since January 1998.

4. `baseline_outlays_changes`  
This file contains the changes reported in CBO's budget and economic outlook reports for each outlay category and subcategory analyzed in this report. Those changes are divided between three categories: legislative, economic, and technical. Where applicable, this file also contains changes recorded for each fiscal year that occur after the last budget and economic outlook report of the year is published. Data are shown in billions of dollars.

    * For Total outlays, data are from each baseline since March 1984.
    * For Total Mandatory, Total Discretionary, Net Interest, Social Security, Medicare, Medicaid, and Other Mandatory outlays, data are from each baseline since January 1992.
    * For Defense Discretionary and Nondefense Discretionary outlays, data are from each baseline since January 1998.

## Technical Data Notes
### APB Flag
Error calculations in this analysis are only performed on the Spring baselines -- which are typically referred to as "Spring" or Analysis of President's Budget (APB) baselines. The `APB_flag` column in the `input_data/baseline_outlays.csv` file indicates which baseline each year is the Spring baseline.

### Fannie Freddie
For the purposes of this analysis, outlays for the housing entities Fannie Mae and Freddie Mac have been removed from CBO’s projections and from the actual amounts reported by the Treasury because CBO and the Administration account for those entities’ transactions differently.

### Baseline Dates
The files `input_data/baseline_outlays.csv` and `input_data/baseline_outlays_changes.csv` each have a column called `baseline_date`. The dates in those columns are string variables stored in [ISO-8601 date format](https://www.iso.org/iso-8601-date-and-time-format.html). For every value in those columns, the day is equal to '01' (the first of the month), which does not correpsond to the specific day that a baseline was released. As such, the `baseline_date` values should only be interpreted as indicating the *year* and the *month* in which the baseline was released.

## Contact
Questions about the code and data in this repository may be directed to CBO's Office of Communications at communications@cbo.gov.
