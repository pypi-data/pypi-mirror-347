# 🧘 Shanti

create **SH**arable, interactive, st**AN**dalone html dashboard from **T**abular proteom**I**cs data

**Shanti** is a Python library for creating interactive, standalone HTML dashboards from proteomics data (specifically tabular data in Excel format). This package simplifies the process of creating volcano plots and histograms. This tool uses [Bokeh](https://bokeh.org) library in the background to generate a HTML file that contains interactive plots and tables. The HTML files can be opened in a browser (Firefox, Chrome, Safari, Edge) and shared with colleagues. Your colleagues can explore proteomics data with without requiring any server or software installation. This tool is relevant for Mass Spectrometry Core Facilities to create protoemics reports for clients. This tool is conceptualized, designed, built, documented and published by [Nara Marella](https://github.com/nara3m) at the Molecular Discovery Platform of [CeMM](https://cemm.at) Research Center for Molecular Medicine of the Austrian Academy of Sciences, Vienna

Table of Contents

1. [Installation](#installation)
2. [Key Components](#key-components)
3. [Input Files Required](#input-files-required)
4. [Usage](#usage)
5. [Final Output](#final-output)
6. [FAQ](#faq)
7. [For Developers](#for-developers)
8. [Cite](#cite)


## 📦 Installation

You can install the package with pip:

```bash
pip install shanti
```

## 🚀 Key Components

### 1. `load_data()` 

loads proteomics data from Excel files, processes it, and prepares it for visualization. The volcano plot visualization includes threshold curves for significance. The curves are calculated based on the threshold function in [CurveCurator](https://github.com/kusterlab/curve_curator) package. Some default parameters are already set in example snippet below. Only one parameter `fc_lim` needs to adjusted frequently

#### with basic parameters

```python
source = load_data(
    file_path = "Shanti_Test_Proteins.xlsx",
    fc_lim = 0.25,
    l2fc_col = "KO_WT_l2FC",
    pAdj_col = "KO_WT_pAdj"
)
```

- `file_path` is the path to file containing Protein level data. See [Shanti_Test_Proteins.xlsx](https://zenodo.org/records/15307776/files/Shanti_Test_Proteins.xlsx?download=1) for the format of Protein level data file. Column `UniProtID` is mandatory and column name is hardcoded. Other column names are flexible. ⚠️ Avoid special characters or blank spaces in table column names of the input file because output HTML file does not parse special column names correctly
- `fc_lim` is the threshold for significance curve. Although a default value is defined, this parameter should be manually adjusted for each new run becasue of the unique data distribution of input. After trail and error, `0.25` was selected as the best value for column `KO_WT_l2FC` in demo dataset (Shanti_Test_Proteins.xlsx)
- `l2fc_col` is the column name contining log2 fold change values. In demo dataset ([Shanti_Test_Proteins.xlsx](https://zenodo.org/records/15307776/files/Shanti_Test_Proteins.xlsx?download=1)), column `KO_WT_l2FC` was used
- `pAdj_col` is the column name contining adjusted P values. In demo dataset ([Shanti_Test_Proteins.xlsx](https://zenodo.org/records/15307776/files/Shanti_Test_Proteins.xlsx?download=1)), column `KO_WT_pAdj` was used

#### with advanced parameters

to fine tune the threshold curve, additional parameters such as `alpha`, `dfn`, `dfd`, `loc`, `scale`, `two_sided` can be adjusted

```
source = load_data(
    file_path = "Shanti_Test_Proteins.xlsx",
    sheet_name=0,
    alpha = 0.05,
    dfn = 10,
    dfd = 10,
    loc = 0,
    scale = 1,
    two_sided=False,
    fc_lim = 0.25,
    l2fc_col = "KO_WT_l2FC",
    pAdj_col = "KO_WT_pAdj"
)
```

### 2. `make_histogram()` 

creates histograms of the control and treated sample groups. The bin sizes are set to 20 but can be adjusted in the source code

```python
hist, data_filtered, bin_edges_log, bottoms, bar_height = make_histogram(
    source=source,
    hist_col="AN_KO_Mean",
    title="KO dTAG",
    x_axis_label="protein count"
)
```

- `source` is output of `load_data()` function
- `hist_col` is the name of the column containing abundance (or normalized abundances). The numerator in the fold change ratio is usually the first histogram (for example, call it `hist1` instead of `hist`). In example dataset [Shanti_Test_Proteins.xlsx](https://zenodo.org/records/15307776/files/Shanti_Test_Proteins.xlsx?download=1), column `AN_KO_Mean` is used for first histogram. `KO` meaning KnockOut or Treatment Group. The denominator in the fold change ratio is usually the second histogram (for example, call it `hist2` instead of `hist`). In example dataset, column `AN_WT_Mean` is used for second histogram. `WT` meaning WildType or Control Group
- `title` is the `str` to diplay on top of Histogram in HTML output file. Default is no title
- `x_axis_label` default is empty, but good to give a `str`

### 3. `create_interactive_dashboard()` 
generates final output HTML file

```python
create_interactive_dashboard(
    source,
    l2fc_col="KO_WT_l2FC",
    pAdj_col="KO_WT_pAdj",
    volcano_title="KO dTAG vs DMSO Comparison",
    hist1_col="AN_KO_Mean",
    hist2_col="AN_WT_Mean",
    table_columns=["UniProtID", "Gene", "Description", "Peptides", "PeptidesU", "PSMs"],
    peptides_file="Shanti_Test_PeptideGroups.xlsx",
    peptide_columns=["UniProtID", "Sequence", "ProteinGroups", "Proteins", "PSMs", "Position", "MissedCleavages", "QuanInfo"],
    output_path="dashboard.html"
    plot2=hist1,
    plot3=hist2,
    hist1_data_filtered=hist1_data_filtered,
    hist2_data_filtered=hist2_data_filtered,
    hist1_bin_edges_log=hist1_bin_edges_log,
    hist2_bin_edges_log=hist2_bin_edges_log,
    hist1_bottoms=hist1_bottoms,
    hist2_bottoms=hist2_bottoms,
    hist1_bar_height=hist1_bar_height,
    hist2_bar_height=hist2_bar_height,
)
```

- `source` is output of `load_data()` function
- `l2fc_col` and `pAdj_col` were explained in `load_data()` function
- `volcano_title` is `str` to display on top of the Volcano Plot in HTML file. Default is empty
- `table_columns` are the lsit of Protein columns to display. Number of columns to display are fixed at 6 becuase of the HTML page dimentions. In Test example, Shanti_Test_Proteins.xlsx, columns UniProtID, Gene, Description, Peptides, PeptidesU, PSMs were selected to display
- `peptides_file` is path to the file containing Peptide level data. Column name `UniProtID` is mandatory and hardcoded. See Shanti_Test_PeptideGroups.xlsx for the format. Other column names are flexible
- `peptide_columns` are the columns to disaply in HTML file. Columns UniProtID, Sequence, ProteinGroups, Proteins, PSMs, Position, MissedCleavages, QuanInfo from Shanti_Test_PeptideGroups.xlsx were used to generate demo HTML file. Limited to 8 columns becuase of the HTML page dimentions. Column widths can be adjusted in source code but not directly accessible with function arguments
- `output_path` is the filename of the HTML file. defaults to `dashboard.html`
- `hist1_col` and `hist2_col` were explained in `make_histogram()` function
- `plot2`, `plot3`, `hist1_data_filtered`, `hist2_data_filtered`, `hist1_bin_edges_log`, `hist2_bin_edges_log`, `hist1_bottoms`, `hist2_bottoms`, `hist1_bar_height`, `hist2_bar_height` are outputs of `make_histogram()` function

### `DataProcessor()` 

internal Class that handles

- Statistical calculations specifically for protein level data
- Classification of volcano data points based on significance thresholds

## 📂 Input Files Required
1. Protein data Excel file (e.g. [Shanti_Test_Proteins.xlsx](https://zenodo.org/records/15307776/files/Shanti_Test_Proteins.xlsx?download=1))
2. Peptide data Excel file (e.g. [Shanti_Test_PeptideGroups.xlsx](https://zenodo.org/records/15307776/files/Shanti_Test_PeptideGroups.xlsx?download=1))

## 🧪 Usage

⚠️ `create_interactive_dashboard()` function fails in Jupyter notebooks because of the incompatibility with [Bokeh](https://bokeh.org). Therefore, for example, combine `load_data()`, `make_histogram()` and `create_interactive_dashboard()` snippets in a python script called `run.py` and exectute from termainal.

```python
# save as run.py

from shanti import load_data, make_histogram, create_interactive_dashboard

source = load_data(
    file_path = "Shanti_Test_Proteins.xlsx",
    fc_lim = 0.25,
    l2fc_col = "KO_WT_l2FC",
    pAdj_col = "KO_WT_pAdj"
)

hist1, hist1_data_filtered, hist1_bin_edges_log, hist1_bottoms, hist1_bar_height = make_histogram(
    source=source,
    hist_col="AN_KO_Mean",
    title="KO dTAG",
    x_axis_label="protein count"
)

hist2, hist2_data_filtered, hist2_bin_edges_log, hist2_bottoms, hist2_bar_height = make_histogram(
    source,
    hist_col="AN_WT_Mean",
    title="DMSO",
    x_axis_label="protein count"
)

create_interactive_dashboard(
    source,
    l2fc_col="KO_WT_l2FC",
    pAdj_col="KO_WT_pAdj",
    volcano_title="KO dTAG vs DMSO Comparison",
    hist1_col="AN_KO_Mean",
    hist2_col="AN_WT_Mean",
    table_columns=["UniProtID", "Gene", "Description", "Peptides", "PeptidesU", "PSMs"],
    peptides_file="Shanti_Test_PeptideGroups.xlsx",
    peptide_columns=["UniProtID", "Sequence", "ProteinGroups", "Proteins", "PSMs", "Position", "MissedCleavages", "QuanInfo"],
    output_path="dashboard.html"
    plot2=hist1,
    plot3=hist2,
    hist1_data_filtered=hist1_data_filtered,
    hist2_data_filtered=hist2_data_filtered,
    hist1_bin_edges_log=hist1_bin_edges_log,
    hist2_bin_edges_log=hist2_bin_edges_log,
    hist1_bottoms=hist1_bottoms,
    hist2_bottoms=hist2_bottoms,
    hist1_bar_height=hist1_bar_height,
    hist2_bar_height=hist2_bar_height,
)
```

```bash
python run.py
```

## 📊 Final Output

The result of `run.py` is a fully interactive HTML dashboard that can be opened in any moderen browser. A demo HTML output file created with Test datasets is available [here](https://shanti-v010.netlify.app/).

- Volcano Plot showing log fold change vs p-value
- Histograms comparing protein abundance distribution overlaid with selected proteins
- Interactive tables of proteins and peptides
- Ability to click/select proteins and see related peptides instantly

Detailed guide to understand output HTML file and perform interactive data exploration is available here: [nara3m.github.io/shanti](https://nara3m.github.io/shanti/index.html)

![Demo output HTML file created with Test Datasets](https://github.com/nara3m/shanti/raw/refs/heads/main/img/kinase2.png)

## 🧑‍💻 For Developers
To extend or modify this tool:

- Check the shanti [source code](https://github.com/n3m4u/shanti)
- Edit the histogram, volcano, or dashboard layout logic

## 🙋 FAQ
**Q**: What kind of Excel format is expected?

**A**: See [Shanti_Test_Proteins.xlsx](https://zenodo.org/records/15307776/files/Shanti_Test_Proteins.xlsx?download=1) and [Shanti_Test_PeptideGroups.xlsx](https://zenodo.org/records/15307776/files/Shanti_Test_PeptideGroups.xlsx?download=1). The protein and peptide files should contain a mandatory column with the name `UniProtID`. It is hard coded. A fold change column, a p-value (or adjusted p value) column, two normalized abundance columns (for histograms) are minimum columns required. See [demo HTML file](https://shanti-v010.netlify.app/) for columns used in Protien and Petide tables. It is recommended to have atleast 6 Protein columns and 8 Peptide columns to display in table. It is also possible to display log2 fold change and p values in Protein table. ⚠️ The `UniProtID` (**name is hardcoded**) column in Protein table should contain only one ID per row.  ⚠️ The `UniProtID` (**name is hardcoded**) column in Peptide table **can** contain multiple colon `;` seperated `UniProtID`s.

**Q**: Does it support .csv files?

**A**: Not yet, but it's easy to adapt by editing the load_data function.

## 📬 Questions?
Feel free to open an [issue](https://github.com/n3m4u/shanti/issues) or reach out with feedback!

## Cite
Marella, N. (2025). Shanti: create SHarable, interactive, stANdalone html dashboard from Tabular proteomIcs data (v0.1.1). Zenodo. [doi.org/10.5281/zenodo.15307776](https://doi.org/10.5281/zenodo.15307776)
