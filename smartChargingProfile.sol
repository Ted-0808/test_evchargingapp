pragma solidity ^0.4.20;

import "./first.sol" ;


contract smartCharging is chargingPointInfo{
    
    string public message;
    uint powerLimit;
    uint powerDemand;
    uint chargingTime;
    uint numOfCP;
    address contractOwner;
    uint test;
    //status of CP
    
    // mapping (address => uint) ChargingPower; on the other contract
    
    // assign the total registered CPs from the other contract to numOfCP
    constructor ()  public {
        powerLimit = 50;
        numOfCP = totalCP;
        powerDemand = 10;
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
    
    //to calculate current total load from all CPs
    function totalLoad () public {
        for (uint i=1;i<CP_list.length;i++ ){
            powerDemand += ChargingPower[CP_list[i]];
            
        }
    }
    
    //EV user can submit charging request
    function userInput(address cpAddress, uint _energyDemand, uint _chargingTime) public payable returns (bool decision){
        uint avgDemand;
        avgDemand = _energyDemand/_chargingTime;
        chargingTime = _chargingTime;
        if (avgDemand> (powerLimit-powerDemand)){
            return false;
        }
        else {
            ChargingPoints[cpAddress].chargingStatus = 1;
            ChargingPower[cpAddress] = avgDemand;
            powerDemand =0;
            totalLoad();
            return true;
        }
        
    }

    function getData ()  public view returns(uint){

        return powerDemand;
    }
    
    function getCPList () public view returns (address[]){
        return CP_list;
    }

    function endCharging (address _cpAddress) public {
        
        ChargingPower[_cpAddress] = 0;
        ChargingPoints[_cpAddress].chargingStatus = 0;
    }
    
    function getSpecificCHargingPower (address _cpAddress) public view returns (uint){
        return ChargingPower[_cpAddress];
    }
}
