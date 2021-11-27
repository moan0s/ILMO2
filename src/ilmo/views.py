from django.http import HttpResponse
from django.views.decorators.http import require_GET

@require_GET
def security_txt(request):
    lines = ["Contact: mailto: julian-samuel@gebuehr.net",
             "Expires: 2022-11-28T07:00:00.000Z",
             "Encryption: https://hyteck.de/julian-samuel@gebuehr.net.pub.asc",
             "Preferred-Languages: en, de",
             "Scope: The provided contact is the main developer of the application and NOT necessarily the instance "
             "admin.",
             "Policy: Do NOT include user data or detailed reports (especially public or unencrypted) without being "
             "asked to do so. "
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")