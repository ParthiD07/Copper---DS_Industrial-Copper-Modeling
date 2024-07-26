import streamlit as st
import pickle
import numpy as np
from streamlit_option_menu import option_menu

# Add a title to your Streamlit app

st.set_page_config(page_title= "Industrial Copper Modelling",
                   layout= "wide",initial_sidebar_state='expanded')
st.markdown('<h1 style="color:#b26a22;text-align: center;">Industrial Copper Modelling</h1>', unsafe_allow_html=True)
# Set up the option menu

menu=option_menu("",options=["Project Overview","Status Prediction","Selling Price Prediction"],
                        icons=["house","check-circle",'cash'],
                        default_index=1,
                        orientation="horizontal",
                        styles={
        "container": {"width": "100%", "border": "2px ridge", "background-color": "#333333"},
        "icon": {"color": "#FFD700", "font-size": "20px"}, 
        "nav-link": {"font-size": "16px", "text-align": "center", "margin": "0px", "color": "#FFFFFF"},
        "nav-link-selected": {"background-color": "#555555", "color": "#FFFFFF"}})

# set up the information for 'Project Overview' menu
if menu == 'Project Overview':
    st.subheader(':violet[Project Title:]')
    st.markdown('<h5>Industrial Copper Modelling</h5>', unsafe_allow_html=True)

    st.subheader(':violet[Description:]')
    st.markdown('<h5>This project aims to develop predictive models for copper manufacturing processes to enhance production efficiency. By analyzing various input parameters, the project focuses on optimizing manufacturing operations and accurately forecasting outcomes, leading to improved decision-making and cost savings.</h5>', unsafe_allow_html=True)

    st.subheader(':violet[Technologies and Tools:]')
    st.markdown('<h5>Python, Pandas, NumPy, Scikit-Learn, Matplotlib, Seaborn, Streamlit</h5>', unsafe_allow_html=True)

    st.subheader(':violet[Project Learning Outcomes:]')
    st.markdown("""
- **Master Python and Libraries:** Gain proficiency in Python and its data analysis libraries, including Pandas, NumPy, Matplotlib, Seaborn, Scikit-learn, and Streamlit.
- **Data Preprocessing:** Learn techniques for handling missing values, outlier detection, and data normalization.
- **Exploratory Data Analysis (EDA):** Understand and apply EDA techniques such as boxplots, histograms, and scatter plots to visualize and interpret data.
- **Machine Learning:** Develop skills in advanced machine learning techniques for regression and classification, model building, and optimization.
- **Feature Engineering:** Create and utilize new features to enhance model performance.
- **Web Application Development:** Build and deploy an interactive web application using Streamlit to showcase machine learning models.
- **Domain-Specific Insights:** Understand manufacturing challenges and explore how machine learning can address them effectively.""")


# User input Values:
class columns():
    country=[25.0, 26.0, 27.0, 28.0, 30.0, 32.0, 38.0, 39.0, 40.0, 77.0, 78.0, 79.0, 80.0, 84.0, 89.0, 107.0, 113.0]
    status=['Won', 'To be approved', 'Lost', 'Not lost for AM','Wonderful', 'Revised', 'Offered', 'Offerable']
    status_encoded={'Won':1,'To be approved':3,'Lost':0,'Not lost for AM':4,'Wonderful':5,'Revised':6,'Offered':7,'Offerable':8}
    item_type=['W', 'WI', 'S', 'Others', 'PL', 'IPL', 'SLAWR']
    item_type_encoded={'W':5, 'WI':6, 'S':3, 'Others':1, 'PL':2, 'IPL':0, 'SLAWR':4}
    application=[2.0, 3.0, 4.0, 5.0, 10.0, 15.0, 19.0, 20.0, 22.0, 25.0, 26.0, 27.0, 28.0, 29.0, 38.0, 39.0, 40.0, 41.0, 42.0,
                  56.0, 58.0, 59.0, 65.0, 66.0, 67.0, 68.0, 69.0, 70.0, 79.0, 99.0]
    product_ref=[611733, 611993, 628117, 628377, 640405, 640665, 164141591, 164337175, 929423819, 1282007633, 1332077137, 1665572032,
                  1665572374, 1668701376, 1668701698, 1668701718, 1668701725, 1670798778, 1671863738, 1690738206, 1690738219, 1693867550, 1693867563, 1721130331]
    
if menu == 'Status Prediction':
    st.markdown('<h2 style="color:#b26a22;text-align: center;">Status Prediction', unsafe_allow_html=True)
    st.markdown("<h4 style=color:#b26a22>Enter the following details:",unsafe_allow_html=True)
    st.write('')

    with st.form('classifier'):
        col1,col2=st.columns(2)

        with col1:
            Item_Date=st.date_input(label='**Item Date**',format='DD/MM/YYYY')
            Country=st.selectbox(label='**Country**',options=columns.country,index=None)
            Application=st.selectbox(label='**Application**',options=columns.application,index=None)
            Product_Ref=st.selectbox(label='**Product Ref**',options=columns.product_ref,index=None)
            Item_Type=st.selectbox(label='**Item Type**',options=columns.item_type,index=None)

        with col2:
            Customer_ID=st.number_input('**Customer ID**',min_value=10000)
            Quantity=st.number_input('**Quantity Tons**',min_value=0.1)
            Thickness=st.number_input('**Thickness**',min_value=0.1)
            Width=st.number_input('**Width**',min_value=1)
            Selling_Price=st.number_input('**Selling Price**',min_value=1)
            Delivery_Date=st.date_input(label='**Delivery Date**',format='DD/MM/YYYY')

        button=st.form_submit_button(':orange[**Predict Copper Status**]',use_container_width=True)

    if button:
        if not all([Item_Date, Delivery_Date, Country, Item_Type, Application, Product_Ref,
                    Customer_ID,Quantity, Width,Selling_Price]):
            st.error("Select all required fields")
        else:
            with open ('Classifier_model.pkl','rb') as file:
                model=pickle.load(file)

            Item_type_Encoded=columns.item_type_encoded.get(Item_Type)
            Delivery_Time_Taken=abs((Item_Date - Delivery_Date).days)

            Quantity_Tons_Log=np.log(Quantity)
            Thickness_Log=np.log(Thickness)
            Selling_Price_Log=np.log(Selling_Price)+1

            #predict the status with classifier model
            user_data=np.array([[Customer_ID, Country,Item_type_Encoded,Application, Width, Product_Ref,
                                Delivery_Time_Taken, Quantity_Tons_Log, Thickness_Log,Selling_Price_Log]])
            
            status=model.predict(user_data)

            #display the predicted status 
            if status==1:
                st.subheader(f":green[Copper Status:] Won")
            else:
                st.subheader(f":red[Copper Status:] Lost")

if menu == 'Selling Price Prediction':
    st.markdown('<h2 style="color:#b26a22;text-align: center;">Selling Price Prediction', unsafe_allow_html=True)
    st.markdown("<h4 style=color:#b26a22>Enter the following details:",unsafe_allow_html=True)
    st.write('')

    with st.form('regressor'):
        col1,col2=st.columns(2)

        with col1:
            Item_Date=st.date_input(label='**Item Date**',format='DD/MM/YYYY')
            Country=st.selectbox(label='**Country**',options=columns.country,index=None)
            Application=st.selectbox(label='**Application**',options=columns.application,index=None)
            Product_Ref=st.selectbox(label='**Product Ref**',options=columns.product_ref,index=None)
            Item_Type=st.selectbox(label='**Item Type**',options=columns.item_type,index=None)
            Status=st.selectbox(label='**Status**',options=columns.status,index=None)

        with col2:
            Customer_ID=st.number_input('**Customer ID**',min_value=10000)
            Quantity=st.number_input('**Quantity Tons**',min_value=0.1)
            Thickness=st.number_input('**Thickness**',min_value=0.1)
            Width=st.number_input('**Width**',min_value=1)
            Delivery_Date=st.date_input(label='**Delivery Date**',format='DD/MM/YYYY')

        button=st.form_submit_button(':orange[**Predict Copper Selling Price Prediction**]',use_container_width=True)

    if button:
        if not all([Item_Date, Delivery_Date, Country, Item_Type, Application, Product_Ref,
                    Customer_ID,Quantity, Width,Status]):
            st.error("Select all required fields")
        else:
            with open ('Regressor_model.pkl','rb') as file:
                model1=pickle.load(file)

            Status_Encoded=columns.status_encoded.get(Status)
            Item_type_Encoded=columns.item_type_encoded.get(Item_Type)
            Delivery_Time_Taken=abs((Item_Date - Delivery_Date).days)

            Quantity_Tons_Log=np.log(Quantity)
            Thickness_Log=np.log(Thickness)

            #predict the status with regressor model
            user_data=np.array([[Customer_ID, Country,Item_type_Encoded,Application, Width, Product_Ref,
                                Delivery_Time_Taken, Quantity_Tons_Log, Thickness_Log,Status_Encoded]])
            
            predict_sp=model1.predict(user_data)

            selling_price=np.exp(predict_sp[0])

            #display the predicted selling price 
            st.subheader(f":green[Predicted Selling Price :] {selling_price:.2f}") 

            












