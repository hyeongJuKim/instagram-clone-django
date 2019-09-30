from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template.loader import get_template
from django.utils.http import int_to_base36

from posts.models import User


def send_find_password_email(email):
    """ 비밀번호찾기 페이지 생성 후 메일을 보댄다.
        성공여부를 Return 한다.
    """

    user = None

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return False

    token = default_token_generator.make_token(user)

    d = dict({'email': email, 'user_name': user.user_name, 'token': token})
    html = get_template('users/password_reset_response.html')
    html_content = html.render(d)

    msg = EmailMultiAlternatives('Reset Your Password', '', 'hjkim880527', to=[email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()

    return True
