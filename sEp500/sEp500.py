import matplotlib
import pandas as pd
import streamlit as st
import base64 
import matplotlib.pyplot as plt
import yfinance as yf
st.set_option('deprecation.showPyplotGlobalUse', False)


st.title('S&P 500 App')

st.markdown("""

This app retrieves the list of the **S&P 500** (from wikipedia) and its corresponding 
**stock closing price** (year-to-date)!
* **Data source**: https://pt.wikipedia.org/wiki/Lista_de_companhias_citadas_no_Ibovespa  

""")

st.sidebar.header('User input Features')

# Web scraping of the S&P 500 data
@st.cache
def load_data():
    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    html = pd.read_html(url, header=0)
    df = html[0]
    return df

df = load_data()
sector = df.groupby('GICS Sector')

# Sidebar - Sector selection
sorted_sector_unique = sorted(df['GICS Sector'].unique())
selected_sector = st.sidebar.multiselect('Sector', sorted_sector_unique, sorted_sector_unique)

# Filtering data
df_selected_sector =df[(df['GICS Sector'].isin(selected_sector))]

st.header('Display Companies in Selected Sector')
st.write('Data dimension: ' + str(df_selected_sector.shape[0]) + ' rows and' + str(df_selected_sector.shape[1]) + ' columns.')
st.dataframe(df_selected_sector)

# Download CSV data file
def filedownload(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
    href = f'<a href="data:file/csv;base64,{b64}" download="SP500.csv">Download CSV File</a>'
    return href

st.markdown(filedownload(df_selected_sector), unsafe_allow_html=True)

# Download finance data from yahoo
data = yf.download(
    tickers=list(df_selected_sector['Symbol'][:10]),       # In yahoo the brasilian stocks end with '.SA'
    period='ytd',
    interval='1d',
    group_by='ticker',
    auto_adjust=True,
    prepost=True,
    threads=True,
    proxy=None)

# Plot closing price
def price_plot(symbol):
    df = pd.DataFrame(data[symbol]['Close'])
    df['Date'] = df.index
    plt.fill_between(df['Date'], df['Close'], color='Darkgreen', alpha=0.3)
    plt.plot(df['Date'], df['Close'], color='Darkgreen', alpha=0.8)
    plt.xticks(rotation=90)
    plt.title(symbol, fontweight='bold')
    plt.xlabel('Date', fontweight='bold')
    plt.ylabel('Closing Price', fontweight='bold')
    return st.pyplot()

# Delimiting the number of companies
num_company = st.sidebar.slider('Number of companies', 1, 10)

# Plot button
if st.button('Show plots'):
    st.header('Stock Closing Price')
    for i in list(df_selected_sector['Symbol'])[:num_company]:
        price_plot(i)
        

# PAST in Terminal: streamlit run c:/Users/Usuario/Desktop/Data_Science/STREAMLIT_PROJECTS/SEP500_STOCKS/sEp500.py [ARGUMENTS]
