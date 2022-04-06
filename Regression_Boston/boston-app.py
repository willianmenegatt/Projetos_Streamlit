# In this app, the model will be rebuilt every time

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
from sklearn import datasets
import shap

st.write("""
# Boston House Price Prediction App

This app predicts the **Boston House Price**!
""")
st.write('---')

# Loads the Boston House Price dataset
boston = datasets.load_boston()
X = pd.DataFrame(boston['data'], columns=boston['feature_names'])
y = pd.DataFrame(boston['target'], columns=['MEDV'])

# Sidebar
st.sidebar.header('Specify Input Parameters')

def user_input():
    CRIM = st.sidebar.slider('CRIM', float(X['CRIM'].min()), float(X['CRIM'].max()), float(X['CRIM'].mean()))
    ZN = st.sidebar.slider('ZN', float(X['ZN'].min()), float(X['ZN'].max()), float(X['ZN'].mean()))
    INDUS = st.sidebar.slider('INDUS',float(X['INDUS'].min()), float(X['INDUS'].max()), float(X['INDUS'].mean()))
    CHAS = st.sidebar.slider('CHAS', float(X['CHAS'].min()), float(X['CHAS'].max()), float(X['CHAS'].mean()))
    NOX = st.sidebar.slider('NOX', float(X['NOX'].min()), float(X['NOX'].max()), float(X['NOX'].mean()))
    RM = st.sidebar.slider('RM', float(X['RM'].min()), float(X['RM'].max()), float(X['RM'].mean()))
    AGE = st.sidebar.slider('AGE', float(X['AGE'].min()), float(X['AGE'].max()), float(X['AGE'].mean()))
    DIS = st.sidebar.slider('DIS', float(X['DIS'].min()), float(X['DIS'].max()), float(X['DIS'].mean()))
    RAD = st.sidebar.slider('RAD', float(X['RAD'].min()), float(X['RAD'].max()), float(X['RAD'].mean()))
    TAX = st.sidebar.slider('TAX', float(X['TAX'].min()), float(X['TAX'].max()), float(X['TAX'].mean()))
    PTRATIO = st.sidebar.slider('PTRATIO', float(X['PTRATIO'].min()), float(X['PTRATIO'].max()), float(X['PTRATIO'].mean()))
    B = st.sidebar.slider('B', float(X['B'].min()), float(X['B'].max()), float(X['B'].mean()))
    LSTAT = st.sidebar.slider('LSTAT', float(X['LSTAT'].min()), float(X['LSTAT'].max()), float(X['LSTAT'].mean()))
    data = {'CRIM': CRIM,
            'ZN': ZN,
            'INDUS': INDUS,
            'CHAS': CHAS,
            'NOX': NOX,
            'RM': RM,
            'AGE': AGE,
            'DIS': DIS,
            'RAD': RAD,
            'TAX': TAX,
            'PTRATIO': PTRATIO,
            'B': B,
            'LSTAT': LSTAT}
    features = pd.DataFrame(data, index=[0])
    return features

df = user_input()

# Main panel 
st.header('Specified Input Parameters')
st.write(df)
st.write('---')

# Build Regression Model
model = RandomForestRegressor()
model.fit(X, y)

# Apply Model to make prediction
prediction = model.predict(df)

st.header('Prediction of MEDV - Median Value')
st.write(prediction)
st.write('---')

# Explaining the model's prediction using SHAP values
explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X)

st.header('Feature Importance')
plt.title('Feature importance based on SHAP values')
fig = shap.summary_plot(shap_values, X)
st.pyplot(fig, bbox_inches='tight')
st.set_option('deprecation.showPyplotGlobalUse', False)
st.write('---')


plt.title('Feature importance based on SHAP values (Bar)')
fig2 = shap.summary_plot(shap_values, X, plot_type='bar')
st.pyplot(fig2, bbox_inches='tight')
st.set_option('deprecation.showPyplotGlobalUse', False)


# Paste in Terminal: streamlit run c:\Users\Usuario\Desktop\Data_Science\STREAMLIT_PROJECTS\REGRESSION_BOSTON\boston-app.py [ARGUMENTS]
# To deploy in streamlit: https://share.streamlit.io/ - File required: pip freeze > requirements.txt
