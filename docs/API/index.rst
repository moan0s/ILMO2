*****************
API Documentation
*****************

ILMOs API serves two different purposes. The first is to make data available to the public. The seconde is to track working hours and opening status.


Make Data Publicly Available
============================

Example Use-Case:
-----------------

You have a department/club/etc.. homepage that is run by a Content Management System like Wordpress
and want to show which books are in the library available. ILMO is hosted on a different Website.
One line of plain html code is enough to do what you want!

Simply include

.. code::

        <iframe src="https://example.com/index.php?ac=open_show_small_plain" width="100%" height="270"></iframe>

Show all books
--------------

Show all material
-----------------

Track Working Hours and Opening Status
======================================

This part of the API offers the possibility to track working hours via a suitable IoT Device (e.g.
a Raspberry Pi with NFC Reader.

.. hint::
   This part of the API has to be activated in the settings!

Example Use Case
----------------

You have a library in your that is run by two students that need to track the hours they worked.
Writing this down is way too easy and you want a live update when they are present so ILMO shows
that someone is there. ILMO offers the possibility to checkin someone via an API. You therefore
adapt the provided example script, so the students can use their student ID and a NFC reader that
is connected to a Raspberry Pi to identify and checkin themselves.

Access Control
==============
This part of the API offers the possibility to control the access for an optional key locker via a suitable device.
This device sends a message to the server and get back whether the person is allowed to lend a key or not. All access tries are logged and can be shown by an administrator. The permission of each user can be set during the user registration and in the user settings. It is also necessary to set the UID of each user as it is necessary to identify the user.

.. hint::
   This part of the API has to be activated in the settings!

Settings
----------------
You can send the UID of the RFID card coded in the URL. For safety reasons it is also necessary to send an access key in the request. The access key can be set in the settings. Optional you can send the status of the key (key available or not). The default value is 0.

Arguments:
ac=check_access
UID="Number of the UID"
access_key="Access key as set in settings
key_available="0 or 1, if not set 0"
The URL could be: http://localhost/ilmo/index.php?ac=check_acess&UID=1234&acess_key=1234568&key_available=1





