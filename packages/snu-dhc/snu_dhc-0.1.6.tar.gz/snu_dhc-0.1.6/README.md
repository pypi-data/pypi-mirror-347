# SNU-DHC

## Description
`DemoTable` generates baseline characteristic tables for medical studies and exports them to Excel.
It supports continuous and categorical variables, grouping, and automatic p-value calculation.

### Parameters:

- `df`: Input pandas DataFrame.
- `table_name`: Title for the Excel sheet.
- `variables`: List of dictionaries defining the variables to display.
- `group_variable`: Optional column to group comparisons.
- `group_labels`: Display labels for group values.
- `show_total`: Whether to show the total column.
- `show_missing`: Whether to show missing counts for categorical variables.
- `percent_decimals`: Decimal places for percentages.
- `thousands_sep`: Use comma separator for each thousand numbers.
- `show_p_values`: Whether to include a p-value column.
- `p_value_decimals`: Fixed or automatic formatting for p-values.

### Test selection logic (for p-values):
- **Continuous (mean)**:
  - 2 groups: Welch's t-test (with checks and warnings for normality)
  - 3+ groups: ANOVA (with checks and warnings for normality and variance)
- **Continuous (median)**:
  - 2 groups: Mann-Whitney U test
  - 3+ groups: Kruskal-Wallis test
- **Categorical**:
  - Chi-square test by default
  - Fisher's exact test if 2x2 and <5 cell counts

## Usage Example
```python
from snu_dhc.tables import DemoTable

variables_config = [
    {"var": "age", "name": "Age", "type": "continuous", "stat": "median", "decimals": 0},
    {"var": "sex", "name": "Sex", "type": "categorical", "class_labels": {1: "Male", 0: "Female"}},
    {"var": "dm", "name": "Diabetes mellitus", "type": "categorical", "class_labels": {1: ""}},
    {"var": "init_rhythm", "name": "Initial rhythm", "type": "categorical", "class_labels": {1: "VF/VT", 2: "PEA", 3: "Asystole"}},
    {"var": "rti", "name": "RTI", "type": "continuous", "stat": "median", "decimals": 0},
]

table = DemoTable(
    df=ohca_group,
    table_name="Table 1. Baseline characteristics of study patients",
    variables=variables_config,
    group_variable="group",
    group_labels={"train": "Train", "val": "Validation", "test": "Test"}, 
    show_total=True,
    show_missing=True,
    percent_decimals=1,
    thousands_sep=True,
    show_p_values=True,
    p_value_decimals="auto"
)

table.save("table1.xlsx")
```

## snu_dhc.statistics
This module includes tools to evaluate binary classifiers with confidence intervals and visualization utilities.

### `binary_outcome_analysis(true, **probs)`
- `true`: Array-like of true binary labels.
- `**probs`: Dictionary of model names and their predicted probabilities.
**Methods:**
  - `.auc()`: Print AUC and 95% CI for each model.
  - `.roc_auc(**styles)`: Plot ROC curves and display AUC values. Customize plot style per model.
  - `.classification(**cutoffs)`: Print classification metrics using thresholds like fixed float, 'youden', 'sen90', 'spe80', etc.



## Example: `binary_outcome_analysis`
```python
from snu_dhc.statistics.utils import binary_outcome_analysis

probs = {
    'XGBoost': prob0,
    'Random Forest': prob1,
    'Logistic Regression': prob2
}
result = binary_outcome_analysis(true, **probs)

# Plot ROC curves
styles = {
    'XGBoost': {'color': 'C0', 'linestyle': '-'},
    'Random Forest': {'color': 'C1', 'linestyle': '-.'},
    'Logistic Regression': {'color': 'C2', 'linestyle': '--'}
}
result.roc_auc(**styles)

# Show classification metrics with thresholds
cutoffs = {
    'XGBoost': 0.5,
    'Random Forest': 'sen90',
    'Logistic Regression': 'spe80'
}
result.classification(**cutoffs)
```
### `auc_score(true, prob, method='delong', alpha=0.95, n_iterations=1000, show=False)`
- Get AUC and 95% CI using either DeLong's method or bootstrap.
**Returns:** `[auc, [ci_lower, ci_upper]]`

### `classification_metrics(true, pred, method='wilson', ...)`
- Returns sensitivity, specificity, PPV, NPV, and F1-score with confidence intervals.
**Returns:** Dictionary like `{'sen': [...], 'spe': [...], 'ppv': [...], 'npv': [...], 'f1': [...]}`

### `youden_metrics(true, prob, ...)`
- Computes metrics using Youden's index as the threshold.
**Returns:** `(metrics_dict, youden_threshold)`

### `bootstrap_ci(true, pred, fx, n_iterations=1000, alpha=0.95)`
- Computes confidence interval for any function `fx` using bootstrap.
**Returns:** `[estimate, [ci_lower, ci_upper]]`

### `overview_df(df)`
- Provides column-wise overview of a DataFrame.
**Returns:** DataFrame with columns for dtype, #unique, #missing, #zeros, etc.

### `AUC_CI_Delong(y_true, y_pred, alpha=0.95)`
- Calculates AUC and CI using DeLong's method.
**Returns:** `[auc, [ci_lower, ci_upper]]`

### `Classification_CI_Wilson(TP, FP, FN, TN, alpha=0.95)`
- Computes CI for sensitivity, specificity, PPV, NPV using Wilson's method.
**Returns:** Dictionary like `{'sen': [...], 'spe': [...], 'ppv': [...], 'npv': [...]}`

