# Evaluating CBO's Projections of Components of the Federal Budget
The code and data in this repository allow users to replicate the evaluations CBO regularly conducts of its projections of various budget components: outlays, revenues, deficits, and debt. 

The most recent reports on those topics are:
* [*An Evaluation of CBO's Projections of Outlays from 1984 to 2021*](https://www.cbo.gov/publication/58613) 
* [*An Evaluation of CBO's Past Revenue Projections*](https://www.cbo.gov/publication/56499) 
* [*An Evaluation of CBO's Past Deficit and Debt Projections*](https://www.cbo.gov/publication/55234)
* [*The Accuracy of CBO’s Budget Projections for Fiscal Year 2023*](https://www.cbo.gov/publication/59838)

## How to Install the Code and Data
Follow these three steps to install the code and data associated with the **Evaluations of CBO's Past Projections of Outlays, Revenues, Deficits, and Debt** on your computer:

1. **Install the Anaconda distribution of Python**  
Download and install the Anaconda distribution of Python from Anaconda's [Installation page](https://docs.anaconda.com/anaconda/install/index.html).
</br></br>The **Evaluations of CBO's Past Projections of Outlays, Revenues, Deficits, and Debt** was conducted using Python 3.8 on computers running Windows 10, although the code should run on other operating systems as well.
</br></br>The external packages used in the code were managed using Anaconda's built-in package manager, `conda`. To replicate the results in this repository, you will need to use `conda` to create a virtual environment that loads the same versions of Python and external packages used when the code was run. All the external packages (and their versions) are documented in the `environment.yml` file in the project’s root directory. That file is used to create a virtual environment that matches the one used when the code was run. This is done in step 3, below.

2. **Download the repository ("repo") from GitHub**  
There are several options for how to get the code and data from GitHub to your computer:

    * If you have `git` installed on your computer, you can `clone` a copy of the repo to your computer. This is done by entering the following command at the commandline:
    `git clone https://github.com/us-cbo/eval-projections.git`

    * If you also have a GitHub account, you should first "fork" a copy of the repo to your own GitHub account and then `clone` it to your computer with the command:
    `git clone https://github.com/<your-GitHub-account-name>/eval-projections.git`

    * If you don’t have git installed on your computer, you can [download a zip file](https://github.com/us-cbo/eval-projections/archive/refs/heads/main.zip) containing the entire repo and then unzip that file in a directory on your computer.

3. **Create the virtual environment**  
Once you have installed the Anaconda distribution of Python and you have downloaded a copy of the repo to your computer, follow these steps to create a virtual environment that will make sure you have all the appropriate dependencies to run the code:

    * Open the `Anaconda Prompt` application, which comes as part of the Anaconda installation

    * Navigate to the root directory where you cloned or downloaded the repository on your computer using the change directory (`cd`) command:
    `cd path/to/your/copy/of/CBO-eval-projections`
    (The last subdirectory name, `CBO-eval-projections`, is just a suggested name; you may name the subdirectory anything you wish.)

    * Create a virtual environment that matches the one used to conduct the **Evaluation of CBO's Projections** code with the command:  
    `conda env create -f environment.yml`  
    (That command will create a virtual environment on your computer named `CBO-eval-projections` and may take several minutes to complete.)

    * Activate the newly created virtual environment with the command:  
    `conda activate CBO-eval-projections`  
    (To replicate the results in the `./output_data/` directory, the code needs to be run from within that virtual environment.)

    * Deactivate the **CBO-eval-projections** virtual environment when you are finished working with the repository with the command:  
    `conda deactivate`  
    (This will return your computer to the `base` conda environment.)

## How to Run the Evaluation of CBO's Projections
Once the above steps have been followed, and with the `CBO-eval-projections` virtual environment activated, you can run the code with the following command typed into the `Anaconda Prompt` from the root of the project directory:  

`python src/main.py`

The code produces 12 output files, which will be written to the `./output_data/` directory.

For each of the four budget component projections (`outlay`, `revenue`, `deficit`, and `debt`), the code produces three output files:

1. `[component]_actuals_pct_GDP.csv`  
These output files contain the actual values for each budget component projection as a percentage of GDP for each year.

2. `[component]_projection_errors.csv`  
These output files contain the projection errors for each budget component projection for each projection year (1st to 11th) and for each year.

3. `[component]_projection_errors_summary_stats.csv`  
These output files contain summary statistics (average error, average absolute error, root mean square error, and two-thirds spread of errors) for the projection errors in the `[component]_projection_errors.csv` file.

The program also allows users to run the code for just one (or two, or three) budget component(s). For example, to run the code for the just revenue data, type:

`python src/main.py revenue` 

To run the code for both deficits and debt, but not for outlays or revenues, type:

`python src/main.py deficit debt` 

Note that budget components passed into `main.py` must be singular and separated only by spaces.

> **Remember**  
> When you are finished working with the repository, deactivate the virtual environment by typing: `conda deactivate` at the Anaconda Prompt.

## Input Data Descriptions
The input data consists of the four files listed below.

For the purposes of these analyses, outlays for the housing entities Fannie Mae and Freddie Mac have been removed from CBO’s projections and from the actual amounts because CBO and the Administration account for those entities’ transactions differently (see the Fannie Mae and Freddie Mac Outlays section below for more detail). Also, actual outlays related to the Administration's 2022 planned cancellation of outstanding student loans for many borrowers were excluded from this analysis. (see the Student Loan Forgiveness Outlays section below for more detail).

For each of the four files, data are shown in billions of dollars.

1. `actual_gdp.csv`  
This file contains GDP data beginning in 1982. 

2. `actuals.csv`  
This file contains actual outlay, revenue, deficit, and debt data for each outlay and revenue category and outlay subcategory analyzed in the above report. 

    * For Total Outlays, data begin in fiscal year 1984. For every other category, data start in 1989. These data reflect historical information as of the release of the President's 2024 Budget.
    * For revenues, data begin in fiscal year 1982 to 2022 for every revenue category.
    * For deficts and debt, data begin in fiscal year 1984.

3. `baselines.csv`  
This file contains baseline outlay and revenues projections for each outlay and revenue category and outlay subcategory analyzed in this report. It also contains deficit and debt projections. 

    * For Total Outlays, data are from the Spring baselines from 1984 to 1991 and then each baseline since January 1992.
    * For Total Mandatory, Total Discretionary, Net Interest, Social Security, Medicare, Medicaid, and Other Mandatory outlays, data are from each baseline since January 1992.
    * For Defense Discretionary and Nondefense Discretionary outlays, data are from each baseline since January 1998.
    * For revenues, data are from the Winter baselines since February 1982.
    * For deficits, data are from the Spring baselines since February 1984.
    * For debt, data are from the Spring baselines since February 1984.

4. `baseline_changes.csv`  
This file contains the changes reported in CBO's budget and economic outlook reports for each outlay category and subcategory analyzed in this report. Those changes are divided between three categories: legislative, economic, and technical. For revenues, only the legislative changes are shown. Where applicable, this file also contains changes recorded for each fiscal year that occur after the last budget and economic outlook report of the year is published.

## Technical Data Notes

### Baseline Dates
The files `input_data/baselines.csv` and `input_data/baseline_changes.csv` have a baseline_date column, named `baseline_date` and `changes_baseline_date`, respectively. The dates in those columns are string variables stored in [ISO-8601 date format](https://www.iso.org/iso-8601-date-and-time-format.html). For every value in those columns, the day is equal to '01' (the first of the month), which does not correpsond to the specific day that a baseline was released. As such, the `baseline_date` values should only be interpreted as indicating the *year* and the *month* in which the baseline was released.

### Winter Flag
For revenues, error calculations are only performed on the Winter baselines. The `Winter_flag` column in the `input_data/baselines.csv` file indicates which baseline each year is the Winter baseline.

### Spring Flag
For outlays, deficits, and debt, error calculations are only performed on the Spring baselines. The `Spring_flag` column in the `input_data/baselines.csv` file indicates which baseline each year is the Spring baseline.

### Fannie Mae and Freddie Mac Outlays
For the purposes of these analyses, outlays for the housing entities Fannie Mae and Freddie Mac have been removed from CBO’s projections and from the actual amounts reported by the Treasury, because CBO and the Administration account for those entities’ transactions differently. This affects the Total Outlays, the Mandatory category and Other Mandatory subcategory of outlays, as well as the deficit and debt projections. 

### Student Loan Forgiveness Outlays
Because of their unusual size and nature, the estimated budgetary effects of both the Administration’s 2022 planned cancellation of outstanding student loans for many borrowers and the Supreme Court’s subsequent decision prohibiting the Administration from implementing that plan were excluded from this analysis. This affects the actuals for Total Outlays, the Mandatory category and Other Mandatory subcategory of outlays, as well as for the deficit in 2022 and 2023.

For more details, see [*The Accuracy of CBO’s Budget Projections for Fiscal Year 2023*](https://www.cbo.gov/publication/59838#_idTextAnchor003).

## Contact
Questions about the code and data in this repository may be directed to CBO's Office of Communications at communications@cbo.gov.
