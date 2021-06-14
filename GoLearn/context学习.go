
package main

import (
	"context"
	"fmt"
	"sync"
	"time"
)

func someHandler() {
	// 创建继承Background的子节点Context
	ctx, cancel := context.WithCancel(context.Background())
	go doSth(ctx)

	//模拟程序运行 - Sleep 5秒
	time.Sleep(5 * time.Second)
	cancel()
	time.Sleep(1 * time.Second)
}

//每1秒work一下，同时会判断ctx是否被取消，如果是就退出
func doSth(ctx context.Context) {
	var i = 1
	for {
		time.Sleep(1 * time.Second)
		select {
		case <-ctx.Done():
			fmt.Println("done")
			return
		default:
			fmt.Printf("work %d seconds: \n", i)
			return
		}
		i++
	}
}

func doTask(ctx context.Context, task chan int, do chan bool){
	for {
		select {
		case data, _ := <- task:
			if data>0{
				fmt.Printf("[*]: Working: %v\n", data)
				if data == 200 {
					fmt.Printf("Working Done %v\n", data)
					time.Sleep(3 * time.Second)
					do <- true
					return
				}
			}
			case <- ctx.Done():
				return
		}
	}
}

func monitor(do chan bool, wg *sync.WaitGroup){
	defer  wg.Done()
	for {
		select {
		case data, ok := <- do:
			if ok{
				fmt.Printf("Get Result %v\n", data)
				close(do)

				return
				//return
			}
		default:

		}

	}
}

//func monitor (do chan bool, wg *sync.WaitGroup){
//	defer  wg.Done()
//	for {
//		select {
//		case data, ok := <- do:
//			if ok{
//				fmt.Printf("Get Result %v\n", data)
//				close(do)
//				return
//				//return
//			}
//		default:
//
//		}
//
//	}
//}

func work(data int, do  chan bool){
	if data == 200 {
		fmt.Printf("Working Done %v\n", data)
		time.Sleep(3 * time.Second)
		do <- true
	}
}

func main() {
	//fmt.Println("start...")
	//for i:=0;i<4;i++ {
	//	go someHandler()
	//}
	//time.Sleep(3 * time.Second)
	//fmt.Println("end.")
	//var wg sync.WaitGroup

	var do = make(chan bool, 2)
	var ch = make(chan int, 120)

	ctx, cancel := context.WithCancel(context.Background())


	for i:=10;i<103;i++ {
		ch <- i
	}
	close(ch)

	//for i:=0;i<2;i++ {
	//	go doTask(ctx, ch, do)
	//}

	go func() {
		for {
			select {
			case data, ok := <- do:
				if ok{
					fmt.Printf("Get Result %v\n", data)
					close(do)
					cancel()

					//break
				}
			case <- ctx.Done():

			}
		}}()


Loop:
	for data := range ch{
			fmt.Printf("Start: %v\n", data)
			time.Sleep(1 * time.Second)
			if data == 29 {
				fmt.Printf("Working Done %v\n", data)
				time.Sleep(3 * time.Second)
				do <- true
				break Loop
			}
		}
	}
	//for {
	//	select {
	//	case data, _ := <- ch:
	//		if data>0{
	//			fmt.Printf("[*]: Working: %v\n", data)
	//			if data == 110 {
	//				fmt.Printf("Working Done %v\n", data)
	//				time.Sleep(3 * time.Second)
	//				do <- true
	//				break Loop
	//			}
	//		}
	//	case <- ctx.Done():
	//		return
	//	}
	//}

	//
	//	for {
	//		select {
	//		case data, ok := <- ch:
	//			if ok{
	//				fmt.Printf("[*]: Working: %v\n", data)
	//				time.Sleep( 2 * time.Second)
	//				//work(data)
	//				doTask(ctx, ch, do)
	//
	//			}
	//		default:
	//
	//			}
	//		}
	//
	//	}
	//
