from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template.loader import get_template

from posts.models import User


def send_find_password_email(email):
    """ 비밀번호찾기 페이지 생성 후 메일을 보댄다. """

    user_name = User.objects.get(email=email)
    d = dict({'email': email, 'user_name': user_name.user_name})
    html = get_template('users/password_reset_response.html')
    html_content = html.render(d)

    msg = EmailMultiAlternatives('Reset Your Password', '', 'hjkim880527', to=[email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
