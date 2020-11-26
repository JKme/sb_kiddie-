#include "windows.h"
#include "winhttp.h"
#include "wchar.h"
#include "wincrypt.h"
#include <comdef.h>
#include <string>
#include <vector>
#include "atlconv.h"

#pragma comment(lib, "Winhttp.lib")
using namespace std;


string https_post(string key)
{
	string strHost = "example.com";
	string strRequestStr = "/";
	string data = "a=b";
	strRequestStr.append(key);
	string header = "Host: example.cloudfront.net\r\nContent-type: application/x-www-form-urlencoded\r\nCache-Control: max-age=0\r\nAccept-Encoding: gzip, deflate\r\nAccept-Language: zh-CN,zh;q=0.8\r\n";
	USES_CONVERSION;
	LPCWSTR host = A2CW(strHost.c_str());
	LPCWSTR requestStr = A2CW(strRequestStr.c_str());
	LPCWSTR dataStr = A2CW(data.c_str());
	//Variables
	DWORD dwSize = 0;
	DWORD dwDownloaded = 0;
	LPSTR pszOutBuffer;
	vector <string>  vFileContent;
	//BOOL  bResults = FALSE;

	HINTERNET  hSession = NULL,
		hConnect = NULL,
		hRequest = NULL;
	string strHtml = "";// store the html code
	hSession = WinHttpOpen(L"Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36 Core/1.53.2141.400 QQBrowser/9.5.10219.400",
		WINHTTP_ACCESS_TYPE_DEFAULT_PROXY,
		WINHTTP_NO_PROXY_NAME,
		WINHTTP_NO_PROXY_BYPASS, 0);
	// Specify an HTTP server.  INTERNET_DEFAULT_HTTP_PORT
	if (hSession)
		hConnect = WinHttpConnect(hSession, host,
			INTERNET_DEFAULT_HTTPS_PORT, 0);
	// Create an HTTP request handle.
	if (hConnect)
		hRequest = WinHttpOpenRequest(hConnect, L"POST", requestStr,
			NULL, WINHTTP_NO_REFERER,
			WINHTTP_DEFAULT_ACCEPT_TYPES,
			WINHTTP_FLAG_SECURE);

	// if (hConnect)
	// 	hRequest = WinHttpOpenRequest(hConnect, L"GET", requestStr,
	// 		NULL, WINHTTP_NO_REFERER,
	// 		WINHTTP_DEFAULT_ACCEPT_TYPES,
	// 		NULL);


	DWORD dwFlags =
		SECURITY_FLAG_IGNORE_UNKNOWN_CA |
		SECURITY_FLAG_IGNORE_CERT_WRONG_USAGE |
		SECURITY_FLAG_IGNORE_CERT_CN_INVALID |
		SECURITY_FLAG_IGNORE_CERT_DATE_INVALID;

	DWORD dwTimeOut = 3000;
	BOOL bResults = WinHttpSetOption(hRequest, WINHTTP_OPTION_CONNECT_TIMEOUT, &dwTimeOut, sizeof(DWORD));

	bResults = WinHttpSetOption(hRequest, WINHTTP_OPTION_SECURITY_FLAGS, &dwFlags, sizeof(dwFlags));
	bResults = WinHttpSetOption(hRequest, WINHTTP_OPTION_CLIENT_CERT_CONTEXT, WINHTTP_NO_CLIENT_CERT_CONTEXT, 0);


	//Add HTTP header 
	LPCWSTR header1 = A2CW(header.c_str());
	SIZE_T len = lstrlenW(header1);

	WinHttpAddRequestHeaders(hRequest, header1, DWORD(len), WINHTTP_ADDREQ_FLAG_ADD);

	// Send a request.
	if (hRequest)
		bResults = WinHttpSendRequest(hRequest,
			WINHTTP_NO_ADDITIONAL_HEADERS,
			0, (LPVOID)data.c_str(), data.length(),
			data.length(), 0);
	// if (hRequest)
	// 	bResults = WinHttpSendRequest(hRequest,
	// 		WINHTTP_NO_ADDITIONAL_HEADERS,
	// 		0, NULL, 0,
	// 		0, 0);

	// End the request.
	if (bResults)
		bResults = WinHttpReceiveResponse(hRequest, NULL);

	//obtain the html source code
	if (bResults)
		do
		{
			// Check for available data.
			dwSize = 0;
			if (!WinHttpQueryDataAvailable(hRequest, &dwSize))
				printf("Error %u in WinHttpQueryDataAvailable.\n",
					GetLastError());


			pszOutBuffer = new char[dwSize + 1];
			if (!pszOutBuffer)
			{
				printf("Out of memory\n");
				dwSize = 0;
			}
			else
			{
				// Read the Data.
				ZeroMemory(pszOutBuffer, dwSize + 1);
				if (!WinHttpReadData(hRequest, (LPVOID)pszOutBuffer,
					dwSize, &dwDownloaded))
				{
					printf("Error %u in WinHttpReadData.\n",
						GetLastError());
				}
				else
				{
					//printf("%s", pszOutBuffer);
				   // Data in vFileContent
					vFileContent.push_back(pszOutBuffer);

				}
				// Free the memory allocated to the buffer.
				delete[] pszOutBuffer;
			}
		} while (dwSize > 0);
		// Keep checking for data until there is nothing left.
	   // Report any errors.
		if (!bResults)
			printf("Error %d has occurred.\n", GetLastError());
		// Close any open handles.
		if (hRequest) WinHttpCloseHandle(hRequest);
		if (hConnect) WinHttpCloseHandle(hConnect);
		if (hSession) WinHttpCloseHandle(hSession);

		for (int i = 0; i < (int)vFileContent.size(); i++)
		{
			string str = "";
			str = vFileContent[i];
			strHtml += vFileContent[i];

		}
		// debug http response
		//std::cout << strHtml << "\n";
		printf("Content: %s\n", strHtml.c_str());
		return strHtml;
}

int main() {

	https_post("123");
}