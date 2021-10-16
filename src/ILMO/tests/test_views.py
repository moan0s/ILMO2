from http import HTTPStatus
from django.test import SimpleTestCase
from datetime import datetime

class SecurityTxtTests(SimpleTestCase):
    def test_get(self):
        response = self.client.get("/.well-known/security.txt")

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response["content-type"], "text/plain")
        content = response.content.decode()

        # Check that security contact is correct
        self.assertTrue(content.startswith("Contact: mailto: julian-samuel@gebuehr.net"))

        # Check that security.txt is not expired
        lines = content.split("\n")
        expire_line = lines[1]
        date_string = expire_line.split(" ")[1]
        format = "%Y-%m-%dT%H:%M:%S.000Z"
        date = datetime.strptime(date_string, format)
        self.assertTrue(datetime.now() < date)

    def test_post_disallowed(self):
        response = self.client.post("/.well-known/security.txt")

        self.assertEqual(HTTPStatus.METHOD_NOT_ALLOWED, response.status_code)