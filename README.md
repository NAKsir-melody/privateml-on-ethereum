# privateml-on-ethereum
Proof of concept for private machine learning with ethereum(FE, MPC)

It's alpha poc, so there is many ablolute path values and not optimized connections.

Scenarios.
1. User submit encrypted private data on ethereum blockchain.
2. Blockchain forcing MPC rules to node
3. Some nodes doing tensorflow jobs for inference (FE encrypted data)
4. Encrypted result will uploaded on chain
5. only submitter can verify what is the inference result.

PoC now.
1. Setup private ethereum network
2. Deploy simplest contract
3. Modify geth to detect contract called & read filepath
4. Send transaction with python gui (web3, draw number & double click to send transaction)
4. Geth will excute script to run tensorflow 
5. Read result and upload to chain(now, in bloom filter)
6. You can translate bloom filter byte code to string (inference result)
7. using open-sourced monitoring tools

