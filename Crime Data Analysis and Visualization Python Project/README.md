# Crime Data Analysis and Visualization project
I would like to use Python to explore, analyse and visualize data in a simple and intuitive way. 

Steps in the development process
1. Importing the necessary libraries: Tkinter, pandas, and matplotlib
2. Reading and processing the crime data from the CSV files.
3. Grouping the data based on different categories such as crime type, age group, ethnicity,
and year.I would like to detect the main crime types in New Zealand and see how the age, ethnicity vary among the crime types, therefore, it is an important preparation step to categorize the required data.
4. Implementing functions to display various types of graphs, including bar graphs, pie charts, and line graphs.
By using Matplotlib, I can create various types of graphs to show the trend of the crime types.
5. Creating the GUI window using Tkinter.
By using Tkinter, the graphs that I created before can be visualized in a separate window.
6. Adding the dropdown menu, buttons, and error labels to the GUI window.
7. Binding the display functions to the "Display Graph" button.
8. Testing and refining the program to ensure its functionality.

## Things That Went Well
- Accurate data processing and grouping, allowing for meaningful analysis.

The crime data is clear and ready for use because it was acquired directly from the New Zealand police website. But because I didn't know the proper encoding, I got stopped at the initial stage of importing the data from csv files. With the aid of Liam. Using the "file" command, I was able to determine how to check the encoding for the csv file.

<img width="817" alt="Screenshot 2024-05-24 at 15 41 07" src="https://github.com/jacci25/Data-Science-Portfolio/assets/137580685/11e27473-0832-4d40-96d2-b3a1581cd378">

The pandas loc() method, which enables data retrieval based on specified row and column labels and retrieve the data matching to those labels, is what I use to group the data. I may choose and extract data for the data I utilised based on the row names (such as "ANZSOC Division," "Age Group," and "Ethnicity") and the column labels (such as "Offender Count").

- Implementation of different graph types (bar graphs, pie charts, and line graphs) based on user selection.
  
For this part, I use the matplotlib to plot various types of graphs and customize their appearance.

## Challenge Faced
- Embedding Matplotlib graphs into TKinter applications.

When creating visualizations using Matplotlib, the output is typically displayed in a separate window, which is not suited for the final visualization. The "FigureCanvasTkAgg" class from the "Matplotlib.backends.backend_tkagg" module in the Matplotlib library can be used to embed the Matplotlib graphs into TKinter applications. The graphs should first be displayed using a canvas widget that may display a variety of graphics. The Matplotlib figure is then rendered using the draw() method, which transforms it into a format that can be displayed on the canvas. The canvas widget is shown in the TKinter window as the final phase.

Another problem with the final visualization is that it can not show all types of graphs within the dropdown menu. So a global variable ‘CURRENT_CANVAS’ is created to keep track of the current canvas widget that displays the graph. Before creating a new graph, the code checks if there is an existing canvas widget (CURRENT_CANVAS) and destroys it using the destroy() method of the Tkinter widget. This ensures that only one graph is displayed at a time.

<img width="797" alt="Screenshot 2024-05-24 at 15 42 51" src="https://github.com/jacci25/Data-Science-Portfolio/assets/137580685/00d6c47f-23a6-4f55-b1fc-9313b1a4048a">
