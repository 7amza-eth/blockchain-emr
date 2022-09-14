pragma solidity ^0.5.0;

import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/token/ERC721/ERC721Full.sol";

contract EmrBlocks is ERC721Full {
    constructor() public ERC721Full("EmrBlocks", "EMRB") {}

    struct Patient {
        string name;
        uint8 dateOfBirth;
        string gender;
        uint32 weight; //lbs
        uint8 height; //inches
    }

    mapping(uint => Patient) public patientRecords;

    event Weight();//TODO update patient weight and height

//original registration of patient in database
    function registerPatient(
        address owner,
        string memory name,
        uint8  dateOfBirth,
        string memory gender,
        uint32  weight,
        uint8  height
    ) public returns (uint256) {} //TODO fill out function

    function updateWeight() public {}//TODO

    function updateHeight() public {}//TODO
}