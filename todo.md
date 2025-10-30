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

**Section**: 6. Styling
**Next Task**: UX Enhancement & Polish

## Todo 📋

### 7. UX Enhancement & Polish
- [x] Add a "selected_year" variable to this line: st.title("📊 Zwift Training Statistics for: {selected_year}") to print the current value of the global page filter.
- [x] Add the selected_date at the end of the title of page 2. (e.g. Training Details (2025-10-23))
- [x] Add Cardio zones in the "Training Details" page. This should be exactly like the 5 zone cards in "Overview" with the exception that it is filter for a the selected date.
- [ ] Remove the first "dashboard" page. Make the default page: "Overview" without changing the name to "dashboard".
- [ ] Add tooltips and help text for metrics
- [ ] Add loading states
- [ ] Implement data refresh mechanisms
- [ ] Optimize query performance
- [ ] Add data quality indicators
- [ ] Implement responsive design for mobile devices

*Commit: "feat: enhance dashboard with improved UX, error handling, and responsive design"*

### 8. Styling - Polishing Colors
- [] 

*Commit: "style: Change design colors"*

### 9. Documentation & Portfolio Integration
- [ ] Create comprehensive README.md
- [ ] Document data architecture and pipeline
- [ ] Add screenshots and demo video
- [ ] Write technical blog post about the project
- [ ] Update portfolio website with project showcase

*Commit: "docs: complete project documentation and portfolio integration"*

### Nice to haves. Future Enhancements (Optional)
- [ ] Implement comparative analysis with previous periods

## Completed ✅

### 6. Styling
- [x] Create card styling for all metrics on both pages (rectangular with rounded edges, matching nav bar theme)
- [x] Round all distance units (km, km/h) to 1 decimal place in metrics and chart tooltips
- [x] Global page modifications:
  - [x] Replace zone bar chart with 5 individual zone cards (keeping green to red color scheme)
  - [x] Remove zone details table
- [x] Training session page modifications:
  - [x] Replace "heart rate over time" chart with "cadence over time" chart
  - [x] Remove "value" as y-axis title from "power and heart rate over time" chart
  - [x] Make power line blue in the power/heart rate chart
  - [x] Make speed line blue in the speed over time chart
- [x] Remove space before "Global Training Metrics" title. If possible, remove the header that contains the "Deploy" button
- [x] Reduce the top margin for .stMainBlockContainer class.
- [x] Center the text for all card title. After Last iteration they were still left aligned.
- [x] Add a zwift logo at the top of the nav bar. the image is in "src/assets"
- [x] Move the zwift logo to be above the page navigation element.
- [x] Change the text in the left nav bar. "dashboard" -> "Overview". This change didn't work in previous iteration.
- [x] Center the text of the title that is found inside each cards.
- [x] On the second page, reduce the spacing between the "Training Details" title and the chart below by reducing the top margin of the chart element.
- [x] On the second page, modify the chart to reduce spacing between the top of the top-most visual element and the top of the svg element produced by plotly. Try achieving this by adding/modifying a plotly property in "02_Training_Details.py" (line 202-235). Fetch the plotly doc if unsure how to proceed.
- [x] Reduce the padding-top and padding-bottom of the stMainBlockContainer to 10.
- [x] Set a max width for the cards. They get to large when given the chance.
- [x] remove the tool icons that hover in the top right corner for the plotly chart. This can be achieved by adding/modifying a plotly property in "02_Training_Details.py". Fetch the plotly doc if unsure how to proceed.
- [x] Center the title in the card and remove some padding-top. Careful, I am not talking about the h3 element that has a h3 "text-align: left" property. leave that one as is. I want the title such as "Total Training Sessions" and "Max Heart Rate ❤️" to be centered.
- [x] Increase the font size of the title in the card.

*Commit: "style: implement card design, improve chart styling, modify texts, and enhance visual consistency"*

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

**Useful Commands**
- poetry run streamlit run src/dashboard.py