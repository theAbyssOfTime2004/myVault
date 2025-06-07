2025-06-07 13:27


Tags:

# Data_Mining_Lab9_Report

## 1. Tải và khám phá dữ liệu
- Sử dụng thư viện `ucimlrepo` để tải bộ dữ liệu Banknote Authentication từ UCI Machine Learning Repository:

  

```python

from ucimlrepo import fetch_ucirepo

# fetch dataset

banknote_authentication = fetch_ucirepo(id=267)

# data (as pandas dataframes)

X = banknote_authentication.data.features

y = banknote_authentication.data.targets

# metadata

print(banknote_authentication.metadata)

# variable information

print(banknote_authentication.variables)

# References
