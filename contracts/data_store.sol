pragma solidity ^0.4.8;

contract datastore {
	mapping (int => string) public datastores;
	
	function setData(int a, string data) public {
		datastores[a] = data;
	}
	function getData(int a) public constant returns (string data) {
		return datastores[a];
	}
}

