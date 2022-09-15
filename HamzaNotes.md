- Basic functions  
	- Mint: creation of users NFT along with entry of basic info  
		- ERC721 token Save info as a JSON on ipfs along with their picture  
			- Info: Name, Gender, Age, Weight, Height, Medications (Basics for mvp)  
	- Update data: User (possibly doctor?) is able to update data to their record  and see history (similar to appraisal in art registry)  
	- Add viewer: user is able to address of someone to view  
- Breakdown of product:  
	- Frontend  
		- Streamlit app where all functions are accessible (possibly split into 2 apps similar to contracts below)  
	- Backend  
		- Main (admin) contract for mint and add user  
		- secondary (user) contract that access and update the data to be displayed in streamlit  
- To be researched:  
	- Can you upload to IPFS straight from streamlit or does it have to be run through a contract?
		A: If we can upload the file to a local path, then we can upload the file using the Pinata API.

	- Token-gating/limit the access to the data (submarine)  
		A: 

	- How to update the IPFS entries when the use updates their date through dApp  
		A: When the file is modified, a new CID is generated and the reference to the file chances. Same with a folder/directory, when the folder or its content changes, the resulting token changes. 
		As an alternative, we can:
			a) Upload the EMR content as a JSON part of the metadata. This way the metadata can be edited and the file will remain the same, keeping its signature.
			b) Get the file from the IPFS, edit it, delete the Pinata copy, upload a new copy and renew the the signature.
			