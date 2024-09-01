// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.13;

library Secp256k1 {
    function verify(address signer, bytes32 digest, bytes memory sig) internal pure returns (bool) {
        uint8 v;
        bytes32 r;
        bytes32 s;
        assembly {
            v := mload(add(sig, 1))
            r := mload(add(sig, 33))
            s := mload(add(sig, 65))
        }
        return signer == ecrecover(digest, v, r, s);
    }
}

contract KeyManager {
    
    // Owner is responsible for initializing
    address owner;
    constructor () {
	owner = msg.sender;
    }

    // Anyone can see the master public key
    address public xPub;

    ///////////////////////////////////
    // EVM-Friendly remote attestation
    ///////////////////////////////////

    /* The sig is obtained by calling
        dstack-keymanager/attest/<appdata> */
    function verify(string memory caller, bytes32 appData, bytes memory sig) public view returns (bool) {
        bytes32 digest = keccak256(abi.encodePacked(caller, appData));
        return Secp256k1.verify(xPub, digest, sig);
    }
    

    //////////////////////////////
    // Bootstrapping
    //////////////////////////////
    /*
      The bootstrap phase is called by the owner, just once,
      and sets the master public key. The significance of this
      is that the remote attestation
     */

    event BootstrapComplete(address xPub); 
    function bootstrap(address _xPub) public {
	require(msg.sender == owner);
        require(xPub == address(0)); // only once
	require(_xPub != address(0));
        xPub = _xPub;
	emit BootstrapComplete(xPub);
    }

    //////////////////////////////
    // New node register phase
    //////////////////////////////
    /*
    struct TcbInfo {
	bytes16 fmspc;
	bytes32 mrtd;
    }
    mapping(bytes32 => TcbInfo) registry;

    function register(bytes32 myPub) public {
        //require(keccak256(registry[addr]) == keccak256(bytes("")));
        //require(Suave.verifySgx(address(this), keccak256(abi.encodePacked("myPub", myPub, addr)), att));
    }

    event Onboard(bytes32 myPub, bytes resp);
    function onboard(bytes32 myPub, bytes16 fmspc, bytes32 mrtd,
		     bytes memory resp, bytes memory att) public
    {
	bytes32 appdata = keccak256(abi.encodePacked("onboard",myPub,resp));
	require(verify("dstack-keymanager", appdata, att));
	
	// We can process each in turn
	registry[myPub].fmspc = fmspc;
        registry[myPub].mrtd = mrtd;
	
	emit Onboard(myPub, resp);
    }

    // 3. Node completes on boarding
    event Onboard(address addr, bytes ciphertext);
    function onchain_Onboard(address addr, bytes memory ciphertext) public {
        // Note: nothing guarantees all ciphertexts on chain are valid
        emit Onboard(addr, ciphertext);
    }*/
}
