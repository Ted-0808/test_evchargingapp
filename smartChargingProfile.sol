pragma solidity ^0.4.20;

import "./CP_DB.sol" ;


contract smartCharging is chargingPointInfo{
    
    string public message;
    uint powerLimit;
    uint powerDemand;
    uint chargingTime;
    uint numOfCP;
    address contractOwner;
    //status of CP
    
    mapping (address => uint) ChargingPower;
    
    // assign the total registered CPs from the other contract to numOfCP
    constructor () public {
        powerLimit = 50;
        numOfCP = totalCP;
        powerDemand = 0;
        contractOwner = msg.sender;
       
    }
    
    modifier onlyAggragator () {
        require (msg.sender == contractOwner);
        _;
    }
    modifier checkBalance (){
        require (msg.value >= 0.01 ether);
        _;
    }
    
    
    //set by DSO
    function setPowerLimit (uint _powerLimit) public onlyAggragator {
        powerLimit = _powerLimit;
    }
    
    //EV user can submit charging request
    function userInput(address cpAddress, uint _energyDemand, uint _chargingTime) public payable checkBalance returns (bool decision){
        uint avgDemand;
        avgDemand = _energyDemand/_chargingTime;
        chargingTime = _chargingTime;
        
        if (avgDemand> (powerLimit-powerDemand)){
            return false;
        }
        else {
            powerDemand += avgDemand;
            ChargingPoints[cpAddress].chargingStatus = 1;
            ChargingPower[cpAddress] = avgDemand;
            return true;
        }
    }
    
    function getData () view returns(uint){
        return powerDemand;
    }

    function endCharging (address _cpAddress) public {
        
        powerDemand -= ChargingPower[_cpAddress];
        ChargingPoints[_cpAddress].chargingStatus = 0;
    }
}
