from django.shortcuts import render, HttpResponse

# Create your views here.

# 构造要发送的消息
user_dict = {
    'username': 'tom',
    'sex': 'male',
    'age': 18
}
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
# 通过添加装饰器来跳过csrf验证
@csrf_exempt
def usersList(request):

    # 用return HttpResponse(user_dict)返回的不是一个完整的数据，需要重新发送JSON格式对的数据
    # 通过json.dumps(user_dict)
    if request.method == 'GET':
        return HttpResponse(json.dumps(user_dict), content_type='application/json')

    if request.method == 'POST':
        # print(request.POST)
        # 基于Django原生方式实现API ，Django自带解析器
        # 解析器: 解析用户发过来HTTP报文的工具，解析为能够使用的格式，如字典，字符串。。。
        # 没有解析之前在request.body里面, 解析完后放在request.POST里面。Django自带的解析器无法解析JSON类型的报文
        '''
        第一种： 
            data = json.loads(request.body.decode('utf-8'))
            decode()转化为字符串了
            通过json.loads()转化为字典
            根据drf要求，post请求的数据需要返回回去
            return HttpResponse(json.dumps(data), content_type='application/json')
        第二种：
            通过JsonResponse
        '''
        data = json.loads(request.body.decode('utf-8'))

        return JsonResponse(data)


"""
API的本质：
1.后端要接受一个RESTful规范的url,以及json的数据
2.解析JSON数据，做相应的处理
3.生产JSON的数据
4.返回数据和状态码
"""