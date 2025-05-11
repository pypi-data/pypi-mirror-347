# Advanced Dataframe Statistics Library

A library for advanced DataFrame statistics analysis, returns:

=========================== df_name ============================

##### Leading Zeros in Columns

| col1         | col2 |
|--------------|------|
| 0000000000   | 0D2  |
| 0000001999   | 0D4  |
| 0000006669   | 0D1  |

##### General Stats

| Columns   | DTypes         | NaNs | Unique | Duplicates | Totals  | Min  | Max   | Mean  | Median | STD   | STD(%) | Outliers |
|-----------|----------------|------|--------|------------|---------|------|-------|-------|--------|-------|--------|----------|
| col_1     | `str`          | 0    | 5000   | 0          | -       | -    | -     | -     | -      | -     | -      | -        |
| col_3     | `str, NoneType`| 1254 | 9      | 4991       | -       | -    | -     | -     | -      | -     | -      | -        |
| col_5     | `float`        | 0    | 74     | 116        | 863.66  | -66  | 79.36 | 172.73| 23.08  | 1.62  | 938.89 | 613.00   |



## Installation

You can install the library using pip:

```bash
pip install stat-df 
```

## Importing the Library
```python
import stat_df as sd
```
## Usage
```python
sd.show(my_df) 
```
This command will print out "Leading Zeros in Columns" and "General Stats" data in a nice unified table.

