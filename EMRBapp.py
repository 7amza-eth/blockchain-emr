import os
import json
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st
import time
from pinata import pin_file_to_ipfs, pin_json_to_ipfs, convert_data_to_json

load_dotenv()

# Define and connect a new Web3 provider
w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))

# Loads contract using cache and connect ausing ddress and ABI
@st.cache(allow_output_mutation=True)
def load_contract():
    with open(Path('./contracts/compiled/emrblocks_abi.json')) as f:
        contract_abi = json.load(f)
    contract_address = os.getenv("SMART_CONTRACT_ADDRESS")
    contract = w3.eth.contract(
        address=contract_address,
        abi=contract_abi
    )
    return contract
contract = load_contract()

# IPFS helper functions
def pin_patient(patientName,dateOfBirth,gender,weight,height, patientImage):
    #pin patient image
    ipfs_file_hash = pin_file_to_ipfs(patientImage.getvalue())
    #build an patient metadata JSON file
    patientJSON = {
        'image': ipfs_file_hash,
        'name': patientName,
        'DOB': dateOfBirth,
        'gender': gender,
        'weight': weight,
        'height': height
    }
    json_data = convert_data_to_json(patientJSON)
    #pin patient json file
    ipfs_json_hash = pin_json_to_ipfs(json_data)
    return ipfs_json_hash

def pinUpdateHeight(): #@TODO pinning updated height to patient json, update already made json??
    return
def pinUpdateWeight(): #@TODO pinning updated weight to patient json, update already made json??
    return

# Title and account selection
st.title('Blockchain EMR System')
st.write('Choose an account to get started')
accounts = w3.eth.accounts
address = st.selectbox('Select Account', options=accounts)
st.markdown('---')

# Register New Patient
st.markdown('## Register New Patient')
patientName = st.text_input('Enter patient name')
dateOfBirth = st.date_input('Enter patient date of birth') #@TODO find way to set date to uint256 for solidity
gender = st.selectbox('Select gender', options=['male','female'])
weight = st.number_input('Insert patient weight in lbs', min_value=0, step=1)
height = st.number_input('Insert patient height in inches', min_value=0, step=1)
patientImage = st.file_uploader('Upload patient picture', type=["jpg", "jpeg", "png"])
if st.button('Register Patient'):
    patient_ipfs_hash = pin_patient(patientName,str(dateOfBirth),gender,weight,height, patientImage)
    patient_uri = f'ipfs://{patient_ipfs_hash}'
    tx_hash = contract.functions.registerPatient(
        address,
        patientName,
        time.mktime(dateOfBirth.timetuple()),
        patient_uri
    ).transact({'from': address, 'gas': 1000000})
    receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    st.write("Transaction receipt mined:")
    st.write(dict(receipt))
    st.write("You can view the pinned patient record with the following IPFS Gateway Link")
    st.markdown(f"[Artwork IPFS Gateway Link](https://ipfs.io/ipfs/{patient_ipfs_hash})")
st.markdown("---")

# @TODO add functions for updating patients height and weight

# Update a patients weight
st.markdown('## Update Patients Weight')
token_id = st.text_input('What is your Patient ID #')
newWeight = st.number_input('Insert new patient weight in lbs', min_value=0, step=1)
# @TODO should a notes section be added?
if st.button('Update Weight'):
    # @TODO add json update
    st.write("Patient weight has been updated")
st.markdown('---')

# Update a patients height
st.markdown('## Update Patients Height')
token_id = st.text_input('What is your Patient ID #')
newWeight = st.number_input('Insert new patient height in lbs', min_value=0, step=1)
# @TODO should a notes section be added?
if st.button('Update Height'):
    # @TODO add json update
    print("Patient height has been updated")

# @TODO add function for viewing patients record