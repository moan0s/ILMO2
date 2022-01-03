import django.conf
from django.http import HttpResponse
from django.views.decorators.http import require_GET

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
class HomePageView(TemplateView):

    def render_to_response(self, context, **response_kwargs):
        from django.utils import translation
        user_language = 'en-us'
        translation.activate(user_language)
        response = super(HomePageView, self).render_to_response(context, **response_kwargs)
        response.set_cookie(ilmo.settings.LANGUAGE_COOKIE_NAME, user_language)
        return response
