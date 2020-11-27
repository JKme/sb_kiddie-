#include <strsafe.h>
#include <tchar.h>
#include <windows.h>
#include <Tlhelp32.h>

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

int _tmain(int argc, _TCHAR* argv[])
{
	TCHAR tmp[500] = { 0 };
	HANDLE hProcess, hAccessToken;
	TCHAR InfoBuffer[20000] = { 0 };
	PTOKEN_USER ptiUser = NULL;
	DWORD cbti;
	SID_NAME_USE snu;
	//hProcess = GetCurrentProcess();
	hProcess = OpenProcess(MAXIMUM_ALLOWED, FALSE, GetProcessIdByName(L"explorer.exe"));
	BOOL opt = OpenProcessToken(hProcess, TOKEN_READ, &hAccessToken);
	DWORD gle = GetLastError();
	CloseHandle(hProcess);
	if (!opt)
	{
		// MessageBox calls out of this program are a bad idea - they're here for illustration only. When this 
		// runs as a CA from the local system account, it's worse. 
		StringCchPrintf(tmp, sizeof(tmp) / sizeof(TCHAR), TEXT("OpenProcessToken returned %d "), gle);
		MessageBox(NULL, tmp, TEXT("Error"), MB_OK | MB_SERVICE_NOTIFICATION);
		return 0;
	}
	ptiUser = (PTOKEN_USER)HeapAlloc(GetProcessHeap(), 0, 1000);
	BOOL gti = GetTokenInformation(hAccessToken, TokenUser, ptiUser, 1000, &cbti);
	gle = GetLastError();
	CloseHandle(hAccessToken);
	if (!gti)
	{
		StringCchPrintf(tmp, sizeof(tmp) / sizeof(TCHAR), TEXT("GetTokenInformation  returned %d "), gle);
		MessageBox(NULL, tmp, TEXT("Error"), MB_OK | MB_SERVICE_NOTIFICATION);
		return 0;
	}
	// Retrieve user name and domain name based on user's SID.
	TCHAR szUser[100] = { 0 };
	DWORD cchuser = sizeof(szUser) / sizeof(TCHAR);
	TCHAR szDomain[100] = { 0 };
	DWORD cchdom = sizeof(szDomain) / sizeof(TCHAR);
	BOOL lua = LookupAccountSid(NULL, ptiUser->User.Sid, szUser, &cchuser, szDomain, &cchdom, &snu);
	gle = GetLastError();
	if (!lua)
	{
		StringCchPrintf(tmp, sizeof(tmp) / sizeof(TCHAR), TEXT("LookupAccountSID returned %d "), gle);
		MessageBox(NULL, tmp, TEXT("Error"), MB_OK | MB_SERVICE_NOTIFICATION);
		return 0;
	}

	MessageBox(NULL, szUser, szDomain, MB_OK | MB_SERVICE_NOTIFICATION);
	return 0;
}
