import requests
import time
import re

# URL = 'https://share.dmhy.org/topics/list/page/3400'
URL = 'https://share.dmhy.org/topics/list/page/3400'

re_infoURL = '<ahref="/topics/view/([\s\S]*?)"target="_blank">'
re_time = '<li>發佈時間:<span>([\s\S]*?)</span></li>'
re_type = '<tdwidth="6%"align="center"><aclass="([\s\S]*?)"href="'
re_title = '<divclass="topic-titleboxui-corner-all"><h3>([\s\S]*?)</h3>'
re_size = '<li>文件大小:<span>([\s\S]*?)</span></li>'
re_info = '<strong>簡介:&nbsp;</strong>([\s\S]*?)<a name="description-end"></a>'
re_magnet1 = '<aclass="magnet"id="a_magnet"href="([\s\S]*?)">([\s\S]*?)</a>'
re_magnet2 = '<aid="magnet2"href="([\s\S]*?)">([\s\S]*?)</a>'
re_uper = '<tdalign="center"><ahref="([\s\S]*?)">([\s\S]*?)</a></td>'
re_UDO_DATA = '<tdnowrap="nowrap"align="center"><spanclass="btl_1">([\s\S]*?)</span></td><tdnowrap="nowrap"align="center"><spanclass="bts_1">([\s\S]*?)</span></td><tdnowrap="nowrap"align="center">([\s\S]*?)</td><tdalign="center"><ahref="([\s\S]*?)">([\s\S]*?)</a></td>'
# re_UDO_DATA = '<tdnowrap="nowrap"align="center"><spanclass="btl_1">([\s\S]*?)</span></td><tdnowrap="nowrap"align="center"><spanclass="bts_1">([\s\S]*?)</span></td><tdnowrap="nowrap"align="center">([\s\S]*?)</td>'



_header = {
    # ':authority':'www.dmhy.org',
    # ':path':'/',
    # ':scheme':'https',
    # 'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    # 'accept-encoding':'gzip, deflate, br',
    # 'accept-language':'zh-CN,zh;q=0.9,en;q=0.8',
    # 'cache-control':'max-age=0',
    # 'if-modified-since':'Sat, 02 Mar 2019 15:18:33 GMT',
    # 'upgrade-insecure-requests':'1',
    # 'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
    'Referer':'https://share.dmhy.org/topics/list/sort_id/31/page/1',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
}
def time_decorator(func,**kwargs):
    """
    插入排序
    时间复杂度O（n^2）
    """
    def run_time(*args,**kwargs):
        start=time.time()
        # print 'start:', start
        func(*args,**kwargs)
        # return res
        stop=time.time()
        print('run_time:',(stop-start))
    return run_time

def clear_html_re(src_html):
    '''
    正则清除HTML标签
    :param src_html:原文本
    :return: 清除后的文本
    '''
    content = re.sub(r"</?(.+?)>", "", src_html) # 去除标签
    # content = re.sub(r"&nbsp;", "", content)
    dst_html = re.sub(r"\s+", "", content)  # 去除空白字符
    return dst_html

def getDMHY_types(_str):
    '''
    动漫花园资源类别转换
    :param _str: 字符串，传入类似“sort-2”即可
    :return: 字符串
    '''
    types = {
        'sort-2':'动画',
        'sort-31':'季度全集',
        'sort-3':'漫画',
        'sort-41':'港台漫画',
        'sort-42':'日版漫画',
        'sort-4':'音乐',
        'sort-43':'动漫音乐',
        'sort-44':'同人音乐',
        'sort-15':'流行音乐',
        'sort-6':'日剧',
        'sort-7':'生肉（RAW）',
        'sort-9':'游戏',
        'sort-17':'电脑游戏',
        'sort-18':'电视游戏',
        'sort-19':'掌机游戏',
        'sort-20':'网络游戏',
        'sort-21':'游戏周边',
        'sort-12':'特摄',
        'sort-1':'其他',
        'viewInfoURL':'https://share.dmhy.org/topics/view/',
    }

    return types[_str]

def HtmlDownloader(URL,_header):
    P = {
        "http": "http://127.0.0.1:1080",
        "https": "http://127.0.0.1:1080",
        # "https":"https://106.60.44.145:80",

    }
    # _respone = requests.get(url=URL, headers=_header,proxies=P)
    _respone = requests.get(url=URL, headers=_header)
    return _respone.text

def re_DMHY(html_text,re_pattern,nbsp_del = True):
    '''
    增则过滤函数
    :param html_text: 字符串，网页的文本
    :param re_pattern: 字符串，正则表达式
    :param nbsp_del: 布尔值，控制是否以去除换行符的形式抓取有用信息
    :return:
    '''
    pattern = re.compile(re_pattern)
    if nbsp_del:
        return pattern.findall("".join(html_text.split()))
    else:
        return pattern.findall(html_text)

@time_decorator
def main_DMHY():
    a_i_u_e_o = HtmlDownloader(URL,_header)
    ha_hi_fu_he_ho = list(map(lambda x:getDMHY_types('viewInfoURL')+x,re_DMHY(a_i_u_e_o,re_infoURL)))
    sa_shi_su_se_so = re_DMHY(a_i_u_e_o,re_type)
    upers = re_DMHY(a_i_u_e_o, re_UDO_DATA)
    for ma_mi_mu_me_mo, na_ni_nu_ne_no,UDO in zip(ha_hi_fu_he_ho, sa_shi_su_se_so,upers):
        rec_dict = {
            '类别': getDMHY_types(na_ni_nu_ne_no),
            '标题': '',
            '发布时间': '',
            '文件大小': '',
            'Magnet連接': '',
            'Magnet連接typeII': '',
            '简介': r'<div>\r\n' + '',
            '详情URL': ma_mi_mu_me_mo,
            'test': UDO,
        }
        print(rec_dict)


if __name__ == '__main__':
    main_DMHY()