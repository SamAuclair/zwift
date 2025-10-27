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
**Next Task**: Implement global metrics dashboard with training statistics and performance metrics

## Todo 📋

### 4. Global Metrics Dashboard (Page 1)
- [ ] Create main metrics page layout
- [ ] Implement year filter (default: "all years")
- [ ] Create score cards for global training metrics:
  - [ ] Total training sessions (count distinct dates from augmented_data)
  - [ ] Total distance (sum distance_km from training table)
  - [ ] Average distance per session
  - [ ] Average duration per session (HH:MM:SS format)
- [ ] Create score cards for performance metrics (max/avg from augmented_data):
  - [ ] Heart rate statistics
  - [ ] Cadence statistics  
  - [ ] Power statistics
  - [ ] Speed statistics
- [ ] Implement cardio zone time distribution analysis (using zone table)
- [ ] Apply responsive grid layout for score cards

*Commit: "feat: implement global metrics dashboard with training statistics and performance metrics"*

### 5. Training Session Detail Dashboard (Page 2)
- [ ] Create training session detail page layout
- [ ] Implement date picker filter (only dates with existing training sessions)
- [ ] Set default filter to latest training date
- [ ] Create session-specific metric cards (max/avg from augmented_data):
  - [ ] Session heart rate statistics
  - [ ] Session cadence statistics
  - [ ] Session power statistics
  - [ ] Session speed statistics
- [ ] Implement Plotly line chart for time-series data:
  - [ ] Power curve over time
  - [ ] Cadence curve over time
  - [ ] Dual y-axis configuration
  - [ ] Interactive zoom and hover features

*Commit: "feat: implement training session detail page with metrics and time-series visualization"*

### 6. Dashboard Enhancement & Polish
- [ ] Add loading states and error handling
- [ ] Implement data refresh mechanisms
- [ ] Add tooltips and help text for metrics
- [ ] Optimize query performance
- [ ] Add data quality indicators
- [ ] Implement responsive design for mobile devices

*Commit: "feat: enhance dashboard with improved UX, error handling, and responsive design"*

### 7. Deployment & Production Setup
- [ ] Create Dockerfile for Streamlit application
- [ ] Set up Google Cloud Run configuration
- [ ] Configure environment variables and secrets management
- [ ] Set up CI/CD pipeline for automated deployment
- [ ] Configure custom domain and SSL (optional)
- [ ] Implement monitoring and logging

*Commit: "feat: deploy Streamlit dashboard to Google Cloud Run with CI/CD pipeline"*

### 8. Documentation & Portfolio Integration
- [ ] Create comprehensive README.md
- [ ] Document data architecture and pipeline
- [ ] Add screenshots and demo video
- [ ] Write technical blog post about the project
- [ ] Update portfolio website with project showcase

*Commit: "docs: complete project documentation and portfolio integration"*

### 9. Future Enhancements (Optional)
- [ ] Add training plan recommendations
- [ ] Implement comparative analysis with previous periods
- [ ] Add goal tracking and progress monitoring
- [ ] Integrate weather data correlation
- [ ] Add social features for training buddies comparison
- [ ] Implement machine learning models for performance prediction

*Commit: "feat: implement advanced analytics and ML features for training insights"*

## Completed ✅

### 1. Data Collection & Backup Infrastructure
- [x] Backup .fit files to Google Drive
- [x] Parse .fit files and extract relevant training data
- [x] Upload processed data to BigQuery

### 2. Data Transformation & Modeling
- [x] Build DBT models to create augmented tables in BigQuery
- [x] Build DBT models to create aggregated tables in BigQuery
- [x] Establish data architecture with training, augmented_data, and zone tables

### 3. Dashboard Infrastructure Setup
- [x] Set up Streamlit application structure
- [x] Configure BigQuery connection for Streamlit
- [x] Implement dark theme configuration
- [x] Set up multi-page navigation structure

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
