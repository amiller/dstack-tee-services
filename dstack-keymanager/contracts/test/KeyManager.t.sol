// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.13;

import {Test, console} from "forge-std/Test.sol";
import {KeyManager} from "../src/KeyManager.sol";
import "forge-std/Vm.sol";

contract KeyManagerTest is Test {
    KeyManager public keymgr;

    Vm.Wallet alice;
    Vm.Wallet bob;
    Vm.Wallet carol;

    function setUp() public {
        vm.prank(vm.addr(uint(keccak256("KeyManager.t.sol"))));
        keymgr = new KeyManager();

        alice = vm.createWallet("alice");
        bob = vm.createWallet("bob");
    }

    function test_bootstrap() public {
	// 1. Bootstrap
	// 1a. Simulate invoking /dstack-keymanager/bootstrap
        Vm.Wallet memory xPub = vm.createWallet("masterkey");
	// quote = ffi fetch a tdx attestation

        // 1b. Post the key and attestation on-chain
        keymgr.bootstrap(xPub.addr);

        // 2. Register a new node
        // 2a. Simulate invoking /dstack-keymanager/register
	Vm.Wallet memory myPub = vm.createWallet("ephem");
	bytes32 mPub = bytes32(myPub.publicKeyX);
	// quote = ffi fetch a tdx attestation

	// 2b. Onchain submit the request
        keymgr.register(mPub);

        // 3. Help onboard a new node
        // 3a. Offchain generate a ciphertext with the key
        //bytes memory ciphertext = 
	
        // 3b. Onchain post the ciphertext
        //keymgr.onboard(bob_kettle, ciphertext);
    }
    
}
