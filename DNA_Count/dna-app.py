from turtle import width
import pandas as pd
import streamlit as st
import altair as alt
from PIL import Image


# Page header

image = Image.open('C:/Users/Usuario/Desktop/Data_Science/STREAMLIT_PROJECTS/DNA_COUNT/dna_logo.jpg')

st.image(image, use_column_width=True)      # Expand the image

st.write("""

# DNA Nucleotide Count Web App

This app counts the nucleotide composition of query DNA!

""")


# Input text box

st.header('Enter DNA sequence:')

sequence_input = ">DNA Query 2\nGAACACGTGGAGGCAAACAGGAAGGTGAAGAAGAACTTATCCTATCAGGACGGAAGGTCCTGTGCTCGGG\nATCTTCCAGACGTCGCGACTCTAAATTGCCCCCTCTGAGGTCAAGGAACACAAGATGGTTTTGGAAATGC\nTGAACCCGATACATTATAACATCACCAGCATCGTGCCTGAAGCCATGCCTGCTGCCACCATGCCAGTCCT"

sequence = st.text_area('Sequence input', sequence_input, height=250)
sequence = sequence.splitlines()
sequence = sequence[1:]         # skipping the sequence name (first line)
sequence = ''.join(sequence)    # concatenates the sequence input with '' space


st.write("""***""")

# Print the input DNA sequence
st.header('INPUT (DNA Query)')
sequence

# DNA nucleotide count
st.header('OUTPUT (DNA Nucleotide Count)')

# Print dictionary
st.subheader('1. Print dictionary')
def DNA_count(sequence):
    d = dict([('A', sequence.count('A')),
              ('T', sequence.count('T')),
              ('G', sequence.count('G')),
              ('C', sequence.count('C'))])
    return d

X = DNA_count(sequence)
X

# Print text
st.subheader('2. Print text')
st.write('There are ' + str(X['A']) + ' adenine (A).')
st.write('There are ' + str(X['T']) + ' thymine (T).')
st.write('There are ' + str(X['G']) + ' guanine (G).')
st.write('There are ' + str(X['C']) + ' cytosine (C).')

# Display dataframe
st.subheader('3. Display dataframe')
df = pd.DataFrame.from_dict(X, orient='index')
df = df.rename({0: 'count'}, axis='columns')
df.reset_index(inplace=True)
df = df.rename(columns = {'index': 'nucleotide'})
st.write(df)

# Display bar chart using altair
st.subheader('4. Display bar chart')
plot = alt.Chart(df).mark_bar().encode(x='nucleotide', y='count')
plot = plot.properties(width=alt.Step(80))     # controls the width of bar

st.write(plot)


# Paste in CMD: streamlit run d:/USUARIO/Desktop/PYTHON/STREAMLIT_PROJECTS/DNA_COUNT/dna-app.py [ARGUMENTS]