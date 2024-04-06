# OlympicPulse | Harnessing Olympics Insights
OlympicPulse is a Streamlit web application designed for the analysis of Summer Olympics dataset. It provides users with interactive visualizations and insights derived from the dataset, allowing them to explore historical Olympic data in an intuitive manner


# Dataset
The dataset used in this project is sourced from Kaggle. It contains comprehensive information about athletes, events, and results spanning 120 years of Olympic history.

Dataset Link: https://www.kaggle.com/datasets/heesoo37/120-years-of-olympic-history-athletes-and-results

# Installation
To run the OlympicPulse application locally, follow these steps:

1. Clone the repository to your local machine:

       git clone https://github.com/singhsuryanshofficial/OlympicPulse-Harnessing-Olympic-Insights.git

2. Navigate to the project directory:

       cd OlympicPulse

3. Install the required libraries using pip:

       pip install -r requirements.txt
   
# Usage
To run the OlympicPulse application, execute the following command in your terminal:

    streamlit run OlympicPulse.py

Access the application through your web browser at the provided local address. Choose from various analysis options available in the sidebar menu.

# Files
**1. OlympicPulse.py** :  Main code file containing the Streamlit web application.

**2. preprocessor.py** : Python script for preprocessing the dataset, filtering for summer Olympics, and adding necessary columns.

**3. helper.py** : Contains utility functions used in the project for data analysis and visualization.

# Libraries Used
**1. Streamlit**: Used for building interactive web applications with Python.

**2. Plotly**: Provides interactive and publication-quality plots.

**3. Seaborn**: Data visualization library based on Matplotlib, offers a high-level interface for drawing attractive statistical graphics.

**4. Matplotlib**: Comprehensive library for creating static, animated, and interactive visualizations in Python.

**5. Pandas**: Data manipulation and analysis library, providing data structures and functions for working with structured data.

**6. NumPy**: Library for numerical computing in Python.

# Features
Medal Tally: View medal tallies for different countries in various Olympic editions.

Overall Analysis: Explore top statistics, participating nations, events, and athletes over time.

Country-wise Analysis: Analyze medal tallies and performance trends for specific countries.

Athlete-wise Analysis: Investigate age distribution, height vs. weight, and participation trends for athletes.

# Contributors
Suryansh Singh

# License
This project is licensed under the [MIT License](LICENSE).

