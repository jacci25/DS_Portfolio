import tkinter as tk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Create a global variable to store the current FigureCanvasTkAgg instance
CURRENT_CANVAS= None

# Import data from CSV file
crime_data = pd.read_csv('Unique_Offenders_2023.csv', sep="\t", encoding="UTF-16")

# Rename the last column to 'Record Count'
crime_data = crime_data.rename(columns={'记录数': 'Record Count'})

#Group the data by crime types
counts_crime_type = {}
for i in range(len(crime_data)):
    # Get the crime type and offender count for the current row
    # Use 'loc' method to select rows and columns by label
    crime_type = crime_data.loc[i, 'ANZSOC Division']
    offender_count = crime_data.loc[i, 'Offender Count']
    if crime_type in counts_crime_type:
        counts_crime_type[crime_type] += offender_count
    else:
        counts_crime_type[crime_type] = offender_count
# Convert the dictionary to a pandas series
counts_crime_type = pd.Series(counts_crime_type)

#Group the data by crime subdivision types
counts_crime_type_subdivision = {}
for i in range(len(crime_data)):
    crime_subdivision = crime_data.loc[i, 'ANZSOC Subdivision']
    offender_count = crime_data.loc[i, 'Offender Count']
    if crime_subdivision in counts_crime_type_subdivision:
        counts_crime_type_subdivision[crime_subdivision] += offender_count
    else:
        counts_crime_type_subdivision[crime_subdivision] = offender_count
counts_crime_type_subdivision = pd.Series(counts_crime_type_subdivision)

#Group the data by age
counts_age_group = {}
for i in range(len(crime_data)):
    age_group = crime_data.loc[i, 'Age Group']
    offender_count = crime_data.loc[i, 'Offender Count']
    if age_group in counts_age_group:
        counts_age_group[age_group] += offender_count
    else:
        counts_age_group[age_group] = offender_count
counts_age_group = pd.Series(counts_age_group)

#Group the data by ethnicity
counts_ethnicity = {}
for i in range(len(crime_data)):
    ethnicity = crime_data.loc[i, 'Ethnicity']
    offender_count = crime_data.loc[i, 'Offender Count']
    if ethnicity in counts_ethnicity:
        counts_ethnicity[ethnicity] += offender_count
    else:
        counts_ethnicity[ethnicity] = offender_count
counts_ethnicity = pd.Series(counts_ethnicity)

# Create an empty pandas DataFrame
data = pd.DataFrame()
# Loop over the range of years 2019 to 2023
for year in range(2019, 2024):
    filename = f"Unique_Offenders_{year}.csv"
    df = pd.read_csv(filename, sep="\t", encoding="UTF-16")
    df = df.sort_values(by='Year')
    data = pd.concat([data, df], axis=0) # Append the current year's DataFrame to the main DataFrame
counts_year = data.groupby(['Year'])['Offender Count'].sum()
counts = counts_year.reset_index().set_index('Year')

# Create the function to display a graph
def display_bar_graph(title, x_label, y_label, data=None):
    """Create the function to display a graph"""
    global CURRENT_CANVAS
    # clear the current figure
    plt.close('all')
    # Create a new figure with a specific size
    fig, axes = plt.subplots(figsize=(15, 10))
    # Create a bar plot using the data, with the x values specified as the index of the data
    # and the y values specified as the values of the data
    axes = data.plot.bar(data.index, data.values, ax=axes)
    # add text labels for the bar values
    counter = 0
    for value in data.values:
        # Add text to the plot at the current x and y coordinates, with the value converted to a string
        plt.text(counter, value, str(value), ha='center') 
        counter += 1
    axes.set_xlabel(x_label)
    axes.set_ylabel(y_label)
    axes.set_title(title)
    plt.xticks(rotation=90)

    # Create a FigureCanvasTkAgg instance and pack it into the GUI window
    CURRENT_CANVAS = FigureCanvasTkAgg(fig, master=root)
    #Render the figure onto the Tkinter canvas.
    CURRENT_CANVAS.draw()
    #Pack the canvas widget within the Tkinter window to display the graph
    CURRENT_CANVAS.get_tk_widget().pack()
    
def display_pie_graph(title,x_label, y_label, data=None):
    """Create the function to display a pie chart"""
    global CURRENT_CANVAS
    # clear the current figure
    plt.close('all')
    # create a pie chart with percentages displayed
    fig, axes = plt.subplots(figsize=(10,10))
    # compute the percentage of each data point and create custom labels
    labels = []
    total = sum(data)
    for label, value in data.items():
        percent = value / total * 100
        label_str = label + ' - ' + str(round(percent,1)) + '%'
        labels.append(label_str)
    # plot the pie chart and add the custom labels to the legend
    wedges, _, _ = axes.pie(data, autopct='%1.1f%%',textprops={'fontsize': 8})
    axes.legend(handles=wedges, loc="best", bbox_to_anchor=(1, 0.5), labels=labels)
    # remove the y-axis label
    axes.set_ylabel('')
    axes.set_title(title)

    # Create a FigureCanvasTkAgg instance and pack it into the GUI window
    CURRENT_CANVAS = FigureCanvasTkAgg(fig, master=root)
    CURRENT_CANVAS.draw()
    CURRENT_CANVAS.get_tk_widget().pack()

def display_line_graph(title, x_label, y_label, data=None):
    """Create the function to display a line graph"""
    global CURRENT_CANVAS
    # clear the current figure
    plt.clf()
    counts_year.plot(kind='line', figsize=(10, 6))
     # get unique years from the index
    years = data.index.unique()
     # set the x-axis ticks to the years
    plt.xticks(years,years.astype(int))
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
        
    # Create a FigureCanvasTkAgg instance and pack it into the GUI window
    CURRENT_CANVAS = FigureCanvasTkAgg(plt.gcf(), master=root)
    CURRENT_CANVAS.draw()
    CURRENT_CANVAS.get_tk_widget().pack()

# Create the GUI window
# Initialize a tkinter object
root = tk.Tk()

# Set the title of the window
root.title("Crime Data Analysis in New Zealand")

#Set GUI window size
root.geometry("1000x1000")

# Create the label for graph selection
graph_label = tk.Label(root, text="Select a graph:")

# Pack the label into the window
graph_label.pack()

# Create the graph selection dropdown menu
graph_options = ['Offender Count by Crime Type','Offender Count by Specific Crime Type', 'Offender Count by Age Group', 'Offender Count by Ethnicity', 'Offender Count by Year (2019-2023)']

#Create a string variable for graph selection
graph_variable = tk.StringVar(root)

#Set the default graph selection to the first option in the list
graph_variable.set(graph_options[0])

#Create a dropdown menu for selecting the graph
graph_dropdown = tk.OptionMenu(root, graph_variable, *graph_options)
# Pack the dropdown menu into the window
graph_dropdown.pack()

# Create the function to display the selected graph
def display_selected_graph():
    """Create the function to display the selected graph"""
    global CURRENT_CANVAS
    # Delete the old FigureCanvasTkAgg instance
    if CURRENT_CANVAS is not None:
        CURRENT_CANVAS.get_tk_widget().destroy()
    selection = graph_variable.get()
    while selection not in graph_options:
        # Display an error message if an invalid option is selected
        error_label.config(text='Invalid selection. Please select a valid option.')
        return error_label.config(text='')
    if selection == 'Offender Count by Crime Type':
        display_bar_graph('Offender Count by Crime Type', 'Crime Type', 'Offender Count', data=counts_crime_type)
    elif selection == 'Offender Count by Specific Crime Type':
        display_bar_graph('Offender Count by Specific Crime Type', 'Crime Type', 'Offender Count', data=counts_crime_type_subdivision)
    elif selection == 'Offender Count by Age Group':
        display_bar_graph('Offender Count by Age Group', 'Age Group', 'Offender Count', data=counts_age_group)
    elif selection == 'Offender Count by Ethnicity':
        display_pie_graph('Offender Count by Ethnicity', None, None, data=counts_ethnicity)
    elif selection == 'Offender Count by Year (2019-2023)':
        display_line_graph('Offender Count by Year (2019-2023)', 'Year', 'Offender Count', data=counts)
    else:
        # Display an error message if no graph is selected
        error_label.config(text='Please select a graph to display.')

# Create the button to display the selected graph
display_button = tk.Button(root, text="Display Graph", command=display_selected_graph)
# Pack the dropdown menu into the window
display_button.pack()

# Create the label for error messages
error_label = tk.Label(root, fg='red')
# Pack the dropdown menu into the window
error_label.pack()

# Create the function to close the GUI window
def close_window():
    """Create the function to close the GUI window"""
    root.destroy()

# Create the button to close the GUI window
close_button = tk.Button(root, text="Close Window", command=close_window)
# Pack the dropdown menu into the window
close_button.pack()

# Run the GUI window
root.mainloop() 
