import os
import json
from turtle import update
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st
import time
from pinata import pin_file_to_ipfs, pin_json_to_ipfs, convert_data_to_json, hash_json_metadata

load_dotenv()

# Define and connect a new Web3 provider
w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))

# Loads contract using cache and connect ausing ddress and ABI
@st.cache(allow_output_mutation=True)
# # def load_contract():
# #     with open(Path('./contracts/compiled/emrblocks_abi.json')) as f:
# #         contract_abi = json.load(f)
# #     contract_address = os.getenv("SMART_CONTRACT_ADDRESS")
# #     contract = w3.eth.contract(
# #         address=contract_address,
# #         abi=contract_abi
# #     )
# #     return contract
# # contract = load_contract()

# IPFS helper functions
def pin_patient(patientName,dateOfBirth,gender,weight,height, patientImage):
    #pin patient image
    ipfs_file_hash = pin_file_to_ipfs(patientImage.getvalue())
    #build an patient metadata JSON file
    # 'image': ipfs_file_hash,
    patientJSON = {
        'name': patientName,
        'DOB': dateOfBirth,
        'gender': gender,
        'weight': weight,
        'height': height
    }
    
    # json_data = convert_data_to_json(patientJSON)
    payload = {
        'pinataOptions': {
            'cidVersion': 1
        },
        'pinataMetadata': {
            'name': f'{patientName} EMRB',
            'keyvalues': patientJSON
        },
        'pinataContent': {
            'image': f'https://ipfs.io/ipfs/{ipfs_file_hash}'
        }
    }

    json_data = json.dumps(payload)

    #pin patient json file
    ipfs_json_hash = pin_json_to_ipfs(json_data)
    return ipfs_json_hash

### Streamlit Frontend

# Account and Function selection
st.sidebar.title('Blockchain EMR System')
st.sidebar.write('Choose an account to get started')
accounts = w3.eth.accounts
address = st.sidebar.selectbox('Select Account', options=accounts)
st.markdown('---')
st.sidebar.write('Select a function from the dropdown menu below')
menu = ['Register Patient', 'Update Patient Info', 'View Patient Info']
function = st.sidebar.selectbox('Menu', options=menu)


# Register New Patient
if function == 'Register Patient':
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
        # # tx_hash = contract.functions.registerPatient(
        # #     address,
        # #     patientName,
        # #     time.mktime(dateOfBirth.timetuple()),
        # #     patient_uri
        # # ).transact({'from': address, 'gas': 1000000})
        # # receipt = w3.eth.waitForTransactionReceipt(tx_hash)
        st.write("Transaction receipt mined:")
        # st.write(dict(receipt))
        st.write("You can view the pinned patient record with the following IPFS Gateway Link")
        st.markdown(f"[EMRB IPFS Gateway Link](https://ipfs.io/ipfs/{patient_ipfs_hash})")
    st.markdown("---")

# Update Patient Info
elif function == 'Update Patient Info':
    #choose patient to be updated
    st.title('Update Patient Info')
    tokens = contract.functions.balanceOf(address).call()
    token_id = st.selectbox("Select which patient's info you would like to update", list(range(tokens)))
    retrieve_uri = contract.functions.patientURI(token_id).call()
    # @TODO finish token selection

    # Update a patients weight
    st.markdown('## Update Patients Weight')
    #token_id = st.text_input('What is your Patient ID # (EMRB CID)')
    newWeight = st.number_input('Insert new patient weight in lbs', min_value=0, step=1)
    # @TODO should a notes section be added?
    if st.button('Update Weight'):
        payload = json.dumps({
            "ipfsPinHash": token_id,
            "name": f'{patientName} EMRB',
            "keyvalues": {
                "weight": newWeight
            }
        })

        update_result = hash_json_metadata(payload)
        st.write(f"Patient weight has been updated: {update_result}")
    st.markdown('---')

    # Update a patients height
    st.markdown('## Update Patients Height')
    #token_id = st.text_input('What is your Patient ID #')
    newHeight = st.number_input('Insert new patient height in inches', min_value=0, step=1)
    # @TODO should a notes section be added?
    if st.button('Update Height'):
        payload = json.dumps({
            "ipfsPinHash": token_id,
            "name": f'{patientName} EMRB',
            "keyvalues": {
                "height": newHeight
            }
        })
        update_result = hash_json_metadata(payload)
        print(f"Patient height has been updated: {update_result}")

# @TODO add function for viewing patients record
elif function == 'View Patient Info':
    # @TODO token selection from within patients address
    st.markdown('## View Patient Info')
    tokens = contract.functions.totalSupply().call()
    token_id = st.selectbox("Select your Patient ID", list(range(tokens)))
    if st.button("Retrieve Patient Info"):
        retrieve_uri = contract.functions.patientURI(token_id).call()
        st.write(retrieve_uri)