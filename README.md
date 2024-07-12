# Facebook Data Analysis Dashboard

This Streamlit application allows users to perform exploratory data analysis (EDA) on a Facebook dataset. The application includes data pre-processing, feature engineering, and interactive visualizations. 

## Features

1. **Data Pre-processing and Feature Engineering:**
   - Handles missing values in the `gender` and `tenure` columns.
   - Creates a new `dob` (date of birth) column by combining `dob_year`, `dob_month`, and `dob_day`.
   - Adds new features: `engagement_rate` and `click_through_rate`.

2. **Data Analysis and Exploration:**
   - Filters data based on user-specified date range, gender, and age range.
   - Displays bar charts and histograms for various metrics.
   - Provides downloadable CSV files of the filtered data.

3. **Interactive Data Visualization:**
   - Bar chart of friend count by gender.
   - Histogram of age distribution.
   - Line chart showing time series analysis of friend count.
   - Treemap showing hierarchical view of friend count by gender and age.
   - Histograms for engagement rate and click-through rate distributions.
   - Scatter plot showing the relationship between likes and likes received.
   - Summary tables with downloadable CSV options.

## Requirements

- Python 3.6 or later
- Streamlit
- Plotly
- Pandas

## How to Run

1. Clone this repository to your local machine.
2. Ensure all dependencies are installed:
    pip install streamlit plotly pandas
3. Run the Streamlit application:
    streamlit run dashboard.py --server.port 8888

## File Description

- `dashboard.py`: The main Streamlit application file.
- `pseudo_facebook.csv`: Example CSV dataset for testing (included in the repository).

## Detailed Code Explanation

### Data Pre-processing and Feature Engineering
The code handles missing values in `gender` and `tenure`, creates a new `dob` column, and computes `engagement_rate` and `click_through_rate`.

### Data Filtering
Users can filter the data based on date range, gender, and age range. The filtered data is then used for visualizations.

### Visualizations
- **Bar Chart**: Gender-wise friend count.
- **Histogram**: Age distribution.
- **Line Chart**: Time series analysis of friend count.
- **Treemap**: Hierarchical view of friend count by gender and age.
- **Histograms**: Engagement rate and click-through rate distributions.
- **Scatter Plot**: Relationship between likes and likes received.
- **Summary Tables**: Summary of various metrics with options to download the data as CSV files.

### Download Options
Users can download the filtered dataset and the summary tables as CSV files.

## Notes

- Ensure the uploaded dataset has columns `dob_year`, `dob_month`, `dob_day`, `gender`, `tenure`, `age`, `friend_count`, `likes`, `likes_received`, `mobile_likes`, `dob`.
- The date range filter applies to the `dob` column.

## Contact
For any questions or issues, please contact Fateh Muhammad at fateh.m0101@gmail.com.

