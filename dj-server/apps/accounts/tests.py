from django.test import TestCase

from django.contrib.auth.models import User
from .models import Ip4Entry
from .utils import user_reg_ip4


class UserRegIp4TestCase(TestCase):

    fixtures = ['test_user_reg_ip4.json', ]

    def test_clear_fixture(self):
        self.assertEqual(Ip4Entry.objects.all().count(), 0)

    def test_new_entry(self):
        user = User.objects.filter(username='user1')[0]
        status = user_reg_ip4(user, '1.1.1.1')

        self.assertEqual(status, 0)
        self.assertEqual(
            Ip4Entry.objects.filter(ip_address='1.1.1.1', user=user).count(),
            1
        )

    def test_update_entry(self):

        user = User.objects.filter(username='user1')[0]
        entry = Ip4Entry(user=user, ip_address='1.1.1.1', priority=0)
        entry.save()

        status = user_reg_ip4(user, '1.1.1.1', 100)
        self.assertEqual(status, 0)

        self.assertEqual(Ip4Entry.objects.all().count(), 1)
        self.assertEqual(
            Ip4Entry.objects.filter(
                ip_address='1.1.1.1',
                user=user,
                priority=100
            ).count(),
            1
        )

    def test_replace_entry(self):

        user1 = User.objects.filter(username='user1')[0]
        user2 = User.objects.filter(username='user2')[0]

        status = user_reg_ip4(user1, '1.1.1.1')
        self.assertEqual(status, 0)
        self.assertEqual(Ip4Entry.objects.all().count(), 1)

        status = user_reg_ip4(user2, '1.1.1.1')
        self.assertEqual(status, 0)
        self.assertEqual(Ip4Entry.objects.all().count(), 1)
        self.assertEqual(
            Ip4Entry.objects.filter(ip_address='1.1.1.1', user=user2).count(),
            1
        )

    def test_replace_entry_priority(self):

        user1 = User.objects.filter(username='user1')[0]
        user2 = User.objects.filter(username='user2')[0]

        status = user_reg_ip4(user1, '1.1.1.1', 100)
        self.assertEqual(status, 0)
        self.assertEqual(Ip4Entry.objects.all().count(), 1)

        status = user_reg_ip4(user2, '1.1.1.1', 0)
        self.assertEqual(status, 1)
        self.assertEqual(Ip4Entry.objects.all().count(), 1)
        self.assertEqual(
            Ip4Entry.objects.filter(ip_address='1.1.1.1', user=user1).count(),
            1
        )

    def test_max_count_entry_1(self):

        user1 = User.objects.filter(username='user1')[0]

        status = user_reg_ip4(user1, '1.1.1.1')
        self.assertEqual(status, 0)
        self.assertEqual(Ip4Entry.objects.all().count(), 1)
        self.assertEqual(
            Ip4Entry.objects.filter(ip_address='1.1.1.1', user=user1).count(),
            1
        )

        status = user_reg_ip4(user1, '1.1.1.2')
        self.assertEqual(status, 0)
        self.assertEqual(Ip4Entry.objects.all().count(), 1)
        self.assertEqual(
            Ip4Entry.objects.filter(ip_address='1.1.1.2', user=user1).count(),
            1
        )

    def test_max_count_entry_2(self):

        user2 = User.objects.filter(username='user2')[0]

        status = user_reg_ip4(user2, '1.1.1.1')
        self.assertEqual(status, 0)
        self.assertEqual(Ip4Entry.objects.all().count(), 1)
        self.assertEqual(
            Ip4Entry.objects.filter(ip_address='1.1.1.1', user=user2).count(),
            1
        )

        status = user_reg_ip4(user2, '1.1.1.2')
        self.assertEqual(status, 0)
        self.assertEqual(Ip4Entry.objects.all().count(), 2)
        self.assertEqual(
            Ip4Entry.objects.filter(ip_address='1.1.1.2', user=user2).count(),
            1
        )

        status = user_reg_ip4(user2, '1.1.1.3')
        self.assertEqual(status, 0)
        self.assertEqual(Ip4Entry.objects.all().count(), 2)
        self.assertEqual(
            Ip4Entry.objects.filter(ip_address='1.1.1.3', user=user2).count(),
            1
        )

    def test_change_priority(self):

        user1 = User.objects.filter(username='user1')[0]

        status = user_reg_ip4(user1, '1.1.1.1')
        self.assertEqual(status, 0)
        self.assertEqual(Ip4Entry.objects.all()[0].priority, 0)

        status = user_reg_ip4(user1, '1.1.1.1', 100)
        self.assertEqual(status, 0)
        self.assertEqual(Ip4Entry.objects.all()[0].priority, 100)

    def test_replace_entry_with_priority_1(self):

        user1 = User.objects.filter(username='user1')[0]
        status = user_reg_ip4(user1, '1.1.1.1', 100)
        self.assertEqual(status, 0)
        self.assertEqual(Ip4Entry.objects.all()[0].priority, 100)

        status = user_reg_ip4(user1, '1.1.1.2', 0)
        self.assertEqual(status, 1)
        self.assertEqual(
            Ip4Entry.objects.filter(ip_address='1.1.1.1', user=user1).count(),
            1
        )

    def test_replace_entry_with_priority_2(self):

        user2 = User.objects.filter(username='user2')[0]
        status = user_reg_ip4(user2, '1.1.1.1', 100)
        self.assertEqual(status, 0)
        self.assertEqual(Ip4Entry.objects.all()[0].priority, 100)

        status = user_reg_ip4(user2, '1.1.1.2', 0)
        self.assertEqual(status, 0)
        self.assertEqual(
            Ip4Entry.objects.filter(ip_address='1.1.1.1', user=user2).count(),
            1
        )
        self.assertEqual(
            Ip4Entry.objects.filter(ip_address='1.1.1.2', user=user2).count(),
            1
        )

        status = user_reg_ip4(user2, '1.1.1.3', 0)
        self.assertEqual(status, 0)
        self.assertEqual(
            Ip4Entry.objects.filter(ip_address='1.1.1.1', user=user2).count(),
            1
        )
        self.assertEqual(
            Ip4Entry.objects.filter(ip_address='1.1.1.3', user=user2).count(),
            1
        )

    def test_decrease_priority(self):

        user = User.objects.filter(username='user1')[0]

        status = user_reg_ip4(user, '1.1.1.1', 100)
        self.assertEqual(status, 0)

        status = user_reg_ip4(user, '1.1.1.1', 0)
        self.assertEqual(status, 0)

        self.assertEqual(Ip4Entry.objects.all().count(), 1)
        self.assertEqual(
            Ip4Entry.objects.filter(
                ip_address='1.1.1.1',
                user=user,
                priority=100
            ).count(),
            1
        )
