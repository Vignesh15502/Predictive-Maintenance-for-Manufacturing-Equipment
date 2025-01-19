import streamlit as st
import pickle
import numpy as np
import sklearn
from streamlit_option_menu import option_menu
import pymongo

client = pymongo.MongoClient("mongodb+srv://vignesh:vigneshd@vignesh.vrsd7ro.mongodb.net/?retryWrites=true&w=majority&appName=VIGNESH")

db = client["Predictive_Maintenance"]
coll = db["datas"]

def predict_failier(Air_temp, Process_temp, Rot_speed, Torque, 
                    Tool_wear, Type):
    
    if Type == "H":
        H, L, M = (1, 0, 0)
        
    elif Type == "L":
        H, L, M = (0, 1, 0)

    elif Type == "M":
        H, L, M = (0, 0, 1)

    #modelfile of the classification
    with open(r"Predictive_Maintenance_Model.pkl","rb") as f:
        model_reg=pickle.load(f)

    user_data= np.array([[Air_temp, Process_temp, Rot_speed, Torque,
                          Tool_wear, H, L, M]])
    
    y_pred= model_reg.predict(user_data)

    Target = int(y_pred[0][0])
    No_Failure = int(y_pred[0][1])
    Heat_Dissipation_Failure = int(y_pred[0][2])
    Overstrain_Failure = int(y_pred[0][3])
    Power_Failure = int(y_pred[0][4])
    Tool_Wear_Failure = int(y_pred[0][5])
    Random_Failures = int(y_pred[0][6])


    user_data_dict = {'Air temperature [K]': Air_temp,
                        'Process temperature [K]': Process_temp,
                        'Rotational speed [rpm]': Rot_speed,
                        'Torque [Nm]': Torque,
                        'Tool wear [min]': Tool_wear,
                        'H': H,
                        'L': L,
                        'M': M,
                        'Target': Target,
                        'No Failure': No_Failure,
                        'Heat Dissipation Failure': Heat_Dissipation_Failure,
                        'Overstrain Failure': Overstrain_Failure,
                        'Power Failure': Power_Failure,
                        'Tool Wear Failure': Tool_Wear_Failure,
                        'Random Failures': Random_Failures}

    coll.insert_one(user_data_dict)

    st.write("## :green[**User Data Successfully inserted into MongoDB**]")

    if y_pred[0][0] == 1:
        return "One Failer Occured", y_pred
    
    else:
        return "No Failier", y_pred


st.set_page_config(layout= "wide")

st.title(":blue[**Predictive Maintenance for Manufacturing Equipment**]")

with st.sidebar:
    option = option_menu('VIGNESH P', options=["PREDICT FAILIER"])

if option == "PREDICT FAILIER":

    st.header("PREDICT FAILIER")
    st.write(" ")

    col1,col2= st.columns(2)


    with col1:
        Air_temperature= st.number_input(label="**Enter the Value for Air temperature [K]**")
        Process_temperature= st.number_input(label="**Enter the Value for Process temperature [K]**")
        Rotational_speed= st.number_input(label="**Enter the Value for Rotational speed [rpm]**")

    with col2:
        Torque= st.number_input(label="**Enter the Value for Torque [Nm]**")
        Tool_wear= st.number_input(label="**Enter the Value for Tool wear [min]**")
        Type= st.selectbox("Enter the Type:",["H", "L", "M"])
        

    button= st.button(":violet[***PREDICT THE FAILIER***]",use_container_width=True)

    if button:
        status, y_predicted= predict_failier(Air_temperature,Process_temperature,Rotational_speed,
                                Torque,Tool_wear,Type,)
        
        if status == "One Failer Occured":


            st.write("## :red[One Failer Occured]")
            st.write("")
            st.write("")
            st.subheader("The Failier is")
            if y_predicted[0][2] == 1:
                st.write("## :red[Heat Dissipation Failure]")

            elif y_predicted[0][3] == 1:
                st.write("## :red[Overstrain Failure]")

            elif y_predicted[0][4] == 1:
                st.write("## :red[Power Failure]")
            
            elif y_predicted[0][5] == 1:
                st.write("## :red[Tool Wear Failure]")

            elif y_predicted[0][6] == 1:
                st.write("## :red[Random Failures]")

        elif status == "No Failier":
            st.write("## :green[**No Failier Occured**]")
   
