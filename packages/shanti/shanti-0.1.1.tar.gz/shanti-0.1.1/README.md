# 🧘 Shanti

create **SH**arable, interactive, st**AN**dalone html dashboard from **T**abular proteom**I**cs data

**Shanti** is a Python library for creating interactive, standalone HTML dashboards from proteomics data (specifically tabular data in Excel format). This package simplifies the process of creating volcano plots and histograms. This tool uses [Bokeh](https://bokeh.org) library in the background to generate a HTML file that contains interactive plots and tables. The HTML files can be opened in a browser (Firefox, Chrome, Safari, Edge) and shared with colleagues. Your colleagues can explore proteomics data with without requiring any server or software installation. This tool is relevant for Mass Spectrometry Core Facilities to create protoemics reports for clients. This tool is conceptualized, designed, built, documented and published by Nara Marella at the Molecular Discovery Platform of [CeMM](https://cemm.at) Research Center for Molecular Medicine of the Austrian Academy of Sciences, Vienna.

## 📦 Installation

You can install the package with pip:

```bash
pip install shanti
```

## 🚀 Key Components

`load_data()` loads proteomics data from Excel files, processes it, and prepares it for visualization. The volcano plot visualization includes threshold curves for significance. The curves are calculated based on the threshold function in [CurveCurator](https://github.com/kusterlab/curve_curator) package. Some default parameters are already set in example snippet below. Only one parameter `fc_lim` needs to adjusted frequently.

`make_histogram()` creates histograms of the control and treated sample groups. The bin sizes are set to 20 but can be adjusted in the source code.

`create_interactive_dashboard()` generates an interactive Bokeh dashboard

- A volcano plot showing log2 fold change vs. -log10 adjusted p-value
- Histograms overlaid with selected proteins from volcano plot
- Filter sliders and search functionality
- A protein data table and a peptide data table

`DataProcessor` is the internal Class that handles

- Statistical calculations specifically for protein level data
- Classification of volcano data points based on significance thresholds
- Creation of histograms for protein abundance visualization

## 📂 Input Files Required
- Protein data Excel file (e.g. [Shanti_Test_Proteins.xlsx](https://zenodo.org/records/15307776/files/Shanti_Test_Proteins.xlsx?download=1))
- Peptide data Excel file (e.g. [Shanti_Test_PeptideGroups.xlsx](https://zenodo.org/records/15307776/files/Shanti_Test_PeptideGroups.xlsx?download=1))

## 🧪 Usage

Here's a simple example to demonstrate how to use the `shanti` package:

### Load data with custom parameters

#### with basic parameters

```python
from shanti import load_data, make_histogram, create_interactive_dashboard

source = load_data(
    file_path = "Shanti_Test_Proteins.xlsx",
    fc_lim = 0.25,
    l2fc_col = "KO_WT_l2FC",
    pAdj_col = "KO_WT_pAdj"
)
```
`file_path` is the path to file containing Protein level data. See Shanti_Test_Proteins.xlsx for the format. Column `UniProtID` is mandatory and column name is hardcoded. Other column names are flexible.

⚠️ Avoid special characters or blank spaces in table column names of the input file because output HTML file does not parse special column names correctly.

`fc_lim` is the threshold for significance curve. Although a default value is defined, this parameter should be manually adjusted for each new run becasue of the unique data distribution of input. After trail and error, `0.25` was selected as the best value for column `KO_WT_l2FC` in demo dataset (Shanti_Test_Proteins.xlsx)

`l2fc_col` is the column name contining log2 fold change values. In demo dataset (Shanti_Test_Proteins.xlsx), column `KO_WT_l2FC` was used.

`pAdj_col` is the column name contining adjusted P values. In demo dataset (Shanti_Test_Proteins.xlsx), column `KO_WT_pAdj` was used.

#### with advanced parameters

To fine tune the threshold curve, additional parameters such as `alpha`, `dfn`, `dfd`, `loc`, `scale`, `two_sided` can be adjusted.

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

### Create histograms for visualization:

```python
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
```

`source` is output of `load_data()` function
`hist_col` is the name of the column containing abundance (or normalized abundances). The numerator in the fold change ratio is first histogram `hist1`. In example dataset, column `AN_KO_Mean`. `KO` meaning KnockOut or Treatment Group. The denominator in the fold change ratio is second histogram `hist2`. In example dataset, column `AN_WT_Mean`. `WT` meaning WildType or Control Group.

`title` is the `str` to diplay on top of Histogram in HTML output file. Default is no title.

`x_axis_label` default is empty, but good to give a `str`

### Generate the interactive dashboard:

```python
dashboard_path = create_interactive_dashboard(
    source,
    l2fc_col="KO_WT_l2FC",
    pAdj_col="KO_WT_pAdj",
    volcano_title="KO dTAG vs DMSO Comparison",
    hist1_col="AN_KO_Mean",
    hist2_col="AN_WT_Mean",
    table_columns=["UniProtID", "Gene", "Description", "Peptides", "PeptidesU", "PSMs"],
    peptides_file="shanti/data/Shanti_Test_PeptideGroups.xlsx",
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

`source` is output of `load_data()` function
`l2fc_col` and `pAdj_col` were explained in `load_data()` function
`volcano_title` is `str` to display on top of the Volcano Plot in HTML file. Default is empty
`table_columns` are the lsit of Protein columns to display. Number of columns to display are fixed at 6 becuase of the HTML page dimentions. In Test example, Shanti_Test_Proteins.xlsx, columns UniProtID, Gene, Description, Peptides, PeptidesU, PSMs were selected to display.

`peptides_file` is path to the file containing Peptide level data. Column name `UniProtID` is mandatory and hardcoded. See Shanti_Test_PeptideGroups.xlsx for the format. Other column names are flexible.

`peptide_columns` are the columns to disaply in HTML file. Columns UniProtID, Sequence, ProteinGroups, Proteins, PSMs, Position, MissedCleavages, QuanInfo from Shanti_Test_PeptideGroups.xlsx were used to generate demo HTML file. Limited to 8 columns becuase of the HTML page dimentions. Column widths can be adjusted in source code but not directly accessible with function arguments.

`output_path` is the filename of the HTML file. defaults to `dashboard.html`

`hist1_col` and `hist2_col` were explained in `make_histogram()` function

`plot2`, `plot3`, `hist1_data_filtered`, `hist2_data_filtered`, `hist1_bin_edges_log`, `hist2_bin_edges_log`, `hist1_bottoms`, `hist2_bottoms`, `hist1_bar_height`, `hist2_bar_height` are outputs of `make_histogram()` function

⚠️ `create_interactive_dashboard()` function fails in Jupyter notebooks because of the incompatibility with [Bokeh](https://bokeh.org). Therefore, for example, combine `load_data()`, `make_histogram()` 1, 2, `create_interactive_dashboard()` snippets in a python script called `run.py` and exectute from termainal.

```bash
python run.py
```

## 📊 Final Output

The result of `create_interactive_dashboard()` is a fully interactive HTML dashboard that can be opened in any moderen browser. A demo HTML output file created with Test datasets is available [here](https://shanti-v010.netlify.app/).

- Volcano Plot showing log fold change vs p-value
- Histograms comparing protein abundance distribution overlaid with selected proteins
- Interactive tables of proteins and peptides
- Ability to click/select proteins and see related peptides instantly

Detailed guide to understand output HTML file and perform interactive data exploration is available here: [nara3m.github.io/shanti](https://nara3m.github.io/shanti/index.html)

## 🧑‍💻 For Developers
To extend or modify this tool:

- Check the shanti [source code](https://github.com/n3m4u/shanti)
- Edit the histogram, volcano, or dashboard layout logic

## 🙋 FAQ
**Q**: What kind of Excel format is expected?
**A**: See [Shanti_Test_Proteins.xlsx](https://zenodo.org/records/15307776/files/Shanti_Test_Proteins.xlsx?download=1) and [Shanti_Test_PeptideGroups.xlsx](https://zenodo.org/records/15307776/files/Shanti_Test_PeptideGroups.xlsx?download=1). The protein and peptide files should contain a mandatory column with the name `UniProtID`. It is hard coded. A fold change column, p-value columns, two normalized abundance columns for Histograms are minimum columns required. See demo HTML file for recommended Protien and Petide table columns. The `UniProtID` column in Protein table should contain only one ID per row. The `UniProtID` column in Peptide table can contain multiple colon `;` seperated IDs.

**Q**: Does it support .csv files?
**A**: Not yet, but it's easy to adapt by editing the load_data function.

## 📬 Questions?
Feel free to open an [issue](https://github.com/n3m4u/shanti/issues) or reach out with feedback!

## Cite:
Marella, N. (2025). Shanti: create SHarable, interactive, stANdalone html dashboard from Tabular proteomIcs data (v0.1.1). Zenodo. [doi.org/10.5281/zenodo.15307776](https://doi.org/10.5281/zenodo.15307776)
