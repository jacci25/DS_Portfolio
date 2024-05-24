# Analyzing the Impact of School Count and Crime Rate on Housing Prices in Aotearoa
## Introduction

The housing market in New Zealand has consistently been a topic of significant interest, as it reflects not only the housing needs of families but also investment opportunities and changes in socioeconomic conditions. Housing prices vary significantly across different regions of New Zealand, and these variations are influenced by a multitude of factors. This project aims to conduct an analysis of two primary influencing factors: schools and crime rates, to investigate how they impact housing prices in New Zealand across various regions.
## Data Source
The data was obtained from various different sources.
1. The NZ school directory data was obtained directly from Education Counts. All territorial authorities were selected and the data was exported as a CSV file.
2. The crime data was obtained from PoliceNZ. The data covered the time period from January 2023 to June 2023 and records the number of victimizations for different crime types for each territorial authority during this time frame. The data was downloaded as a CSV file.
3. The housing price data for each territorial authority was scraped from Opes Partners (see Techniques Employed section for scraping details).
4. Population estimates for each territorial authority was also collected from StatsNZ (download data section) in order to normalize the school counts and crime rate. The data was downloaded as an XLSX file.
5. In order to create a map of the territorial authorities, NZ territorial authority polygon data was obtained from StatsNZ.
### Relational Data Model
Vertabelo was used to create the relational data model. First, five distinct entities were defined, specifically “Average_Housing_Price”, “School”, “Crime”, “Population” and “Territorial Authority”. "Territorial Authority" is the primary key used to connect and establish relationships between these tables. In each table, only the attributes that are relevant to the project were selected.

The relationships between these entities were illustrated as follows:
1. Average_Housing_Price and Territorial Authority (One-to-One): This relationship means that for each record in the "Territorial Authority" table, there is exactly one corresponding record in the " Average_Housing_Price " table. It suggests that house price data is specific to each individual territorial authority, creating a direct one-to-one relationship.
2. Crime and Territorial Authority (Many-to-One): In this relationship, there are multiple records in the "crime" table associated with a single record in the "Territorial Authority" table. This suggests that multiple victimisations are reported within a single territorial authority, creating a many-to-one relationship.
3. School and Territorial Authority (Many-to-One): Similarly, this relationship implies that there are multiple school records associated with a single territorial authority. It suggests that multiple schools are located within the boundaries of a single territorial authority.
4. Population and Territorial Authority (One-to-One): This relationship means that population data is specific to each individual territorial authority, and there is one population record for each territorial authority, indicating a one-to-one relationship.
<img width="754" alt="Screenshot 2024-05-24 at 15 25 59" src="https://github.com/jacci25/Data-Science-Portfolio/assets/137580685/4b350bdd-9085-4edb-a48a-6268e4e1c9d5">

## Data Wrangling

In this extensive data processing and cleaning section, five datasets from the mentioned sources were acquired. Both Julia and R were used for this data wrangling process.

Careful attention was paid to data exploration to familiarize with the data. Data consistency was addressed, ensuring that each dataset was up to standards. Transformations were applied, refining the data to the right data type. Integration efforts were made to synthesize information from various sources, creating a cohesive dataset. Rigorous validation and quality checks were implemented to fortify the reliability of the data.

**A. Housing Price (Julia)**

Both data acquisition and cleaning for the housing price dataset (‘housedata’) were executed entirely using Julia. The data was scraped by sending an HTTP GET request to the specified URL and converted the data from binary format into a DataFrame.

As 'Territorial_Authority' acts as the primary key in the relational data model, the process commenced with the renaming of the 'Location' column to 'Territorial_Authority'. Following this modification, the data was cleansed by removing the initial row, which contained an aggregate of New Zealand data, not relevant to this specific analysis. Subsequently, the 'Price' column underwent refinement by removing commas from numeric representations and converting them into integers. This transformation was accomplished using the parse() function after comma removal. To streamline the dataset further, only the 'Territorial_Authority' and 'Price' columns were selected, creating a more focused subset.

The resulting processed dataset was then saved in a new CSV file, 'housedata.csv,' in preparation for subsequent steps such as joining tables.

**B. CrimeData(R)**

Data processing for the "crime_data" dataset was carried out using the R. As mentioned previously, the original data was downloaded from the NZ Police website in CSV format. However, the file was in UTF16 format, which led to anomalies during the import into Jupyter Notebook. In particular, the "Territorial Authority" column exhibited irregular formatting and lacked clear delimiters between columns, resulting in improper data display. To address this issue, the CSV file was converted to an Excel format to ensure data integrity and consistency.

Subsequently, only columns of interest were selected, including "Territorial Authority," "Anzsoc Division," "Year Month," and "Victimisations". In an effort to improve clarity and maintain a consistent naming convention, the columns were renamed by replacing spaces with underscores.

Furthermore, trailing periods in the "Territorial Authority" column were present. These were eliminated to enhance data accuracy. A check to verify if the dataset contained all "Territorial Authority" values was also conducted.

A summary dataset named "victims_by_TA" was then created by grouping the data based on "Territorial Authority" and "Anzsoc Division," calculating the total victimizations for each specific crime type within each territorial authority.

It should be also noted that data missing issues when joining tables (see section E) were encountered. After a careful examination of each dataset, a spelling mistake was identified as the cause of this issue: "Whanganui District" was misspelled as "Wanganui District" in this "crime_data" dataset. This was therefore corrected to "Whanganui District."

**C. School Data (R)**

Using R, the school dataset ('School_Data.csv’) was read using the read.csv() function. The first 15 rows of the data were hidden as they were header introductions in the original CSV data. In addition, only specific columns of interest were selected, including 'Territorial.Authority', 'School.Type', and 'Total.School.Roll'.

Examination of the data table revealed that the Auckland territorial authority was divided in multiple suburbs (in the format Auckland-Suburb - e.g., Auckland - Hibiscus and Bays). The 'Territorial.Authority' column thus underwent some data cleaning using the gsub() function to remove the Auckland suburb.

Unique values from 'Territorial.Authority' and 'School.Type' were then extracted, displaying them along with the total count of unique values. This step is to know the unique content of each column, especially to check if the values in the 'Territorial.Authority' column are consistent with the other datasets as this is the primary key.

Finally, a summary dataset named 'group_by_data_draft' was created by grouping the data based on 'Territorial.Authority' and 'School.Type', calculating school counts and total school roll numbers. The first five rows were removed as they contained missing values for ‘Territorial.Authority’. The columns were also renamed and the dataframe was written to a CSV file named 'Final_School_Data.csv'.

**D. Population Data (R)**

The population data (Excel file) was loaded into R using read_excel() and by specifying the tab containing the data ("Table 4"). As the Excel file contained some formatting, the resulting dataframe contained some unnecessary rows at the beginning and end of the dataset. These were thus removed. Moreover, the columns of the dataframe were assigned more intuitive and descriptive names.

The dataset also contained information for each Auckland local board. Since the primary focus of this project lays on territorial authorities, data pertaining to Auckland local boards was excluded.

Next, an irregularity within the year values was addressed: some entries containing an extraneous "P" were removed for uniformity. Subsequently, the data was filtered using the year column, extracting only the records pertinent to 2022 and only relevant columns (i.e., "Territorial_Authority" and "Total_Population") were selected.

To account for potential character encoding issues, variations in the "Territorial_Authority" column were addressed, whereby characters were standardized to ensure uniformity and accuracy in the dataset.

The last row containing a summary for the entirety of New Zealand was also deleted.

A comprehensive check was conducted to validate the unique value of the "Territorial_Authority" column. This step provided an added layer of assurance regarding the accuracy and consistency of the data.

Finally, the dataframe was written and saved in a CSV format.

**E. Normalize the table and join together**

Different territorial authorities can exhibit significant variations in population size, with some being notably larger than others. When comparing crime rates and school counts across these territorial authorities, directly using raw counts can lead to unfair comparisons, as larger territorial authorities tend to naturally have higher crime rates and more schools due to their larger populations. Therefore, the victimisations and school counts data were standardized by adjusting them to a common scale (per 10,000 inhabitants) separately, allowing for a more equitable comparison. This adjustment ensures that comparisons are not skewed by population size and enables a fair assessment of relative differences in crime rates and school counts.

Finally, the normalized school data, normalized crime data and house price data were joined together based on the same territorial authority. Left join was used to ensure that all the territorial authorities were kept even if there was no direct match with school data, crime data or house price data.

<img width="611" alt="Screenshot 2024-05-24 at 15 30 25" src="https://github.com/jacci25/Data-Science-Portfolio/assets/137580685/02774bbd-3187-4325-9cef-48c6626d601f">

**F. Mapping Data (R)**

In order to create a map visualization of the data, the territorial authority shapefile was joined with the normalized data table (section V). The geospatial data was first read in R using st_read() from the sf library, and the normalized data was read using read_csv().

The dataframes were then joined on the territorial authority columns, using a left join to ensure that all the geospatial data was kept in (even if there was no corresponding school/crime data).

The resulting dataframe was written and saved as a shapefile.

## Data Visualization and Insights

Using the mapping data table, a scatter plot of the average house price for each territorial authority as a function of both the normalized number of schools and the normalized crime rate was generated. The plot shows that, based on the collected data, there is no evidence of a correlation between crime rate or number of schools and the average house price.

<img width="772" alt="Screenshot 2024-05-24 at 15 33 07" src="https://github.com/jacci25/Data-Science-Portfolio/assets/137580685/2412dacc-f829-408d-8155-e04cd6676b07">

Moreover, choropleth maps displaying the normalized number of schools, the normalized crime rate and the average house price for each territorial authority were created. The R Shiny dashboard allows the user to choose which data to display.

<img width="810" alt="Screenshot 2024-05-24 at 15 33 42" src="https://github.com/jacci25/Data-Science-Portfolio/assets/137580685/a619e8f1-958e-4915-a950-8cd73b9df784">

In addition, the user can select a specific territorial authority to display further information about the school and crime data (see Figure 5). More specifically, using the cleaned crime and school data, bar charts showing the distribution of the crime types (e.g., theft, sexual assault, etc.) and school types (e.g., primary, secondary, etc.) for the selected region were generated.

<img width="526" alt="Screenshot 2024-05-24 at 15 34 31" src="https://github.com/jacci25/Data-Science-Portfolio/assets/137580685/64d7c41b-cffb-432c-b6e7-056db3134377">

## Conclusion

In conclusion, the aim of this project was to investigate the impact of factors such as crime rate and the number of schools on housing prices in Aotearoa. To achieve this, data from 5 different sources was collected and wrangled using various techniques, including scraping, data cleaning, aggregation and joining. An interactive dashboard was then produced using the wrangled and cleaned data to display findings. Overall, based on the data collected, there is no evidence of correlation between crime rate or number of schools and housing price. Further investigation that takes into account temporality and the changes of these factors over time would be useful to confirm this.
