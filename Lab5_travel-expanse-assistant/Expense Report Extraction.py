#from openai import AzureOpenAI
import openai
import streamlit as st
import base64
import json
import requests
import re
from sqlalchemy import create_engine
import pandas as pd
import urllib.parse as parse

# Defining image details
image_paths = {
    "Receipt # 1": "images/bills/receipt1.jpg",
    "Receipt # 2": "images/bills/receipt2.jpg",
    "Receipt # 3": "images/bills/receipt3.jpg",
    "Receipt # 4": "images/bills/receipt4.jpg"
}

# Extracting environment variables. Adjust values according to the lab documentation.
AOAI_API_BASE = "YOUR_AZURE_OPENAI_ENDPOINT"
AOAI_API_KEY = "YOUR_AZURE_OPENAI_KEY"
AOAI_API_VERSION = "2023-12-01-preview"
AOAI_DEPLOYMENT = "gpt-4-vision"

# # Initiating Azure OpenAI client.
# client = AzureOpenAI(
#     azure_endpoint=AOAI_API_BASE,
#     api_key=AOAI_API_KEY,
#     api_version=AOAI_API_VERSION
# )

# Database connection details. Adjust DB_Name according to your Team DB.
DB_SERVER = "sqlhackmi-j754o5hum2r36.7a59bf01d694.database.windows.net"
# Adjust DB_Name according to your team number, e.g. TEAM01_LocalMasterDataDB.
DB_NAME = "YOUR_DB_NAME"
DB_USERNAME = "Demouser"
DB_PASSWORD = "Demo@pass1234567"

# Establishing a connection to the Azure SQL Database using SQLAlchemy
connecting_string = f"Driver={{ODBC Driver 17 for SQL Server}};Server=tcp:{DB_SERVER},1433;Database={DB_NAME};Uid={DB_USERNAME};Pwd={DB_PASSWORD}"
params = parse.quote_plus(connecting_string)
engine = create_engine("mssql+pyodbc:///?odbc_connect=%s" % params)



# Defining various variables
base64_image = None
current_image = None
current_image_name = None
analyse_button = False
export_button = False
if "camera" not in st.session_state:
    st.session_state.camera = None
    #st.snow()  # New Year's theme :)

# Defining helper function to call Azure OpenAI endpoint using Python SDK
def gpt4v_completion(image_path):
    # Encoding image to base64
    with open(image_path, "rb") as image_file:
        base64_image = base64.b64encode(image_file.read()).decode("utf-8")

    # Prepare endpoint, headers, and request body
    base_url = f"{AOAI_API_BASE}openai/deployments/{AOAI_DEPLOYMENT}"
    endpoint = f"{base_url}/extensions/chat/completions?api-version=2023-12-01-preview"
    headers = {
        "Content-Type": "application/json",
        "api-key": AOAI_API_KEY
    }

    # Calling Azure OpenAI endpoint via Python SDK. Make sure to adjust the computer vision endpoint and key values according to lab documentation.
    data = {
        "model": "gpt-4-vision-preview",
        "enhancements": {
            "ocr": {
                "enabled": True
            },
            "grounding": {
                "enabled": True
            }
        },
        "dataSources": [
            {
                "type": "AzureComputerVision",
                "parameters": {
                    "endpoint": "YOUR_COMPUTER_VISION_ENDPOINT",
                    "key": "YOUR_COMPUTER_VISION_KEY",
                }
            }
        ],
        "messages": [
            {"role": "system", "content": "You are an finance assistant reading a receipt. Extract information as specified by the user and export as JSON"},
            {"role": "user", "content": [  
                { 
                    "type": "text", 
                    "text": "Extract the following information from the receipt: date, total_amount, tax"    
                },
                { 
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_image}"
                    }
                }
            ]} 
        ],
        "max_tokens": 2000
    }
    

    response = requests.post(endpoint, headers=headers, data=json.dumps(data))

    # Parse relevant information from the response
    result = response.json()
    assistant_response = result['choices'][0]['message']['content']

    # Extracting date, total_amount, and tax from the assistant's response
    date_match = re.search(r'"date":\s*"([^"]+)"', assistant_response)
    total_amount_match = re.search(r'"total_amount":\s*"([^"]+)"', assistant_response)
    tax_match = re.search(r'"tax":\s*"([^"]+)"', assistant_response)

    date_of_purchase = date_match.group(1) if date_match else 'N/A'
    total_amount = total_amount_match.group(1) if total_amount_match else 'N/A'
    tax = tax_match.group(1) if tax_match else 'N/A'

    return {
        'date_of_purchase': date_of_purchase,
        'total_amount': total_amount,
        'tax': tax
    }

# Creating sidebar with instructions
st.sidebar.header("Instructions:")
st.sidebar.markdown(
    """
    Welcome to our Receipt Management Application, where efficiency meets sophistication! Navigate through your receipt assortment seamlessly with our intuitive button selection. 

Experience the precision of our application as it precisely extracts essential details such as the date of purchase, total amount spent, and tax, elegantly presenting them in a structured JSON format when you just click the 'Analyse' button.

In addition to this, the 'Analyse and Export' button goes beyond mere analysis, offering the capability to securely store results in the specified SQL table mentioned in the script. This comprehensive functionality ensures not only detailed insights but also organized and secure data management.

Embrace a new standard in receipt management sophistication with our application!
    """
)

# Creating Home Page UI
st.title("Travel Expense Assistant")
main_container = st.container()
col1, col2 = main_container.columns([1, 3])
image_placeholder = col2.empty()
result_container = st.container()
result_placeholder = result_container.empty()

# Creating button for each receipt image in the first column
for image_name, image_path in image_paths.items():
    # If the button is clicked, load the image and display it in the second column
    if col1.button(image_name):
        image_placeholder.image(image=image_path, caption=image_name, use_column_width=True)
        current_image = image_path
        current_image_name = image_name
        st.session_state.camera = image_name
        analyse_button = False
    # If the analysis button is clicked, preserve the last selected image
    elif st.session_state.camera == image_name:
        image_placeholder.image(image=image_path, caption=image_name, use_column_width=True)
        current_image = image_path
        current_image_name = image_name
        st.session_state.camera = image_name


# Creating analysis button in the first column
if col1.button("Analyse"):
    my_bar = st.progress(50)
    result = gpt4v_completion(current_image)
    my_bar.progress(100)
    result_placeholder.text(
        f"Image analysis results for {current_image_name}:\n{json.dumps(result, indent=2)}"
    )





# Creating export to JSON button in the first column
if col1.button("Analyze & Export"):
    my_bar = st.progress(50)
    result = gpt4v_completion(current_image)
    my_bar.progress(100)

    # Extracting data from the result without unnecessary transformations
    date_of_purchase_value = result['date_of_purchase'] if 'date_of_purchase' in result else None
    total_amount_value = result['total_amount'] if 'total_amount' in result else None
    tax_value = result['tax'] if 'tax' in result else None

    # Format date_of_purchase_value to a valid date format
    formatted_date = pd.to_datetime(date_of_purchase_value, errors='coerce')

    # Remove non-numeric characters from total_amount_value and tax_value
    total_amount_value = ''.join(filter(str.isdigit, str(total_amount_value)))
    tax_value = ''.join(filter(str.isdigit, str(tax_value)))

    # Ensure that total_amount_value and tax_value are numeric or None
    total_amount_value = float(total_amount_value) / 100 if total_amount_value else None
    tax_value = float(tax_value) / 100 if tax_value else None

    # Creating a DataFrame with the extracted data
    df = pd.DataFrame({
        'ReceiptName': [current_image_name],
        'date_of_purchase': [formatted_date if pd.notna(formatted_date) else None],
        'total_amount': [total_amount_value],
        'tax': [tax_value]
    })

 

    try:
        # Inserting data into the 'TravelExpenses' table
        df.to_sql('TravelExpenses', con=engine, if_exists='append', index=False)
        result_placeholder.text(
            f"Exported {current_image_name}:\n{json.dumps(result, indent=2)}\n\nData also stored in Azure SQL Database."
        )
    except Exception as e:
        result_placeholder.text(f"Error during SQL insertion: {str(e)}")
        print(f"Error during SQL insertion for {current_image_name}: {str(e)}")