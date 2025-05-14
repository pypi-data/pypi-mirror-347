import urllib3

from yplib import *
from yplib import sort_by_json_key
from yplib.common_package import *

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 有关 http 的工具类


# 创建一个线程本地存储对象
__THREAD_LOCAL_HTTP_UTIL_DATA = threading.local().data = {}


def save_data_to_thread_local(headers_save=None,
                              headers=None,
                              BASE_URL=None):
    if headers_save:
        # 保存 headers
        __THREAD_LOCAL_HTTP_UTIL_DATA['headers_save'] = headers
    headers = headers if headers is not None else __THREAD_LOCAL_HTTP_UTIL_DATA.get('headers_save', None)

    r_list = [headers]
    # 输出非空字段
    for key, value in {
        'BASE_URL': BASE_URL,
    }.items():
        this_key = f'{key}__{key}'
        value_temp = value if value is not None else __THREAD_LOCAL_HTTP_UTIL_DATA.get(this_key, None)
        __THREAD_LOCAL_HTTP_UTIL_DATA[this_key] = value_temp
        r_list.append(value_temp)
    return r_list


def do_parser(file_path=None, html_data='', selector=None):
    """
    解析 html 中的数据
    file_path :   html 文件的路径
    html_data :   html 数据
    selector  :   选择器
    """
    if file_path is not None:
        html_str = ''.join(to_list(file_path))
    else:
        if isinstance(html_data, list):
            html_str = ''.join(html_data)
        else:
            html_str = str(html_data)
    return BeautifulSoup(html_str, 'html.parser').select(selector)


# div_list_content = do_parser(r'D:\notepad_file\202306\asfdf.html', selector='table.reference')[4].select('tr')
#
# for i in range(len(div_list_content) - 1):
#     td = div_list_content[i + 1].select('td')
#     num = td[0].text
#     fun_name = td[1].select('a')[0].text
#     fun_desc = td[1].text.replace(fun_name, '')
#     print(f'{num} : {fun_name} , {fun_desc}')


def do_get_response(url=None,
                    session=None,
                    headers=None,
                    cookie=None,
                    auth=None,
                    timeout=1000,
                    verify=False):
    """
    get 类型的请求
    session : session , 默认 : requests.session()
    headers : headers
    cookie  : cookie
    auth    : auth
    verify  : verify
    r_json : 返回的数据是否是一个 json 类型的数据
    """
    if session is None:
        session = requests.session()
    # requests.packages.urllib3.disable_warnings()
    return session.get(url=url, headers=headers, auth=auth, timeout=timeout, verify=verify, cookies=cookie)


def do_get(url=None,
           BASE_URL=None,
           param=None,
           data=None,
           session=None,
           headers=None,
           headers_save=False,
           cookie=None,
           auth=None,
           timeout=1000,
           verify=False,
           r_json=True):
    '''
    param : 都是参数
    data  : 都是参数
    headers_save  : headers save 保存在 __THREAD_LOCAL_HTTP_UTIL_DATA 中, 下次请求的时候, 会自动带上
    '''
    [headers, BASE_URL] = save_data_to_thread_local(headers_save=headers_save,
                                                    headers=headers,
                                                    BASE_URL=BASE_URL)
    if url.startswith(BASE_URL):
        BASE_URL = ''
    url = ('' if BASE_URL is None else BASE_URL) + url
    start_time = time.time()
    parts = [sort_by_json_key(d, sep='&', join='=', join_list=',') for d in [param, data] if d is not None]
    if parts:
        url += '?' + '&'.join(parts)

    response = do_get_response(url=url, session=session, headers=headers, cookie=cookie, auth=auth, timeout=timeout, verify=verify)
    response.encoding = 'utf-8'
    r1 = json.loads(response.text.strip()) if r_json else response.text.strip()

    # for log 部分
    do_http_log(url=url,
                param=param,
                data=data,
                session=session,
                headers=headers,
                cookie=cookie,
                response=response,
                response_text=r1,
                method='get',
                elapsed_time_ms=to_int((time.time() - start_time) * 1000),
                r_json=r_json)

    return r1


# 返回的是一个 json 数据
def do_get_json(url=None,
                param=None,
                data=None,
                session=None,
                headers=None,
                headers_save=False,
                cookie=None,
                auth=None,
                timeout=1000,
                verify=False):
    return do_get(url=url,
                  param=param,
                  data=data,
                  session=session,
                  headers=headers,
                  headers_save=headers_save,
                  cookie=cookie,
                  auth=auth,
                  timeout=timeout,
                  verify=verify,
                  r_json=True)


def do_download(url=None,
                file_name=None,
                file_path='download',
                session=None,
                headers=None,
                cookie=None,
                auth=None,
                timeout=1000,
                verify=False):
    r"""
    下载
    file_name   : 文件名 , 默认 txt
                  当文件名是 C:\Users\yangpu\Desktop\study\abc\d\e\f\a.txt 这种类型的时候, 可以直接创建文件夹,
                      会赋值 file_path=C:\Users\yangpu\Desktop\study\abc\d\e\f,
                            file_name=a.txt,
                            fixed_name=True
                  当文件名是 abc 的时候, 按照正常值,计算
    file_path   : 文件路径
    """
    if session is None:
        session = requests.session()
    # requests.packages.urllib3.disable_warnings()
    response = session.get(url=url, headers=headers, auth=auth, timeout=timeout, verify=verify, cookies=cookie)
    if response.status_code != 200:
        to_log_file('error', url, response.status_code)
        return
    # 默认的文件路径,
    file_name = url[url.rfind('/') + 1: len(url)] if file_name is None else file_name
    if file_name is not None:
        file_name = str(file_name)
        for sep in ['\\', '/']:
            # C:\Users\yangpu\Desktop\study\abc\d\e\f\a.txt
            f_n = file_name.split(sep)
            if len(f_n) > 1:
                # a.txt
                file_name = f_n[-1]
                # C:\Users\yangpu\Desktop\study\abc\d\e\f
                file_path = sep.join(f_n[0:-1])
    # 检查路径 file_path
    while file_path.endswith('/'):
        file_path = file_path[0:-1]
    check_file(file_path)
    # 去掉文件名称中的非法字符
    file_name = re.sub('[^a-zA-Z0-9._]', '', file_name)
    path_name = file_path + '/' + file_name
    # 重复下载的删掉以前的
    if os.path.exists(path_name):
        os.remove(path_name)
    # 下载的文件
    with open(path_name, 'wb') as f:
        f.write(response.content)
    # 返回全路径名称, 文件名, 路径名
    return path_name, file_name, file_path


# print(do_download('https://www.runoob.com/?s=sorted', r'C:\Users\yangpu\Desktop\study\abc\d\e\f\a.txt'))
# print(do_get('https://www.runoob.com/?s=sorted'))
# print(do_get('http://10.6.180.156:18000/login/need'))
# print(do_get('http://10.6.180.156:18000/login/need', r_json=True))


def do_post_response(url=None,
                     data=None,
                     is_form_data=False,
                     session=None,
                     headers=None,
                     cookie=None,
                     auth=None,
                     timeout=1000,
                     verify=False):
    """
    post 类型的请求
    data         : data post 体中的数据
    is_form_data : 是否是 form 表单
    headers      : headers
    cookie       : cookie
    auth         : auth
    verify       : verify
    r_json       : 返回的数据是否是一个 json 类型的数据
    """
    # headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    # data = {}
    # data['appkey'] = APP_KEY
    # data['secretkey'] = SECRET_KEY
    # data['content'] = content
    # data['phone'] = obtainMobileIndonesia(mobile)
    # requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    # response = requests.post(URL, headers=headers, verify=False, data=data)
    # response.encoding = 'utf-8'
    # text = response.text
    # text = text.replace('\n', '')
    # text = text.replace('\r', '')
    # return text
    if session is None:
        session = requests.session()
    # requests.packages.urllib3.disable_warnings()
    d = data if is_form_data else json.dumps(data)
    headers = {} if headers is None else headers
    content_type = headers['Content-Type'] if 'Content-Type' in headers else 'application/json;charset=UTF-8'
    if 'Content-Type' not in headers and is_form_data:
        content_type = 'application/x-www-form-urlencoded'
    headers['Content-Type'] = content_type
    return session.post(url=url, data=d, headers=headers, auth=auth, timeout=timeout, verify=verify, cookies=cookie)


def do_post(url=None,
            BASE_URL=None,
            data=None,
            param=None,
            is_form_data=False,
            session=None,
            headers=None,
            headers_save=False,
            cookie=None,
            auth=None,
            timeout=1000,
            verify=False,
            r_json=True):
    start_time = time.time()
    p_list = [x for x in [param, data] if x is not None]
    p = p_list[0] if p_list else None

    [headers, BASE_URL] = save_data_to_thread_local(headers_save=headers_save,
                                                    headers=headers,
                                                    BASE_URL=BASE_URL)
    if url.startswith(BASE_URL):
        BASE_URL = ''
    url = ('' if BASE_URL is None else BASE_URL) + url
    response = do_post_response(url=url,
                                data=p,
                                is_form_data=is_form_data,
                                session=session,
                                headers=headers,
                                cookie=cookie,
                                auth=auth,
                                timeout=timeout,
                                verify=verify)
    response.encoding = 'utf-8'
    r1 = json.loads(response.text.strip()) if r_json else response.text.strip()

    # for log 部分
    do_http_log(url=url,
                param=param,
                data=data,
                session=session,
                headers=headers,
                cookie=cookie,
                response=response,
                response_text=r1,
                method='post',
                elapsed_time_ms=to_int((time.time() - start_time) * 1000),
                r_json=r_json)
    return r1


def do_http_log(url=None,
                param=None,
                data=None,
                session=None,
                headers=None,
                cookie=None,
                response=None,
                response_text=None,
                method=None,
                elapsed_time_ms=None,
                r_json=False):
    # for log 部分
    temp = get__thread_local_index_data()
    flag = temp.get('_use_fun_flag', False)
    if not flag:
        return
    log_fun = temp['_use_fun']
    log_fun('', line_with_space_count=1)
    # 日志字段列表
    log_fields = {
        'url': [url, False],
        'method': [str(method).upper() if method is not None else method, False],
        'session': [session, False],
        'headers': [headers, True],
        'cookie': [cookie, False],
        'request_data': [data, True],
        'request_param': [param, True],
        'response': [response, False],
        'elapsed_time_ms': [elapsed_time_ms, False],
    }
    # 输出非空字段
    for key, [value, flag] in log_fields.items():
        if value is not None:
            if flag:
                log_fun(f'{key}:')
                r_temp = json.dumps(value, indent=4, ensure_ascii=False, sort_keys=True)
                r_temp = rreplace(r_temp, '\n}', '\n }', 1)
                log_fun(r_temp)
            else:
                log_fun(f'{key}:', value)
    # 输出响应正文
    log_fun('response_text:')
    r_temp = json.dumps(response_text, indent=4, ensure_ascii=False, sort_keys=True) if r_json else response_text
    r_temp = rreplace(r_temp, '\n}', '\n }', 1)
    log_fun(r_temp)
    log_fun(f'{str(method).upper() if method is not None else method}__END')
    log_fun()
    log_fun('####################################################################################################', line_with_space_count=-1)
