import requests
from django.contrib import admin
from django.contrib.auth import get_permission_codename
from django.urls import reverse
from django.utils.html import format_html

from .models import Post, Category, Tag
from .adminforms import PostAdminForm
from typeidea.custom_site import custom_site

PERMISSION_API = 'http://permission.sso.com/has_perm?user={}&perm_code={}'

# TabularInline 以表格形式展现行内编辑模型
# 列是该模型的字段名，行是一条完整的数据
# StackedInline 以堆叠行是展现行内编辑模型
# 每条数据为一叠，一叠中每个字段垂直排布


class PostInline(admin.TabularInline):  # StackedInline 样式不同
    fields = ('title', 'desc')
    extra = 1  # 控制额外多几个？？？其实是在已有数据条目下额外显示几个空条目
    model = Post


@admin.register(Category, site=custom_site)
class CategoryAdmin(admin.ModelAdmin):
    # inlines 跟 fields 一样，添加了行内编辑的效果
    inlines = [PostInline, ]
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


@admin.register(Tag, site=custom_site)
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


class CategoryOwnerFilter(admin.SimpleListFilter):
    """自定义过滤器只展示当前用户分类"""
    # 展示过滤器的标题
    title = '分类过滤器'
    # 查询字符串的参数名字
    parameter_name = 'owner_category'

    def lookups(self, request, model_admin):
        return Category.objects.filter(owner=request.user).values_list(
            'id', 'name')

    def queryset(self, request, queryset):
        category_id = self.value()
        if category_id:
            return queryset.filter(category_id=self.value())
        return queryset


@admin.register(Post, site=custom_site)
class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm
    list_display = [
        'title', 'category', 'status',
        'created_time', 'owner', 'operator',
    ]
    # 哪些字段可以作为链接，点击即可进入编辑页面
    # 默认为 list_display[0]
    # 如下指定则只有通过分类才能点击编辑
    list_display_links = ['category']

    # 过滤器显示在列表页右边
    list_filter = [CategoryOwnerFilter]
    # 上方出现搜索框
    search_fields = ['title', 'category__name']

    # 上方和下方都有动作栏
    actions_on_top = True
    actions_on_bottom = True

    # 进入修改页面后，上方下方都有保存工具条
    save_on_top = True
    # 修改页面中，分类和标题展示在同一行
    # fields = (
    #     ('category', 'title'),
    #     'desc',
    #     'status',
    #     'content',
    #     'tag',
    # )
    # fields 和 exclude 能一起写吗？
    exlude = ('owner',)

    fieldsets = (
        ('基础配置', {
            'description': '基础配置描述',
            'fields': (
                ('title', 'category'),
                'status',
            ),
        }),
        ('内容', {
            'fields': (
                'desc',
                'content',
            )
        }),
        ('额外信息', {
            'classes': ('collapse',),
            'fields': ('tag',),
        })
    )

    # filter_horizontal = ('tag',)
    filter_vertical = ('tag',)

    # list_display 中展示的自定义字段
    # 用一个函数来实现，参数固定，obj 代表当前行的对象
    # 可通过 format_html 直接返回 html
    def operator(self, obj):
        return format_html(
            '<a href="{}">编辑</a>',
            # reverse 里面的东西应该是 Django 自动帮我们定义好的
            reverse('cus_admin:blog_post_change', args=(obj.id,))
        )
    operator.short_description = '操作'

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(owner=request.user)

    def has_add_permission(self, request):
        opts = self.opts
        codename = get_permission_codename('add', opts)
        perm_code = '%s.%s' % (opts.app_label, codename)
        resp = requests.get(PERMISSION_API.format(request.user.username,
                                                  perm_code))
        if resp.status_code == 200:
            return True
        else:
            return False

    class Media:
        css = {
            'all': (
                "https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/css/bootstrap.min.css",
                ),
         }
        js = ('https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/js/bootstrap.bundle.js', )
