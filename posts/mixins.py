from django.http import JsonResponse

from posts import models


class AjaxFormMixin(object):

    def form_invalid(self, form):
        response = super(AjaxFormMixin, self).form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        response = super(AjaxFormMixin, self).form_valid(form)
        if self.request.is_ajax():
            email = form.cleaned_data["email"]
            name = form.cleaned_data["name"]
            user_name = form.cleaned_data["user_name"]
            password1 = form.cleaned_data["password1"]
            clean_user = models.User.objects.create_user(email, name, user_name, password1)
            clean_user.save()

            data = {'message': email+"으로 가입에 성공했습니다."}
            return JsonResponse(data)
        else:
            return response
