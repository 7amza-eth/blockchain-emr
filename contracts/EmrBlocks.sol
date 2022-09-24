pragma solidity ^0.5.0;

import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/token/ERC721/ERC721Full.sol";

contract EmrBlocks is ERC721Full {
    constructor() public ERC721Full("EmrBlocks", "EMRB") {}

    struct Patient {
        string name;
        uint256 dateOfBirth;
    }

    mapping(uint => Patient) public patientRecords;


//original registration of patient in database
    function registerPatient(
        address owner,
        string memory name,
        uint256  dateOfBirth,
        string memory patientURI
    ) public returns (uint256) {
        uint256 tokenId = totalSupply();

        _mint(owner, tokenId);
        _setTokenURI(tokenId, patientURI);

        patientRecords[tokenId] = Patient(name, dateOfBirth);

        return tokenId;

    }
}