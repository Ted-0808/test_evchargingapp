pragma solidity ^0.4.20;

//this contract can be treated as the aggregator of local EV charging system, all charging points in this system share the same constraints either geographically or virtually.
but also can be further divided into several subgroups because of the existance of multiple feeders or extra source of power (PV invertor Battey storages, etc.). But as we indicated 
blockchain is only for data record purpose and all other calculation works are performed off-chain.


contract chargingPointInfo {

    enum supplyMode {AC,DC}
    enum status {Available, Occupied}

    struct ChargingPoint {
        string operator;
        string connectionType;
        supplyMode chargingType;
        uint32 maxPowerSupply;
        uint8 insPower; //real-time power supply to the EV
        uint32 latitude;
        uint32 longitude;
        uint8 chargingStatus; //0 for available and 1 for occupied
        uint32 price;

    }

    event chargingPointRegs (address CPaddr, string operator, string connectionType, supplyMode chargingType, uint32 maxPowerSupply, uint32 latitude, uint32 longitude, uint8 chargingStatus, uint32 price);

    mapping (address => ChargingPoint) ChargingPoints;
    mapping (address => uint) cpIndexArr;

    address[] public CP_list;
    uint public totalCP;

    constructor  () public {
        // position 0 occupied by invalid address
        CP_list.push(0x0);
    }


    //registration

    function setChargingPoint (string memory _operator, string memory _connectionType, supplyMode _chargingType, uint32 _maxPowerSupply, uint32 _latitude, uint32 _longitude, uint8 _chargingStatus, uint32 _price) public {
        if (!cpAddrArr(msg.sender)){
        // mapping address to index
        cpIndexArr[msg.sender]= CP_list.length;
        ChargingPoints[msg.sender]= ChargingPoint(_operator, _connectionType, _chargingType, _maxPowerSupply, _latitude, _longitude, _chargingStatus, _price);
        CP_list.push(msg.sender);
        emit chargingPointRegs(msg.sender,_operator, _connectionType, _chargingType, _maxPowerSupply,_latitude,_longitude, _chargingStatus, _price);
        }
        
        totalCP = CP_list.length -1;
    }

    //check if an address is already registered or not
    function cpAddrArr(address cpAddr) public constant returns (bool) {
        //address 0x0 is not valid if pos 0 is not in the array
        if (cpAddr != 0x0 && cpIndexArr[cpAddr]>0){
            return true;
        } else {
            return false;
        }
    }

    //get registration details
    function getChargingPointDetails () public constant returns (address, string, string, supplyMode, uint32, uint32, uint32, uint8, uint32){
        return (msg.sender, ChargingPoints[msg.sender].operator, ChargingPoints[msg.sender].connectionType, ChargingPoints[msg.sender].chargingType, ChargingPoints[msg.sender].maxPowerSupply, ChargingPoints[msg.sender].latitude, ChargingPoints[msg.sender].longitude, ChargingPoints[msg.sender].chargingStatus, ChargingPoints[msg.sender].price);
    }

    function getSpecificCPDetails (address _cpaddr) public constant returns ( string, supplyMode, uint32, uint32, uint32, uint8, uint32){
        return ( ChargingPoints[_cpaddr].connectionType, ChargingPoints[_cpaddr].chargingType, ChargingPoints[_cpaddr].maxPowerSupply, ChargingPoints[_cpaddr].latitude, ChargingPoints[_cpaddr].longitude, ChargingPoints[_cpaddr].chargingStatus, ChargingPoints[_cpaddr].price);
    }
    
    function getChargingList () public view returns (address[]){
        return CP_list;
    }
}
