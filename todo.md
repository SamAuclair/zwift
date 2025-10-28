# Zwift Cycling Data Analysis Project - TODO

## Project Description

This project is a comprehensive data science portfolio piece that demonstrates end-to-end data engineering and analytics capabilities using Zwift cycling application data. The goal is to store, process, and analyze personal training data from Zwift to create meaningful insights and visualizations.

The project showcases:
- ETL pipeline development (Python)
- Cloud data storage and processing (Google Cloud Platform, BigQuery)
- Data transformation and modeling (DBT)
- Interactive dashboard development (Streamlit)
- Data visualization (Plotly)

**Data Architecture**: Raw .fit files → Google Drive backup → BigQuery → DBT transformations → Streamlit Dashboard

**Key Tables**:
- `training`: Core training session metadata
- `augmented_data`: Detailed time-series data with calculated fields
- `zone`: Heart rate/power zone definitions for training analysis

## Current Status

**Phase**: Dashboard Development
**Next Task**: Styling

## Todo 📋

### 6. Styling
- [ ] 


### 7. Dashboard Enhancement & Polish
- [ ] Add loading states and error handling
- [ ] Implement data refresh mechanisms
- [ ] Add tooltips and help text for metrics
- [ ] Optimize query performance
- [ ] Add data quality indicators
- [ ] Implement responsive design for mobile devices

*Commit: "feat: enhance dashboard with improved UX, error handling, and responsive design"*


### 8. Documentation & Portfolio Integration
- [ ] Create comprehensive README.md
- [ ] Document data architecture and pipeline
- [ ] Add screenshots and demo video
- [ ] Write technical blog post about the project
- [ ] Update portfolio website with project showcase

*Commit: "docs: complete project documentation and portfolio integration"*

### Nice to haves. Future Enhancements (Optional)
- [ ] Implement comparative analysis with previous periods


## Completed ✅

### 5. Training Session Detail Dashboard (Page 2)
- [x] Create training session detail page layout
- [x] Implement date picker filter (only dates with existing training sessions)
- [x] Set default filter to latest training date
- [x] Create session-specific metric cards (max/avg from augmented_data):
  - [x] Session heart rate statistics
  - [x] Session cadence statistics
  - [x] Session power statistics
  - [x] Session speed statistics
- [x] Implement Plotly line chart for time-series data:
  - [x] Power curve over time
  - [x] Cadence curve over time
  - [x] Dual y-axis configuration
  - [x] Interactive zoom and hover features
- [x] Additional time-series charts for heart rate and speed

*Commit: "feat: implement training session detail page with metrics and time-series visualization"*

### 4. Global Metrics Dashboard (Page 1)
- [x] Create main metrics page layout
- [x] Implement year filter (default: "all years") - dynamically loads years from data
- [x] Create score cards for global training metrics:
  - [x] Total training sessions (count distinct dates from training table)
  - [x] Total distance (sum distance_km from training table)
  - [x] Average distance per session
  - [x] Average duration per session (HH:MM:SS format)
- [x] Create score cards for performance metrics (max/avg from augmented_data):
  - [x] Heart rate statistics (max/avg)
  - [x] Cadence statistics (max/avg)
  - [x] Power statistics (max/avg)
  - [x] Speed statistics (max/avg)
- [x] Implement cardio zone time distribution analysis (using zone table with bar chart visualization)
- [x] Apply responsive grid layout for score cards (4-column layout)
- [x] Add data caching with @st.cache_data decorator (TTL: 10 minutes)
- [x] Implement error handling for missing data

*Commit: "feat: implement global metrics dashboard with training statistics and performance metrics"*

### 3. Dashboard Infrastructure Setup
- [x] Set up Streamlit application structure
- [x] Configure BigQuery connection for Streamlit
- [x] Implement dark theme configuration
- [x] Set up multi-page navigation structure

*Commit: "feat: initialize Streamlit dashboard with BigQuery connection and dark theme"*

### 2. Data Transformation & Modeling
- [x] Build DBT models to create augmented tables in BigQuery
- [x] Build DBT models to create aggregated tables in BigQuery
- [x] Establish data architecture with training, augmented_data, and zone tables

### 1. Data Collection & Backup Infrastructure
- [x] Backup .fit files to Google Drive
- [x] Parse .fit files and extract relevant training data
- [x] Upload processed data to BigQuery


## Technical Notes

**Dependencies**:
- streamlit
- plotly
- pandas
- google-cloud-bigquery
- python-dotenv

**BigQuery Connection**: Ensure service account credentials are properly configured for Streamlit cloud deployment.

**Performance Considerations**: 
- Implement query caching for frequently accessed aggregations
- Consider materialized views for complex calculations
- Use Streamlit's caching mechanisms (@st.cache_data)
