// SPDX-License-Identifier: MIT

pragma solidity ^0.6.0;

contract SimpleStorage {
    uint256 favoriteNumber;
    bool favoriteBool;

    // store favorite number
    function store(uint256 _favoriteNumber) public {
        favoriteNumber = _favoriteNumber;
    }

    // get favorite number. Could be created for us by making favoriteNumber variable public, so this is uneccessary
    function retreive() public view returns (uint256) {
        return favoriteNumber;
    }

    struct Person {
        uint256 favoriteNumber;
        string name;
    }

    Person[] public people;
    mapping(string => uint256) public nameToNumber;

    // store new person in people array. Also map name to number
    function newPerson(string memory _name, uint256 _favoriteNumber) public {
        people.push(Person(_favoriteNumber, _name));
        nameToNumber[_name] = _favoriteNumber;
    }
}
