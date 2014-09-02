#-*- coding:utf-8 -*-
#!/usr/bin/env python
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

from flask import Flask, request, redirect
from flask import render_template
from collections import OrderedDict
import os
import json
import requests
import re
from _base.config import WECHAT, PATH, HOST
from model.parse import verify, parse_msg, is_subscribe_event, is_text_msg, is_click_event
from model.responser import Responser, IndividualRepoter
from model.const import WELCOME_MESSAGE, INDIVIDUAL_RESPONSE
from model.user import user_rm, user_individuality_new, user_in_indivduality, user_result_dumps
from model.directory_tree import D
from model.file import folders_list, files_list, get_file_content, all_is_file
from model.decision import decision_content_dumps


app = Flask(__name__)
app.debug = True


@app.route('/')
def i_am_ok():
    return "Hello, I am ok"


@app.route('/weixin', methods=['GET'])
def access_verify():
    """ 微信认证接口
    """
    echostr = request.args.get('echostr')
    if verify(request) and echostr:
        return echostr
    raise Exception('access verification fail')


@app.route('/weixin', methods=['POST'])
def msg_handle():
    """ 处理来自用户的消息
    """
    if not verify(request):  # 如果消息不是来自微信服务器, 拒绝服务.
        raise Exception('message processing fail')

    msg = parse_msg(request.data)
    user_id = msg['FromUserName']
    Rp = Responser(msg)
    IRp = IndividualRepoter(msg, D, PATH.INDIVIDUAL_PATH)

    if is_subscribe_event(msg):  # 新用户关注
        return Rp.rp_text_msg(WELCOME_MESSAGE)

    elif is_click_event(msg):    # 用户点击了微信菜单上的click事件按钮
        if msg['EventKey'] == WECHAT.INDIVIDUAL_TOKEN:
            user_rm(user_id)
            user_individuality_new(user_id)
            return Rp.rp_text_msg(INDIVIDUAL_RESPONSE)

    elif is_text_msg(msg):
        if user_in_indivduality(user_id):   # 请求个性化告知服务
            result = IRp.individual_response()
            return Rp.rp_text_msg(result)
        else:
            return Rp.make_rp()
    raise Exception('xxx')


@app.route('/individual')
def individual():
    """个性化告知 -> 结果页
    """
    _id = request.args.get('id').encode('utf-8')
    content = '\n'.join(user_result_dumps(_id)).encode('utf-8')
    return render_template('individual.html', content=content, title='办证材料')


@app.route('/individual/decision')
def individual_decision():
    """个性化告知 -> 股东XX书
    """
    select = request.args.get('select').encode('utf-8')
    index = request.args.get('index').encode('utf-8')

    return render_template('detail.html', content=decision_content_dumps(select, int(index)))


@app.route('/guide/licence/')
def comman_tell_index():
    """办照通用指南 -> 首页
    """
    def _key(s):
        r = re.findall('\d+', s)
        return int(r[-1]) if r else -1

    data = folders_list('办照指南/办照通用指南')
    data.sort(key=_key)
    return render_template('bztyzn_index.html',
                           data=data,
                           title="办照通用指南",
                           next_route='/guide/licence/doc?file_name=',
                           )


@app.route('/guide/licence/doc')
def common_tell_doc():
    """ 办照通用指南 -> 告知单页面
    """

    path = request.args.get('file_name').encode('utf-8')
    abs_path = os.path.join('办照指南/办照通用指南/', path)
    data = OrderedDict()
    if all_is_file('content/' + abs_path):
        data[path] = files_list(abs_path)
        description = get_file_content('__readme.txt', abs_path)
    else:
        folders = folders_list(abs_path)
        for each in folders:
            if each == 'readme.txt':
                description = get_file_content(each, abs_path)
            else:
                data[each] = files_list(os.path.join(abs_path, each))

    return render_template('bztyzn_gzd.html',
                           data=data,
                           title=path[2:],
                           description=description,
                           pdf_src=HOST.QINIU,
                           next_route="/guide/licence/article?file_name="
                           )


@app.route('/guide/licence/article')
def common_tell_detail():
    """办照通用指南 -> 详情页
    """
    name = request.args.get('file_name').encode('utf-8')
    content = get_file_content(name, path="办照指南/办照通用指南")
    title = name[2:-4] if name.startswith('__') else name[3:-4]

    return render_template('detail.html', content=content, title=title)


@app.route('/guide/web_register')
def web_register():
    """网上登记
    """
    content = get_file_content('网上登记.rst', path="办照指南/网上登记")

    return render_template('detail.html', content=content, title="网上登记")


@app.route('/guide/3in1')
def _3in1():
    """三证合一办理
    """
    content = get_file_content('三证合一办理告知.rst', path="办照指南/三证合一办理")

    return render_template('detail.html', content=content, title="三证合一办理告知")


@app.route('/guide/map')
def guide_map_index():
    """我去哪儿办照 -> 首页
    """
    content = files_list('办照指南/我去哪儿办照')
    return render_template('where_to_register.html',
                           content=content,
                           title="我去哪儿办照",
                           next_route="/guide/map/detail?file_name="
                           )


@app.route('/guide/map/detail')
def guide_map_detail():
    """我去哪儿办照 -> 详情页
    """
    name = request.args.get('file_name').encode('utf-8')
    content = get_file_content(name, path="办照指南/我去哪儿办照")
    title = name[2:-4] if name.startswith('__') else name[:-4]

    return render_template('detail.html', content=content, title=title)


@app.route('/e/server')
def e_server_index():
    """微服务 -> 首页
    """
    return render_template('nav.html',
                           content=folders_list('工商e典/微服务'),
                           title="微服务",
                           next_route="/e/server/detail?file_name="
                           )


@app.route('/e/server/detail')
def e_server_detail():
    """微服务 -> 详情页
    """
    name = request.args.get('file_name').encode('utf-8')
    return render_template('detail.html',
                           content=get_file_content(name, "工商e典/微服务"),
                           title=name[2:-4]
                           )


@app.route('/e/interactive')
def e_interactive():
    """微互动
    """
    name = request.args.get('file_name')
    if not name:  # 首页
        content = files_list('工商e典/微互动')
        return render_template('nav.html',
                               content=content,
                               title="微互动",
                               next_route="/e/interactive?file_name="
                               )
    else:  # 详情页
        name = name.encode('utf-8')
        content = get_file_content(name, "工商e典/微互动")
        return render_template('detail.html', content=content, title=name[2:-4])


@app.route('/e/map')
def e_map():
    """微导航
    """
    content = get_file_content('微导航.rst', '工商e典/')
    return render_template('detail.html', content=content, title="微导航")


@app.route('/truth/outline')
def truth_outline():
    """信用查询 -> 线下信用查询
    """
    content = get_file_content('outline.rst', '信用查询')
    return render_template('detail.html', content=content, title="信用查询")


@app.route('/truth/app')
def truth_app():
    """ 信用查询 -> 信用信息APP
    """
    app_android = "http://a.app.qq.com/o/simple.jsp?pkgname=com.hyjx.main&g_f=995366"
    app_iso = "https://itunes.apple.com/cn/app/bei-jing-shi-qi-ye-xin-yong/id680476740?mt=8&ign-mpt=uo%3D4"
    ios = ['iPod', 'iPhone', 'iPad']

    if any(request.headers.get('User-Agent').find(i) != -1 for i in ios):
        return redirect(app_iso)
    else:
        return redirect(app_android)


@app.route('/map')
def map():
    """百度地图导航页面
    """
    def geocoder(key):
        url = "http://api.map.baidu.com/geocoder?address={}&output=json".format(key)
        r = requests.get(url)
        c = json.loads(r.text)
        if c['result']:
            return c['result']['location']

    title = request.args.get('title').encode('utf-8')
    key = request.args.get('key').encode('utf-8')
    location = geocoder(key)

    return render_template('baidu_map.html',
                           title=title,
                           key=key,
                           lng=location['lng'],
                           lat=location['lat']
                           )


# 需要时使用
# @app.route('/article')
# def article():
#     """图文信息或其它article的展示页面
#     """
#     name = request.args.get('article_name').encode('utf-8')
#     content = get_file_content(name, 'article')
#     return render_template('detail.html', content=content, title=name)


from bae.core.wsgi import WSGIApplication
application = WSGIApplication(app)
# if __name__ == '__main__':
#     app.run()
