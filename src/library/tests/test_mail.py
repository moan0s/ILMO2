import datetime
from django.core import mail
from django.contrib.auth.models import User
from django.test import TestCase
from datetime import date, timedelta
from django.urls import reverse
from django.utils import timezone

from library.models import Loan, Book, Member, Author, BookInstance
from library.mail import MailReminder


class MailTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        test_author = Author.objects.create(first_name="Jane", last_name="Doe")
        b = Book.objects.create(title="How to Test",
                                summary="How to write better tests than you do",
                                isbn="1234567890123")
        b.author.add(test_author)
        cls.bookInstanceA = BookInstance.objects.create(book=b, label="T 1 a")
        cls.bookInstanceB = BookInstance.objects.create(book=b, label="T 1 b")
        cls.bookInstanceC = BookInstance.objects.create(book=b, label="T 1 c")
        cls.bookInstanceD = BookInstance.objects.create(book=b, label="T 1 d")

        cls.u = User.objects.create_user('foo', password='bar',
                                         first_name="user",
                                         last_name="1",
                                         email="test_user_1@example.com")
        cls.u2 = User.objects.create_user('foo2',
                                          password='bar2',
                                          first_name="user",
                                          last_name="2",
                                          email="test_user_2@example.com")  # One loan
        cls.u3 = User.objects.create_user('foo3',
                                          password='bar3',
                                          first_name="user",
                                          last_name="3",
                                          email="test_user_3@example.com")  # No loans
        cls.u4 = User.objects.create_user('foo4',
                                          password='bar4',
                                          first_name="user",
                                          last_name="4")  # No email
        cls.bookInstanceA.borrow(Member.objects.get(user=cls.u),
                                 due_back=date.today(),
                                 lent_on=date.today()-timedelta(days=99))
        cls.bookInstanceB.borrow(Member.objects.get(user=cls.u),
                                 due_back=date.today(),
                                 lent_on=date.today()-timedelta(days=99))
        cls.bookInstanceC.borrow(Member.objects.get(user=cls.u2),
                                 due_back=date.today(),
                                 lent_on=date.today()-timedelta(days=99))
        cls.bookInstanceD.borrow(Member.objects.get(user=cls.u2),
                                 due_back=date.today(),
                                 lent_on=date.today()-timedelta(days=99))

    def test_email_text_from_loan(self):
        loanA = Loan.objects.get(item=self.bookInstanceA)
        loan_text = MailReminder._email_text_from_loan(loanA)
        self.assertEquals(f"[T 1 a] How to Test by Jane Doe is due back on {date.today().strftime('%-d.%-m.%Y')}", loan_text)

    def test_gen_loan_text(self):
        reminder = MailReminder()
        loan_text = reminder._gen_loan_text(Member.objects.get(user=self.u))
        self.assertIn("[T 1 a]", loan_text)
        self.assertIn("[T 1 b]", loan_text)

    def test_gen_messages(self):
        reminder = MailReminder()
        messages = reminder._gen_messages()
        self.assertEquals(len(messages), 2)
        self.assertEquals(['test_user_1@example.com'], messages[0].to)
        self.assertIn("[T 1 c]", messages[1].body)

    def test_send(self):
        reminder = MailReminder()
        reminder.send()
        self.assertEqual(len(mail.outbox), 2)
        self.assertEqual(mail.outbox[0].subject, 'Your unreturned loans')
        self.assertEqual(['test_user_1@example.com'], mail.outbox[0].to)
        self.assertEqual(Loan.objects.get(item=self.bookInstanceA).last_reminder, timezone.now().date())

    def test_index_send(self):
        test_user1 = User.objects.create_user(username='testuser1', password='12345')
        test_user2 = User.objects.create_user(username='testuser2', password='12345', is_staff=True)

        # Test with user that has no admin permissions
        login = self.client.login(username='testuser1', password='12345')
        response = self.client.get(reverse('library:index'))
        self.assertEqual(len(mail.outbox), 0)

        # Test with user that has no admin permissions
        login = self.client.login(username='testuser2', password='12345')
        response = self.client.get(reverse('library:index'))
        self.assertEqual(len(mail.outbox), 2)
