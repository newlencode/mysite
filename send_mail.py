import os
from django.core.mail import EmailMultiAlternatives

os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'

if __name__ == '__main__':

    subject, from_email, to = '来自jackpardon的测试邮件', 'jackpardon@sina.com', 'c7877@qq.com'
    text_content = '欢迎访问jackpardond的站点'
    html_content = '<p>欢迎访问<a href="http://www.liujiangblog.com" target=blank>www.liujiangblog.com</a>，这里是jackpardon的博客和教程站点</p>'
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()