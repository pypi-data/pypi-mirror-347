# 🧠 data-science-snippets

**data-science-snippets** is a modular, production-ready Python snippets  containing curated, reusable utilities used in the day-to-day workflows of senior data scientists and machine learning engineers.

It includes tools for EDA, cleaning, validation, text processing, feature engineering, visualization, model evaluation, time series, and more — organized by task to keep your work clean and efficient.

---

## 🚀 Features

✅ Covers every major step in the data science lifecycle  
✅ Clean, modular structure by task  
✅ Built for reusability in real-world projects  
✅ Lightweight: only depends on `pandas`, `numpy`, `matplotlib`, `seaborn` by default  
✅ Compatible with Python 3.9+

---

## 📁 Folder Structure

```
data-science-snippets/
├── eda/
│   ├── most_frequent_values.py
│   ├── data_summary.py
│   ├── cardinality_report.py
│   └── basic_statistics.py
├── data_cleaning/
│   ├── missing_data_summary.py
│   ├── outlier_detection.py
│   └── duplicate_removal.py
├── preprocessing/
│   ├── minmax_scaling.py
│   ├── encoding.py
│   └── normalize_columns.py
├── loading/
│   ├── load_csv_with_info.py
│   ├── safe_parquet_loader.py
│   └── load_large_file_chunks.py
├── visualization/
│   ├── missing_data_heatmap.py
│   ├── distribution_plot.py
│   └── correlation_matrix.py
│   └── color_palette_utils.py
├── feature_engineering/
│   ├── create_datetime_features.py
│   ├── binning.py
│   ├── interaction_terms.py
│   └── rare_label_encoding.py
├── automated_eda/
│   ├── quick_eda_report.py
│   └── profile_report_wrapper.py
├── model_evaluation/
│   ├── classification_report_extended.py
│   ├── confusion_matrix_plot.py
│   ├── cross_validation_metrics.py
│   └── roc_auc_plot.py
├── text_processing/
│   ├── clean_text.py
│   ├── tokenize_text.py
│   └── tfidf_features.py
├── time_series/
│   ├── lag_features.py
│   ├── rolling_statistics.py
│   └── datetime_indexing.py
├── modeling/
│   ├── model_training.py
│   ├── pipeline_builder.py
│   └── hyperparameter_tuner.py
├── data_validation/
│   ├── schema_check.py
│   ├── unique_constraints.py
│   └── value_range_check.py
├── utils/
│   ├── memory_optimization.py
│   ├── execution_timer.py
│   └── logging_setup.py
└── README.md
```

---

## 🔹 `eda/` – Exploratory Data Analysis

- `most_frequent_values.py`: Shows the most common (modal) value per column, its frequency, and percent from non-null values.
- `data_summary.py`: Summarizes dtypes, nulls, uniques, and memory usage for quick inspection.
- `cardinality_report.py`: Reports high-cardinality columns in categorical features.
- `basic_statistics.py`: Returns mean, median, min, max, std, and other summary statistics.

---

## 🔹 `data_cleaning/`

- `missing_data_summary.py`: Shows missing value count and percentage per column, along with data types.
- `outlier_detection.py`: Detects outliers using IQR or Z-score methods.
- `duplicate_removal.py`: Identifies and removes duplicate rows or records.

---

## 🔹 `preprocessing/`

- `minmax_scaling.py`: Scales numeric values to a [0, 1] range.
- `encoding.py`: Label encoding and one-hot encoding utilities.
- `normalize_columns.py`: Z-score standardization and column normalization helpers.

---

## 🔹 `loading/`

- `load_csv_with_info.py`: Loads CSVs and prints metadata like shape, dtypes, and missing values.
- `safe_parquet_loader.py`: Robust parquet file loader with fallback options.
- `load_large_file_chunks.py`: Loads large files in chunks with progress reporting.

---

## 🔹 `visualization/`

- `missing_data_heatmap.py`: Visualizes missing values with a Seaborn heatmap.
- `distribution_plot.py`: Plots distributions of numeric variables.
- `correlation_matrix.py`: Draws a correlation heatmap of numeric features.

---

## 🔹 `feature_engineering/`

- `create_datetime_features.py`: Extracts features like day, month, year, weekday from datetime columns.
- `binning.py`: Performs binning (equal-width or quantile) on continuous variables.
- `interaction_terms.py`: Creates interaction features (e.g., feature1 * feature2).
- `rare_label_encoding.py`: Groups rare categorical labels into 'Other'.

---

## 🔹 `automated_eda/`

- `quick_eda_report.py`: Generates a summary of shape, dtypes, nulls, basic stats.
- `profile_report_wrapper.py`: Wrapper for pandas-profiling / ydata-profiling report generation.

---

## 🔹 `model_evaluation/`

- `classification_report_extended.py`: Displays precision, recall, F1 with support for multiple averages.
- `confusion_matrix_plot.py`: Annotated confusion matrix visual.
- `cross_validation_metrics.py`: Computes metrics across folds and aggregates results.
- `roc_auc_plot.py`: Plots ROC curve and calculates AUC score.

---

## 🔹 `text_processing/`

- `clean_text.py`: Removes punctuation, stopwords, numbers, and lowercases text.
- `tokenize_text.py`: Word and sentence tokenizers with NLTK or spaCy support.
- `tfidf_features.py`: Builds TF-IDF matrix from text columns.

---

## 🔹 `time_series/`

- `lag_features.py`: Generates lagged versions of a column for time-aware modeling.
- `rolling_statistics.py`: Rolling mean, median, std, and min/max features.
- `datetime_indexing.py`: Time-based slicing, filtering, and resampling helpers.

---

## 🔹 `modeling/`

- `model_training.py`: Trains scikit-learn models with optional cross-validation and logging.
- `pipeline_builder.py`: Builds preprocessing + modeling pipelines using `Pipeline` or `ColumnTransformer`.
- `hyperparameter_tuner.py`: Wraps `GridSearchCV` or `RandomizedSearchCV` with easy setup and evaluation.

---

## 🔹 `data_validation/`

- `schema_check.py`: Validates schema based on expected dtypes and column names.
- `unique_constraints.py`: Ensures unique values for IDs or compound keys.
- `value_range_check.py`: Checks for valid value ranges in numeric columns.

---

## 🔹 `utils/`

- `memory_optimization.py`: Downcasts numerical columns to save memory.
- `execution_timer.py`: Times function execution with decorators or context managers.
- `logging_setup.py`: Sets up consistent logging configuration for larger projects.

---

## 🛠️ Usage

```python
Copy-Paste 📦
```

---

## 📚 Requirements

- Python ≥ 3.9  
- pandas ≥ 1.5.3  
- numpy ≥ 1.24.4  
- seaborn ≥ 0.12.2
- matplotlib ≥ 3.6.3

---
## 🔐 Security

Please see our [SECURITY.md](.github/SECURITY.md) for vulnerability disclosure guidelines.

---

## 👥 Authors

- **Vataselu Andrei**  
- **Nicola-Diana Sincaru**

---

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## 🌟 Contributions

We welcome contributions! If you have a reusable function or snippet that you think belongs in a senior data scientist’s toolkit, feel free to open a pull request.