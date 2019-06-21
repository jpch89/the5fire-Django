from django.test import TestCase, Client

from .models import Student


class StudentTestCase(TestCase):
    def setUp(self):
        Student.objects.create(
            name='tuanzi',
            sex=1,
            email='tuanzi@example.com',
            profession='码农',
            qq='666',
            phone='2333',
        )

    # 测试数据创建以及 sex 字段的正确展示
    def test_create_and_sex_show(self):
        student = Student.objects.create(
            name='datuanzi',
            sex=1,
            email='datuanzi@example.com',
            profession='大码农',
            qq='888',
            phone='8888',
        )
        self.assertEqual(student.sex_show, '男', '性别字段内容跟展示不一致！')
        # 还可以用 Django 自动生成的 get_sex_display
        # self.assertEqual(student.get_sex_display, '男', '性别字段内容跟展示不一致！')

    # 测试查询是否可用
    def test_filter(self):
        Student.objects.create(
            name='datuanzi',
            sex=1,
            email='datuanzi@example.com',
            profession='大码农',
            qq='888',
            phone='8888',
        )
        name = 'tuanzi'
        students = Student.objects.filter(name=name)
        self.assertEqual(students.count(), 1, '应该只存在一个名称为{}的记录'.format(name))

    # 测试首页的可用性
    def test_get_index(self):
        client = Client()
        response = client.get('/')
        self.assertEqual(response.status_code, 200, 'status code must be 200!')

    def test_post_student(self):
        client = Client()
        data = dict(
            name='test_for_post',
            sex=1,
            email='aaa@bb.com',
            profession='前端开发',
            qq='333',
            phone='2333',
        )
        response = client.post('/', data)
        self.assertEqual(response.status_code, 302, 'status code must be 302!')

        response = client.get('/')
        # response.content 是 bytes 类型
        self.assertTrue(b'test_for_post' in response.content,
            'response content must contain `test_for_post`')
