# cog-groupwise-boxplot
Dynamic visualization and statistical analysis of COG data with groupwise boxplots and pairwise significance testing. This script dynamically generates boxplots and scatter plots for categorized data with multiple groups, performs pairwise statistical significance testing, and visualizes the significant differences with horizontal lines and stars. It is adaptable to any number of groups and outputs clear, annotated visualizations.

---

## Features
- Dynamically handles any number of groups.
- Calculates pairwise statistical significance using the Mann-Whitney U test.
- Visualizes results with boxplots and scatter plots for each category and group.
- Marks significant pairwise differences with horizontal lines and stars.
- Outputs plots and statistical results for downstream analysis.

---

## Input

### Files
1. **combined_classifier_count.tsv**: Contains data with columns for `LETTER`, `COLOR`, `Category`, `Class`, and individual isolates.
2. **isolate_colors.tsv**: Maps isolates to their respective groups.

---

## Output

### Files
1. **Boxplots**: Generated for each category and saved as PDFs in the `output/` directory. 
   - File names are formatted as `boxplot_<category>.pdf`.
2. **Statistics Table**: Saved as a TSV file in the `output/` directory.
   - File name: `statistics.tsv`
   - Columns: `Category`, `LETTER`, `Group1`, `Mean1`, `Group2`, `Mean2`, `P-value`, `Significant`.

---

## Usage

### 1. Setup
Ensure the input files are placed in the `input/` directory and match the expected structure.

### 2. Run the Script
Execute the script from the command line:
```bash
python dynamic_significance_plotter.py
```

### 3. View Results
Check the `output/` directory for:
- Boxplots visualizing the data and significance results.
- The `statistics.tsv` file for the pairwise comparison results.

---

## Dependencies
- Python 3.7+
- Required Python Libraries:
  - `pandas`
  - `matplotlib`
  - `seaborn`
  - `scipy`
  - `statsmodels`

Install dependencies using:
```bash
pip install -r requirements.txt
```

---

## Citation
If you are using the `groupwise_boxplot.py` script, please cite it as follows:

Sharma, V. (2024). groupwise_boxplot.py [Python script]. Retrieved from [https://github.com/vsmicrogenomics/cog-groupwise-boxplot]

---

## Acknowledgements
This script utilizes COGclassifier output. Please acknowledge the use of COGclassifier by referring to the tool at [https://github.com/ncbi/amr](https://github.com/moshi4/COGclassifier]



