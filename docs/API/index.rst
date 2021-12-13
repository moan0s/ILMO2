*****************
API Documentation
*****************

ILMOs API serves the purpose of supporting 3rd-person applications and anything you can think of basically.

.. warning::
    The current API is limited in it's functionality. I you miss a specific feature please contact the developer!

API Access
==========

Via browser
-----------

When a user is logged in, they can easily access the API in their browser, authenticated by their session.
The API endpoint can be found at /library/api/
http://example.com:8000/library/api/book

Via token
---------

All users are able to generate a token that allows them to use the API. This can be done in the user's profile.
An application can then send this token in the request header for authorization.

.. code-block::
    $ curl -X GET http://localhost:8000/library/api/book -H 'Authorization: Token 49b39856955dc6e5cc04365498d4ad30ea3aed78'



Access Control
==============
The API allows to query permissions to access rooms. E.g. a IoT device could query this information and decided to open a door or a key locker.
Currently the user can be queried via a UID.

A typical request Looks like this:
.. code-block::
    GET /library/api/uid/1234456/room/dbc71599-a0ce-482f-a896-6f4a7dfc17ec






