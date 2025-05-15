# 🏡 homestock

[![image](https://img.shields.io/pypi/v/homestock.svg)](https://pypi.org/project/homestock/)

[![image](https://pyup.io/repos/github/jpepper19/homestock/shield.svg)](https://pyup.io/repos/github/jpepper19/homestock)

**homestock** is a Python package designed to simplify access to **American Community Survey (ACS)** data from the U.S. Census Bureau. It enables users to fetch detailed demographic, housing, and economic data, and seamlessly convert the results into `pandas` DataFrames or CSV files for further analysis.

Whether you're exploring patterns at the state level or diving deep into neighborhoods using census tracts and block groups, **homestock** provides a flexible, scriptable workflow for researchers, students, journalists, and developers.

---

## 📊 What is the ACS?

The **American Community Survey (ACS)** is an ongoing survey conducted by the U.S. Census Bureau that collects vital information on income, education, housing, employment, and more.

There are two primary types of ACS data products:

### 🔹 1-Year Estimates
- Based on data collected over **12 months**
- Available for **areas with populations of 65,000+**
- Best for analyzing **current trends** in large cities or regions
- Less stable for small populations due to smaller sample size

### 🔸 5-Year Estimates
- Based on data collected over **60 months (5 years)**
- Available for **all geographic areas**, down to **block groups**
- Best for **granular spatial analysis** or long-term planning
- More reliable for small population areas

---

## 🗺️ Supported Geographic Levels

| Geographic Level                    | Description                                                                 | Available In |
|-------------------------------------|-----------------------------------------------------------------------------|--------------|
| **Nation**                          | Entire United States                                                        | 1-Year, 5-Year |
| **State**                           | Individual U.S. states                                                      | 1-Year, 5-Year |
| **County**                          | Counties within states                                                      | 1-Year, 5-Year |
| **County Subdivision**             | Minor civil divisions (e.g., townships)                                     | 5-Year only |
| **Place**                           | Incorporated places (cities, towns)                                         | 1-Year, 5-Year |
| **ZIP Code Tabulation Area (ZCTA)** | Approximated ZIP Code boundaries                                            | 5-Year only |
| **Metropolitan/Micropolitan Area**  | Census-defined metro or micro areas                                         | 1-Year, 5-Year |
| **Census Tract**                    | Small subdivisions of counties (~4,000 residents)                           | 5-Year only |
| **Block Group**                     | Subdivisions of tracts (~600–3,000 residents)                               | 5-Year only |
| **Block**                           | The smallest geography (~40–100 people)                                     | 5-Year only |

---

## ⚙️ What Can You Do with homestock?

- 🧩 **Pull specific ACS tables** by table ID (e.g., `B19013` for median household income)
- 📁 **Convert results** to `pandas` DataFrames or export them as `.csv`
- 🌐 **Query different geographic levels**, from national down to individual blocks
- 🔍 **Explore metadata** dynamically using Census variable labels
- 🗺️ **Use results in mapping tools** like `folium`, `geopandas`, or `leafmap`

---

## 📦 Install

```bash
pip install homestock



