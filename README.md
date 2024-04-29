# Jacci- Academic Individual and Group Projects
This is a file that cover all the projects that I have done during my Master of Applied Data Science at University of Canterbury.

## Individual Project
### Project 1: Crime Data Analysis and Visualisation

#### Description

This project analyzes crime data in New Zealand to identify trends and relationships.

#### Key Features

- Preprocessed and analyzed 25,000 rows of crime data using Python (Pandas).
- Identified primary crime types and explored correlations between crime types, age, and ethnicity.
- Developed informative data visualizations using Matplotlib to communicate findings effectively.
- Created an interactive data visualization interface using Tkinter for exploring crime trends and demographics.

#### Tech Stack

Python
- Pandas
- Matplotlib
- Tkinter


### Project 2: GHCN Data Analysis using Spark
#### Description

This project explores the analysis of climate data using Apache Spark, a distributed computing framework. The dataset comprises daily climate summaries and metadata spanning a remarkable 262 years, accumulating to a substantial 103.5 GB of storage.

#### Key Features:

- Large-Scale Data Processing: The project tackles a massive dataset, efficiently handling data loading, cleaning, transformations, and analysis using Spark's distributed processing capabilities.
- In-Depth Data Exploration: It delves into various aspects of the climate data, including station analysis (total stations, active stations, network participation), distance calculations between stations, and comprehensive exploration of daily observations.
- Data Management Strategies: The project demonstrates effective strategies for managing large datasets in Spark, including broadcast joins to minimize data shuffling, data reuse for efficient analysis, and caching for faster processing.
- Climate Analysis: It performs in-depth climate analysis, such as calculating average annual rainfall by country and year, identifying potential outliers, and visualizing average rainfall distribution using choropleth maps.

#### Technical Stack:

Python Apache Spark

### Project 3: Million Song Dataset using Spark
#### Description

This project analyzes music data using Apache Spark to build a system for music recommendations. It identifies songs with similar audio properties and leverages genre information to personalize suggestions.

#### Key Features:

Audio Similarity Analysis:
- Analyzes audio features extracted from music files.
- Identifies songs with similar acoustic characteristics based on selected features.

Machine Learning for Genre Classification:
- Uses supervised learning models to predict genre labels for songs.
- Improves recommendation accuracy by incorporating genre preferences.

Data Preprocessing and Feature Engineering:
- Cleans and prepares audio data for analysis.
- Selects and transforms relevant features for model training.

Handling Class Imbalance:
- Addresses the challenge of uneven genre distribution in music data.
- Employs sampling techniques to ensure balanced representation of all genres.

#### Tech Stack:

Python Apache Spark

### Project 4: Fashion-MNIST Classification with Neural Networks
#### Description

This project explores neural network architectures for classifying fashion items in the Fashion-MNIST dataset. The dataset consists of 70,000 grayscale images of clothing articles categorized into 10 classes (e.g., T-shirts, shoes, dresses).

#### Experiments:

- Hyperparameter Tuning: We investigated the impact of learning rates, optimizers, and batch sizes on model performance using a basic neural network architecture with two dense layers. We observed that manual tuning yielded better results than Optuna, achieving a test accuracy of 86.7%.
- Network Depth: We increased the model's complexity by adding more dense layers, reaching a test accuracy of 88.1%. However, validation loss remained high, suggesting potential overfitting.
- Convolutional Neural Networks (CNNs): We implemented a CNN architecture to exploit the spatial nature of image data. This model achieved a test accuracy of 91.6%, but again exhibited overfitting during training.
- Dropout Regularization: To address overfitting in the CNN, we incorporated dropout layers. This final model achieved a test accuracy of 91.1% while effectively mitigating overfitting.

#### Key Findings:

- Manual hyperparameter tuning can be more effective than automated approaches like Optuna for this specific dataset and network architecture.
- Deeper network architectures generally improve performance, but careful monitoring of validation loss is crucial to prevent overfitting.
- CNNs are well-suited for image classification tasks like Fashion-MNIST, achieving high accuracy on both training and test data.
- Dropout regularization effectively reduces overfitting in CNNs, leading to improved generalization capabilities.

#### Technical Stack:

Python
- NumPy: Numerical computation and array manipulation
- Pandas: Data analysis and manipulation
- Matplotlib: Data visualization
- Seaborn: Advanced data visualization
- Scikit-learn: Data preprocessing and machine learning models
- TensorFlow: Deep learning framework
- Keras: High-level API for building neural networks
- Optuna: Hyperparameter optimization library

## Group Projects
### Project 5: Data Wrangling Group Project
#### Description

Analyzing Impact of Schools & Crime Rates on Housing Prices in New Zealand

#### Data Sources:

- NZ school directory
- crime data
- housing price data
- population estimates
- territorial authority polygons

#### Data Wrangling and Cleaning:

- Julia: Employed for scraping housing price data using the http package and cleaning the data using functionalities within the Julia environment (e.g., data type conversion, filtering).
- R: Utilized the tidyverse suite of packages for data manipulation (reading, filtering, transforming) and cleaning tasks (handling inconsistencies, missing values). Additionally, the sf library aided in working with geospatial data (territorial authority shapefiles).

Data cleaning presented several challenges:

- Inconsistencies: Variations in formatting, missing values, and differing naming conventions across datasets required careful attention and correction.
- Missing values: Data points missing from specific territorial authorities necessitated checks and adjustments to ensure data integrity.

#### Methodology:

Data from all sources was integrated using the "Territorial Authority" as the common key. We employed left joins in R to ensure all territorial authorities were included in the final dataset, even if data from other sources (crime, schools) was missing for specific regions.

#### Technical Stack:

- Julia - http package
- R - tidyverse packages, sf library
- R Shiny
- use of GitHub for version control and collaboration

### Project 6: Road Safety Analysis with Machine Learning and Data Visualization
#### Description

This project investigates factors influencing car crash severity in New Zealand using machine learning and data visualization.

#### Key Findings

- Analyzed 10,000 rows of car crash data using machine learning (Random Forest) in R to identify key factors contributing to accident severity.
- Developed data visualizations (using Tableau) to explore crash trends by region, victim demographics, and time (monthly/hourly).
- Insights generated actionable recommendations for improving road safety measures.

#### Tech Stack

- R (Random Forest)
- Tableau
