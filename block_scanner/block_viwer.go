package main

import (
	"context"
	"github.com/ethereum/go-ethereum/ethclient"
	"fmt"
	"math/big"
	"os"
	"strconv"
)

func main() {
	var block_start = os.Args[1];
	var block_end = os.Args[2];
	i, _ := strconv.Atoi(block_start);
	j, _ := strconv.Atoi(block_end);
	ScanBlock(int64(i), j)
}
// major
func ScanBlock(nBlock int64, count int) {
	ctx := context.Background();
	client, err := ethclient.DialContext(ctx, "http://127.0.0.1:8080")
	if err != nil {
		fmt.Println("rpc conn error")
		return
	}
	defer client.Close()

	for i := 0; i< count; i++ {
	b_num := big.NewInt(nBlock + int64(i))
	block, err := client.BlockByNumber(ctx,b_num)
	if err != nil {
		fmt.Println("block get failed")
		return
	}

	fmt.Println("=======Block Info=======")
	fmt.Println(nBlock + int64(i))
	fmt.Println(block.Time())
	fmt.Println(block.Difficulty())
	//block_hash := block.Hash()
	block_body := block.Body()

		fmt.Println("======Transaction========")
	for no, tx := range block_body.Transactions {
		fmt.Println(no ,tx.Hash().Hex())
		from, err := client.TransactionSender(ctx, tx, block.Hash(),uint(no))
		if(err == nil){
			fmt.Println("from: ",from.Hex())
		}
		if tx.To() != nil {
			fmt.Println("to: ",tx.To().Hex())
		} else {
			fmt.Println("to: 0 - contract creation")
		}
		result := tx.Value()
		fmt.Println("value: ",result)
		fmt.Println("data: ",tx.Data())
	}
	}
}


