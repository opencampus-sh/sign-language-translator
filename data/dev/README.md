## Data Processing Tools

### Training Data Creation

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/opencampus-sh/sign-language-translator/blob/main/data/dev/create_training_data.ipynb)

This notebook provides utilities for creating and managing training data in Google Cloud Storage:

- Save pandas DataFrames as parquet files with configurable row group sizes
- Efficiently store data in the project's bucket structure
- List and read files from the storage buckets
- Includes authentication and setup for Google Cloud access

Example usage:

```python
# Save DataFrame to bucket
save_parquet_to_bucket(
df=your_dataframe,
project_id="your-project-id",
destination_path="raw-data/my_data.parquet",
row_group_size=750
)
```
