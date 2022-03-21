import django.conf
from django.http import HttpResponse
from django.views.decorators.http import require_GET
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView

import ilmo.settings


@require_GET
def security_txt(request):
    lines = ["Contact: " + ilmo.settings.SEC_CONTACT,
             "Expires: " + ilmo.settings.SEC_EXPIRES,
             "Encryption: " + ilmo.settings.SEC_ENCRYPTION,
             "Preferred-Languages: " + ilmo.settings.SEC_LANG,
             "Scope: " + ilmo.settings.SEC_SCOPE,
             "Policy: " + ilmo.settings.SEC_POLICY
             ]
    return HttpResponse("\n".join(lines), content_type="text/plain")

#From: https://samulinatri.com/blog/django-translation/
def change_language(request):
    response = HttpResponseRedirect('/')
    if request.method == 'POST':
        language = request.POST.get('language')
        if language:
            if language != ilmo.settings.LANGUAGE_CODE and [lang for lang in ilmo.settings.LANGUAGES if lang[0] == language]:
                redirect_path = f'/{language}/'
            elif language == ilmo.settings.LANGUAGE_CODE:
                redirect_path = '/'
            else:
                return response
            from django.utils import translation
            translation.activate(language)
            response = HttpResponseRedirect(redirect_path)
#            response.set_cookie(ilmo.settings.LANGUAGE_COOKIE_NAME, language)
    return response

class HomePageView(TemplateView):

    def render_to_response(self, context, **response_kwargs):
        from django.utils import translation
        user_language = 'en-us'
        translation.activate(user_language)
        response = super(HomePageView, self).render_to_response(context, **response_kwargs)
        response.set_cookie(ilmo.settings.LANGUAGE_COOKIE_NAME, user_language)
        return response