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

st.markdown("""
### Integrantes Grupo 01

- Fernando Júdice  
- Gabriel Souza  
- Ilanna Haimenis  
- Michael Arruda  
- Rafaell Cavalcanti  
- Rodrigo Siqueira
""")

with st.expander('Show Varible description'):
    st.markdown("""
    1. **student_id** – identificador único de cada estudante (numérico).  
    2. **age** – idade do aluno, em anos.  
    3. **gender** – gênero (categoria, por ex. “F”, “M”, “Outro”).  
    4. **study_hours_per_day** – horas médias de estudo por dia.  
    5. **social_media_hours** – tempo total diário gasto em redes sociais (horas).  
    6. **netflix_hours** – horas diárias assistindo Netflix.  
    7. **part_time_job** – horas semanais em trabalho de meio período.  
    8. **attendance_percentage** – frequência às aulas (%).  
    9. **sleep_hours** – horas médias de sono por noite.  
    10. **diet_quality** – índice de qualidade da dieta (0 – 10).  
    11. **exercise_frequency** – número de sessões de exercício por semana.  
    12. **parental_education_level** – escolaridade média dos pais (por ex. “High School”, “College”, “Graduate”).  
    13. **internet_quality** – avaliação da qualidade da internet em casa (0 – 10 ou categorias como “Ruim/Boa/Ótima”).  
    14. **mental_health_rating** – autoavaliação de bem-estar mental (0 – 10).  
    15. **extracurricular_participation** – número de atividades extracurriculares em que o estudante participa.  
    16. **exam_score** – nota final do exame (0 – 100), variável-alvo para análises de desempenho.
    """)


x_var = st.selectbox('X Axis', variables, index = 2)
y_var = st.selectbox('Y Axis', variables, index = 15)

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
