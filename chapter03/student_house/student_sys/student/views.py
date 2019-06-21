from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View

from .forms import StudentForm
from .models import Student


class IndexView(View):
    # 这里写了 template_name 就不用在下面写两次了
    template_name = 'index.html'

    def get_context(self):
        students = Student.get_all()
        context = {
            'students': students,
        }
        return context

    def get(self, request):
        context = self.get_context()
        form = StudentForm()
        context.update({
            'form': form,
        })

        return render(request, self.template_name, context)

    def post(self, request):
        form = StudentForm(request.POST)
        if form.is_valid():
            # 校验的事情已经在 forms 中做好，这里只要保存即可
            form.save()
            # return HttpResponseRedirect(reverse('index'))
            # 其实像下面这样简写就可以了，不用 reverse
            return HttpResponseRedirect('index')

        context = self.get_context()
        context.update({
            'form': form,
        })

        return render(request, self.template_name, context)
