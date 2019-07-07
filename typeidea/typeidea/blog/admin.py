from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import Post, Category, Tag


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    # list_display 是显示展示在列表中的列名
    list_display = ('name', 'status', 'is_nav', 'created_time', 'post_count')
    # fields 是点进去一条数据之后能够修改的字段
    fields = ('name', 'status', 'is_nav')

    # 重写 save_model 方法，以便在保存模型的时候做些额外动作
    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super().save_model(request, obj, form, change)

    def post_count(self, obj):
        """自定义列表页展示的字段"""
        return obj.post_set.count()
    post_count.short_description = '文章数量'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'created_time')
    fields = ('name', 'status')

    def save_model(self, request, obj, form, change):
        # obj 是当前要保存的对象
        # form 是传过来的表单对象
        # request 是当前请求
        # change 表示本次保存的数据是新增的还是更新的
        obj.owner = request.user
        return super().save_model(request, obj, form, change)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'category', 'status',
        'created_time', 'operator'
    ]
    # 哪些字段可以作为链接，点击即可进入编辑页面
    # 默认为 list_display[0]
    # 如下指定则只有通过分类才能点击编辑
    list_display_links = ['category']

    # 过滤器显示在列表页右边
    list_filter = ['category', ]
    # 上方出现搜索框
    search_fields = ['title', 'category__name']

    # 上方和下方都有动作栏
    actions_on_top = True
    actions_on_bottom = True

    # 进入修改页面后，上方下方都有保存工具条
    save_on_top = True
    # 修改页面中，分类和标题展示在同一行
    fields = (
        ('category', 'title'),
        'desc',
        'status',
        'content',
        'tag',
    )

    # list_display 中展示的自定义字段
    # 用一个函数来实现，参数固定，obj 代表当前行的对象
    # 可通过 format_html 直接返回 html
    def operator(self, obj):
        return format_html(
            '<a href="{}">编辑</a>',
            # reverse 里面的东西应该是 Django 自动帮我们定义好的
            reverse('admin:blog_post_change', args=(obj.id,))
        )
    operator.short_description = '操作'

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super().save_model(request, obj, form, change)
