import streamlit as st
import pandas as pd
import os
import plotly.figure_factory as ff


def snake_to_title(snake_str: str):
    return snake_str.replace('_', ' ').title()

def load_data():
    # Find the CSV file inside the decompressed folder (assuming there's only one or you know the name)
    csv_file_name = None
    for root, dirs, files in os.walk("."):
        for file in files:
            if file.endswith(".csv"):
                csv_file_name = os.path.join(root, file)
                break
        if csv_file_name:
            break

    if csv_file_name:
        print(f"Found CSV file: {csv_file_name}")
        # Read the CSV into a pandas DataFrame
        df = pd.read_csv(csv_file_name)
        print("DataFrame created successfully:")
        print(df.head())
    else:
        print("No CSV file found in the zip archive.")

    # Remove snake case
    df.columns = [col.replace('_', ' ').title() for col in df.columns]
    return df


def map_categorical_to_numeric(df):
    # Dictionary to store mappings
    mappings = {}

    # Encode and store mappings
    for col in df.select_dtypes(include='object'):
        labels, uniques = pd.factorize(df[col])
        df[col] = labels
        mappings[col] = dict(enumerate(uniques))  # maps 0 -> 'red', etc.
    return mappings



df = load_data()
mappings = map_categorical_to_numeric(df)
variables = df.keys()

st.title("Correlation betweeen Students habits and final grade")

x_var = st.selectbox('X Axis', variables)
y_var = st.selectbox('Y Axis', variables)

# You can now use the 'df' DataFrame for your data analysis

if x_var and y_var:

    correlation = df[x_var].corr(df[y_var])

    st.write(f"Correlation between {snake_to_title(x_var)} and {snake_to_title(y_var)}: {correlation:.3f}")

    if x_var != 'Student Id' and x_var in mappings:
       s = '\n'.join([f"{k}: {v}" for k, v in mappings[x_var].items()])
       st.write(f"X label: {s}")

    if y_var != 'Student Id' and y_var in mappings:
       s = '\n'.join([f"{k}: {v}" for k, v in mappings[y_var].items()])
       st.write(f"Y label: {s}")


    st.scatter_chart(df,
        x=x_var,
        y=y_var,
        x_label = snake_to_title(x_var),
        y_label = snake_to_title(y_var)
    )
 
    st.write(f"Histogram between {x_var} and {y_var}")

    if x_var != 'Student Id' and x_var in mappings:
        filtered_df = []
        # Filter data for each group
        for code, label in mappings[x_var].items():
            filtered_df.append(df[df[x_var] == code][y_var])
        fig = ff.create_distplot(
            filtered_df, list(mappings[x_var].values()))
        st.plotly_chart(fig)
else:
   st.write("Please, choose another option")
