# coding: utf-8
from burp import IBurpExtender, IBurpExtenderCallbacks, IScannerCheck, IHttpRequestResponse, IScanIssue
from java.io import PrintWriter
import re
from urlparse import urlparse, parse_qs

WHITE_DOMAIN = ["example.com"]


class BurpExtender(IBurpExtender, IScannerCheck):
    PLUGIN_NAME = "Authentication checker"
    COMMENT = "Created by REST API Plugin"

    def registerExtenderCallbacks(self, callbacks):
        self._callbacks = callbacks
        self._helpers = callbacks.getHelpers()
        callbacks.setExtensionName(self.PLUGIN_NAME)
        self.stdout = PrintWriter(callbacks.getStdout(), True)

        self._callbacks.registerScannerCheck(self)
        self.stdout.println("{}\n".format(self.PLUGIN_NAME))

    ''' List<IScanIssue> doPassiveScan(IHttpRequestResponse baseRequestResponse); '''

    def doPassiveScan(self, baseRequestResponse):
        # print "Do PassiveScan"
        req_info = self._helpers.analyzeRequest(baseRequestResponse)
        headers = req_info.getHeaders()
        headers_new = list(filter(lambda x: False if "Cookie" in x or "Authorization" in x else True, headers))

        req_body = baseRequestResponse.getRequest()[req_info.getBodyOffset():]
        base_uri = req_info.getUrl().getPath()
        host = baseRequestResponse.getHttpService().getHost()
        # print "Host: %s" % ()
        top_domain = '.'.join(host.split('.')[-2:])

        if len(headers) != len(headers_new) and not check_list(base_uri) and top_domain in WHITE_DOMAIN:
            modifiedRequestResponse = self._callbacks.makeHttpRequest(baseRequestResponse.getHttpService(),
                                                                      self._helpers.buildHttpMessage(headers_new,
                                                                                                     req_body))
            modified_response_info = self._helpers.analyzeResponse(modifiedRequestResponse.getResponse())

            base_response_info = self._helpers.analyzeResponse(baseRequestResponse.getResponse())
            # res_headers = base_response_info.getHeaders()
            # val = check_headers(res_headers.toString())

            # print "type: %s \n headers: %s" % (type(res_headers), res_headers)
            self.stdout.println("{} {} - {}".format(req_info.getUrl(), base_response_info.getStatusCode(),
                                                    modified_response_info.getStatusCode()))
            if base_response_info.getStatusCode() == modified_response_info.getStatusCode():
                return [CustomScanIssue(
                    baseRequestResponse.getHttpService(),
                    req_info.getUrl(),
                    [baseRequestResponse],
                    "Breaking Authorization", "The request can be executed without authorization",
                    "High")]

    def doActiveScan(self, baseRequestResponse, insertionPoint):
        return None

    def consolidateDuplicateIssues(self, existingIssue, newIssue):
        return 0


def check_list(headers):
    pattern = re.compile(r".*js|.*css|.*png|.*map|.*woff$|.*NoAuth$|.*ico$|.*HOME$")
    match = re.search(pattern, headers)
    if match:
        return True
    else:
        return False


#
# class implementing IScanIssue to hold our custom scan issue details
#

class CustomScanIssue(IScanIssue):
    def __init__(self, httpService, url, httpMessages, name, detail, severity):
        self._httpService = httpService
        self._url = url
        self._httpMessages = httpMessages
        self._name = name
        self._detail = detail
        self._severity = severity

    def getUrl(self):
        return self._url

    def getIssueName(self):
        return self._name

    def getIssueType(self):
        return 0

    def getSeverity(self):
        return self._severity

    def getConfidence(self):
        return "Certain"

    def getIssueBackground(self):
        pass

    def getRemediationBackground(self):
        pass

    def getIssueDetail(self):
        return self._detail

    def getRemediationDetail(self):
        pass

    def getHttpMessages(self):
        return self._httpMessages

    def getHttpService(self):
        return self._httpService
    # def processHttpMessage(self, toolFlag, messageIsRequest, messageInfo):
    #     if toolFlag == 4:
    #         if not messageIsRequest:
    #             response = messageInfo.getResponse()  # get response
    #             analyzedResponse = self._helpers.analyzeResponse(response)
    #             body = response[analyzedResponse.getBodyOffset():]
    #             body_string = body.tostring()  # get response_body
    #
    #             request = messageInfo.getRequest()
    #             analyzedRequest = self._helpers.analyzeResponse(request)
    #             request_header = analyzedRequest.getHeaders()
    #             try:
    #                 method, path = res_path.findall(request_header[0])[0]
    #                 host = res_host.findall(request_header[1])[0]
    #                 url = messageInfo.getUrl().toString()
    #             except:
    #                 url = ""
    #             print "Check Url: %s" % url
    # if method == "GET":
    #     # 检测GET请求的接口
    #     print "[Info]Check url is ", url
    #     cur = noauth_request(host, path, body_string)
    #     noauth_result = cur.run()
    #     if noauth_result:
    #         print "[Info]Found it is a noauth Interface %s" % noauth_result[0][0]
    #         print "[Info]remove param is ", noauth_result[0][1]
    #     print "======================================================================================"
