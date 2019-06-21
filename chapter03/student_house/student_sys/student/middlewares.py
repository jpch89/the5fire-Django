import time

from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin


class TimeItMiddleware(MiddlewareMixin):
    # 请求来到中间件经历的第一个方法
    # 1. 返回 HttpResponse，接下来只会执行 process_response
    # 2. 返回 None，继续执行其他方法
    # 注意：如果中间件是 settings 中的第一个，其他中间件不会执行
    def process_request(self, request):
        self.start_time = time.time()
        return

    # process_request 之后进入这个方法
    # 返回 HttpResponse 或者 None，逻辑和 process_request 一样
    # 返回 None 的话 Django 会帮你执行 view 函数，得到最终的 response
    def process_view(self, request, func, *args, **kwargs):
        if request.path != reverse('index'):
            return None

        start = time.time()
        response = func(request)
        costed = time.time() - start
        print('process view: {:.2f}s'.format(costed))
        return response

    # 如果 response 使用了模板，会进入这个方法
    # 即该 response 是通过 render(request, template, context) 形式产生的
    def process_template_response(self, request, response):
        return response

    # 最后进入这个方法，逻辑和前面一样，只不过前面针对使用了模板的 response
    def process_response(self, reqeust, response):
        costed = time.time() - self.start_time
        print('request to response code: {:.2f}s'.format(costed))
        return response

    # 发生异常时进入
    # 但是如果手动调用了视图，比如在 process_view 调用了 func 则不会触发
    # 可以选择处理异常，返回带有异常信息的 HttpResponse
    # 或者直接返回 None 不处理，这样 Django 会使用自己的异常模板
    def process_exception(self, request, exception):
        pass


# class MiddlewareMixin(object):
#     def __init__(self, get_response=None):
#         self.get_response = get_response
#         super(MiddlewareMixin, self).__init__()

#     def __call__(self, request):
#         response = None
#         if hasattr(self, 'process_request'):
#             response = self.process_request(request)
#         if not response:
#             response = self.get_response(request)
#         if hasattr(self, 'process_response'):
#             response = self.process_response(request, response)
#         return response
