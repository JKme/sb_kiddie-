package main

import (
	"bytes"
	"errors"
	"flag"
	"fmt"
	"log"
	"net"
	"strings"
	"sync"
	"time"
)





var wg sync.WaitGroup
var ips = make(chan string)

func oxid(ip string) error {
	dl := net.Dialer{Timeout: 5 * time.Second}

	conn, err := dl.Dial("tcp", ip+":135")

	// defer conn.Close()
	if err != nil {
		return err
	}

	_, err = conn.Write([]byte("\x05\x00\x0b\x03\x10\x00\x00\x00\x48\x00\x00\x00\x01\x00\x00\x00\xb8\x10\xb8\x10\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x01\x00\xc4\xfe\xfc\x99\x60\x52\x1b\x10\xbb\xcb\x00\xaa\x00\x21\x34\x7a\x00\x00\x00\x00\x04\x5d\x88\x8a\xeb\x1c\xc9\x11\x9f\xe8\x08\x00\x2b\x10\x48\x60\x02\x00\x00\x00"))
	if err != nil {
		return err
	}
	tmpByte := make([]byte, 1024)
	_, err = conn.Read(tmpByte)
	if err != nil {
		return err
	}
	// dcerpc finish

	// IOXIDResolve start
	_, err = conn.Write([]byte("\x05\x00\x00\x03\x10\x00\x00\x00\x18\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x05\x00"))
	if err != nil {
		return err
	}

	result := make([]byte, 4096)
	_, err = conn.Read(result)
	if err != nil {
		return err
	}
	/*
		Two parts:
			1. Distributed Computing Enviroment / Remote Prodedure Call Response
			2. DCOM OXID Resolver <- what we need
	*/

	result = result[24+12+2+2:]
	index := bytes.Index(result, []byte("\x09\x00\xff\xff\x00\x00"))
	if index == -1 {
		return errors.New("Not Found")
	}
	result = result[:index]
	results := []string{}
	for {
		if len(result) == 0 {
			break
		}
		index = bytes.Index(result, []byte("\x00\x00\x00"))
		results = append(results, dataGet(result[:index+3]))
		result = result[index+3:]
	}
	if len(results) > 0 {
		fmt.Println("[+] " + ip)
		for _, v := range results {
			fmt.Println("\t" + v)
		}
		return nil
	}
	return nil
}

func dataGet(data []byte) string {
	if bytes.HasPrefix(data, []byte("\x07\x00")) {
		return string(data[:len(data)-3])
	}
	return ""
}

func hosts(cidr string){
	if strings.Contains(cidr, "/") {
		inc := func(ip net.IP) {
			for j := len(ip) - 1; j >= 0; j-- {
				ip[j]++
				if ip[j] > 0 {
					break
				}
			}
		}
		ip, ipnet, err := net.ParseCIDR(cidr)
		if err != nil {
			log.Fatal(err)
		}

		for ip := ip.Mask(ipnet.Mask); ipnet.Contains(ip); inc(ip) {
			ips <- ip.String()
			//fmt.Printf("Add IP: %s\n",ip.String())
		}
	}
	trial := net.ParseIP(cidr)
	if trial.To4() == nil {
		//fmt.Printf("NULL IP")
	return
	}
	//fmt.Printf("Add IP: %s\n", trial.To4().String())
	ips <- trial.To4().String()
	//fmt.Printf("IPS: %v", ips)
}

//func createWorkerPool(numberWorkers int){
//	for i:=0;i<=numberWorkers;i++{
//		wg.Add(1)
//		go worker(&wg)
//	}
//}

func worker(wg *sync.WaitGroup){
	defer wg.Done()
	for ip := range ips {
			//fmt.Printf("Get IP: %s\n", ip)
		_ = oxid(ip)
	}
}

func main() {
	var (
		ip      string
		threads int
	)
	flag.StringVar(&ip, "i", "", "ip address")
	flag.IntVar(&threads, "t", 10, "threads")
	flag.Parse()
	for i:=0;i<threads;i++{
		wg.Add(1)
		go worker(&wg)
	}
	hosts(ip)
	close(ips)
	wg.Wait()
}
