# DS_International-Debt-Analysis
International Debt Analysis System Using Python, SQL, and Visualization Tools




Problem Statement:
Global financial institutions and organizations such as the World Bank generate vast amounts of data related to international debt, including country-wise borrowings, repayments, interest payments, and other financial indicators. However, this data is often stored in raw and complex formats such as CSV files with multiple indicators, making it difficult to analyze, interpret, and extract meaningful insights.
The challenge lies in transforming this raw financial data into a structured and usable format by performing data cleaning, preprocessing, and exploratory data analysis (EDA). Ensuring data quality, handling missing values, and organizing the data efficiently are critical steps before performing any meaningful analysis.

This project aims to build a complete end-to-end data analytics pipeline that enables candidates to:
Clean and preprocess international debt data using Python
Perform exploratory data analysis (EDA) to identify key trends and patterns
Store processed data in a structured SQL database
Write SQL queries to extract meaningful insights
Develop interactive dashboards using Streamlit (Plotly / Seaborn / Matplotlib) or Power BI for data visualization and reporting
Objective:
The objective of this project is to design and implement an International Debt Analytics System that follows the complete data lifecycle:
Data Collection
Data Cleaning & Preprocessing
Exploratory Data Analysis (EDA)
Data Storage (SQL)
Data Visualization (Power BI / Streamlit)

Approach:
1. Data Collection
Import the dataset in CSV format
Load the dataset into Python using Pandas DataFrame
Understand the structure, columns, and data types

2. Data Preprocessing
Handle missing values (null data)
Remove duplicate records
Perform data type conversion
Filter relevant columns (country, indicators, debt values)
Standardize and clean the dataset

3. Exploratory Data Analysis (EDA)
Analyze country-wise debt distribution
Identify top countries with highest and lowest debt
Explore different debt indicators and their impact
Identify patterns, trends, and relationships
Perform statistical summaries and comparisons

4. Database Design & SQL Integration
Design relational tables (Countries, Indicators, Debt Data)
Create database using MySQL
Insert cleaned data into SQL tables
Write SQL queries for analysis
Apply primary keys and foreign key relationships

5. Data Visualization
Connect SQL database to:
Power BI or
Streamlit application
Create dashboards using:
Plotly / Seaborn / Matplotlib
Build visual insights for country-wise and indicator-wise debt analysis

6. Insights & Reporting
Generate insights on: 
Country-wise debt distribution
Top countries with highest and lowest debt
Debt distribution across different indicators
Trends and patterns in international debt
Support data-driven decision making

Dataset Link: International Debt Statistics Jan 2022 - Dataset

📊 SQL Analytical Questions (30)
🔹 Basic Queries
Retrieve all distinct country names from the dataset.
Count the total number of countries available.
Find the total number of indicators present.
Display the first 10 records of the dataset.
Calculate the total global debt.
List all unique indicator names.
Find the number of records for each country.
Display all records where debt is greater than 1 billion USD.
Find the minimum, maximum, and average debt values.
Count total number of records in the dataset.

🔹 Intermediate Level
Find the total debt for each country.
Display the top 10 countries with the highest total debt.
Find the average debt per country.
Calculate total debt for each indicator.
Identify the indicator contributing the highest total debt.
Find the country with the lowest total debt.
Calculate total debt for each country and indicator combination.
Count how many indicators each country has.
Display countries whose total debt is above the global average.
Rank countries based on total debt (highest to lowest).




🔹 Advanced Level
Find the top 5 indicators contributing most to global debt.
Calculate percentage contribution of each country to total global debt.
Identify the top 3 countries for each indicator based on debt.
Find the difference between maximum and minimum debt for each country.
Create a view for the top 10 countries with highest debt.
Categorize countries into:
High Debt
Medium Debt
Low Debt (based on thresholds)
Use window functions to calculate cumulative debt per country.
Find indicators where average debt is higher than overall average debt.
Identify countries contributing more than 5% of global debt.
Find the most dominant indicator (highest contribution) for each country.

Results:
Structured relational database for international debt data
Clean and preprocessed dataset (handled missing values & duplicates)
Successful CSV to DataFrame conversion
Integrated Python with MySQL database
Effective country-wise debt analysis
Interactive dashboard using Streamlit / Power BI
Insightful data visualization (Plotly / Seaborn / Matplotlib)
Identification of top and least indebted countries
Indicator-wise and country-wise debt insights
End-to-end data analytics pipeline implementation
Project Evaluation metrics:
Proper data preprocessing (handling missing values & duplicates)
Accurate CSV to DataFrame conversion
Effective Exploratory Data Analysis (EDA)
Correct database design & normalization
Proper implementation of table relationships (Primary Key & Foreign Key)
SQL query optimization and performance
Effective use of joins and aggregations
Data integration (Python to MySQL)
Visualization quality and clarity (Plotly / Seaborn / Matplotlib)
Dashboard functionality (Streamlit / Power BI)
Clean and well-structured Python code
Insight generation and interpretation

