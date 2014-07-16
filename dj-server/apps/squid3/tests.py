from django.test import TestCase

from .utils import extruct_domain, extruct_l2_domain
from .cache import UserCache, DomainCache, DomainFilterCache


class ExtructDomainTestCase(TestCase):

    def test_simple(self):

        # http
        domain_name = extruct_domain('http://test')
        self.assertEqual(domain_name, 'test')

        domain_name = extruct_domain('http://test.test')
        self.assertEqual(domain_name, 'test.test')

        domain_name = extruct_domain('http://test.test.test')
        self.assertEqual(domain_name, 'test.test.test')

        # https
        domain_name = extruct_domain('https://test')
        self.assertEqual(domain_name, 'test')

        domain_name = extruct_domain('https://test.test')
        self.assertEqual(domain_name, 'test.test')

        domain_name = extruct_domain('https://test.test.test')
        self.assertEqual(domain_name, 'test.test.test')

    def test_digit(self):

        # http
        domain_name = extruct_domain('http://test1')
        self.assertEqual(domain_name, 'test1')

        domain_name = extruct_domain('http://test1.1test1.1test1')
        self.assertEqual(domain_name, 'test1.1test1.1test1')

        domain_name = extruct_domain('http://1.2.3.4')
        self.assertEqual(domain_name, '1.2.3.4')

        # https
        domain_name = extruct_domain('https://test1')
        self.assertEqual(domain_name, 'test1')

        domain_name = extruct_domain('https://test1.1test1.1test1')
        self.assertEqual(domain_name, 'test1.1test1.1test1')

        domain_name = extruct_domain('https://1.2.3.4')
        self.assertEqual(domain_name, '1.2.3.4')

    def test_sym(self):

        # http
        domain_name = extruct_domain('http://_test1_')
        self.assertEqual(domain_name, '_test1_')

        domain_name = extruct_domain('http://1-tes_t1._1test1.1test1__')
        self.assertEqual(domain_name, '1-tes_t1._1test1.1test1__')

        domain_name = extruct_domain('http://_1._2_._3_._4_')
        self.assertEqual(domain_name, '_1._2_._3_._4_')

        # https
        domain_name = extruct_domain('https://_test1_')
        self.assertEqual(domain_name, '_test1_')

        domain_name = extruct_domain('https://1-tes_t1._1test1.1test1__')
        self.assertEqual(domain_name, '1-tes_t1._1test1.1test1__')

        domain_name = extruct_domain('https://_1._2_._3_._4_')
        self.assertEqual(domain_name, '_1._2_._3_._4_')

    def test_port(self):

        # http
        domain_name = extruct_domain('http://test:8080')
        self.assertEqual(domain_name, 'test')

        domain_name = extruct_domain('http://test.test:8080')
        self.assertEqual(domain_name, 'test.test')

        domain_name = extruct_domain('http://test.test.test:8080')
        self.assertEqual(domain_name, 'test.test.test')

        # https
        domain_name = extruct_domain('https://test:8080')
        self.assertEqual(domain_name, 'test')

        domain_name = extruct_domain('https://test.test:8080')
        self.assertEqual(domain_name, 'test.test')

        domain_name = extruct_domain('https://test.test.test:8080')
        self.assertEqual(domain_name, 'test.test.test')

    def test_complex(self):

        # http
        domain_name = extruct_domain('http://test:8080/1/2/3/4')
        self.assertEqual(domain_name, 'test')

        domain_name = extruct_domain('http://test.ru:8080/fdf/dfdf/dfd/121f')
        self.assertEqual(domain_name, 'test.ru')

        domain_name = extruct_domain('http://_test.ru_:8080/fdf/dfdf/dfd/121f')
        self.assertEqual(domain_name, '_test.ru_')

        domain_name = extruct_domain('http://1.2.3.4:8080/fdf/dfdf/dfd/121f')
        self.assertEqual(domain_name, '1.2.3.4')

        # https
        domain_name = extruct_domain('https://test:8080/1/2/3/4')
        self.assertEqual(domain_name, 'test')

        domain_name = extruct_domain('https://test.ru:8080/fdf/dfdf/dfd/121f')
        self.assertEqual(domain_name, 'test.ru')

        domain_name = extruct_domain('https://_test.ru_:8080/fdf/dfdf/dfd/')
        self.assertEqual(domain_name, '_test.ru_')

        domain_name = extruct_domain('https://1.2.3.4:8080/fdf/dfdf/dfd/')
        self.assertEqual(domain_name, '1.2.3.4')


class ExtructL2DomainTestCase(TestCase):

    def test_simple(self):

        domain_name = extruct_l2_domain('test')
        self.assertEqual(domain_name, None)

        domain_name = extruct_l2_domain('test.test')
        self.assertEqual(domain_name, 'test.test')

        domain_name = extruct_l2_domain('test.test.test')
        self.assertEqual(domain_name, 'test.test')

    def test_digit(self):

        domain_name = extruct_l2_domain('test1')
        self.assertEqual(domain_name, None)

        domain_name = extruct_l2_domain('test1.1test2.1test3')
        self.assertEqual(domain_name, '1test2.1test3')

        domain_name = extruct_l2_domain('1.2.3.4')
        self.assertEqual(domain_name, '3.4')

    def test_sym(self):

        domain_name = extruct_l2_domain('_test1_')
        self.assertEqual(domain_name, None)

        domain_name = extruct_l2_domain('1-tes_t1._1test1.1test1__')
        self.assertEqual(domain_name, '_1test1.1test1__')

        domain_name = extruct_l2_domain('_1._2_._3_._4_')
        self.assertEqual(domain_name, '_3_._4_')


class DomainCacheTestCase(TestCase):

    def test_simple(self):
        cache = DomainCache()

        domain = cache.get_domain('abc.def.ghi')
        self.assertEqual(domain.name, 'abc.def.ghi')
        self.assertEqual(domain.l2_domain.l2_name, 'def.ghi')

    def test_loops(self):
        cache = DomainCache()

        domain = cache.get_domain('abc.def.ghi')
        self.assertEqual(cache.miss_count, 1)
        pk = domain.pk
        for i in xrange(1000):
            domain = cache.get_domain('abc.def.ghi')
            self.assertEqual(domain.pk, pk)
            self.assertEqual(cache.miss_count, 1)

        domain = cache.get_domain('aaa.bbb.ccc')
        self.assertEqual(cache.miss_count, 2)
        pk = domain.pk
        for i in xrange(1000):
            domain = cache.get_domain('aaa.bbb.ccc')
            self.assertEqual(domain.pk, pk)
            self.assertEqual(cache.miss_count, 2)


class UserCacheTestCase(TestCase):

    def test_simple(self):
        cache = UserCache()

        user = cache.get_user_by_ip('0.0.0.0')
        self.assertEqual(user, None)

    def test_loops_cache_miss(self):
        cache = UserCache()

        for i in xrange(1000):
            cache.get_user_by_ip('0.0.0.0')
            self.assertEqual(cache.miss_count, 1)

        for i in xrange(1000):
            cache.get_user_by_ip('0.0.0.1')
            self.assertEqual(cache.miss_count, 2)

        cache.clear()

    def test_loops_no_cache_miss(self):
        cache = UserCache(cache_miss=False)
        miss = 0

        for i in xrange(1000):
            cache.get_user_by_ip('0.0.0.0')
            miss += 1
            self.assertEqual(cache.miss_count, miss)

        for i in xrange(1000):
            cache.get_user_by_ip('0.0.0.1')
            miss += 1
            self.assertEqual(cache.miss_count, miss)

        cache.clear()


class DomainFilterCacheTestCase(TestCase):

    class FakeUser(object):
        def __init__(self, pk):
            super(DomainFilterCacheTestCase.FakeUser, self).__init__()
            self.pk = pk

    class FakeDomain(object):
        def __init__(self, pk):
            super(DomainFilterCacheTestCase.FakeDomain, self).__init__()
            self.pk = pk

    def get_user(self, pk):
        return DomainFilterCacheTestCase.FakeUser(pk)

    def get_domain(self, pk):
        return DomainFilterCacheTestCase.FakeDomain(pk)

    def test_simple(self):
        user = self.get_user(1)
        domain = self.get_domain(1)
        cache = DomainFilterCache()

        self.assertEqual(cache.get(user, domain), None)

        cache.add(user, domain, True)
        self.assertEqual(cache.get(user, domain), True)

        cache.add(user, domain, False)
        self.assertEqual(cache.get(user, domain), False)

        cache.log_statistic()

    def test_loops_cache_miss(self):
        user = self.get_user(1)
        domain = self.get_domain(1)
        cache = DomainFilterCache()

        for i in xrange(1000):
            self.assertEqual(cache.get(user, domain), None)
            self.assertEqual(cache.miss_count, i+1)

        cache.log_statistic()

    def test_loops_cache(self):
        user = self.get_user(1)
        domain = self.get_domain(1)
        cache = DomainFilterCache()

        cache.add(user, domain, True)

        for i in xrange(1000):
            self.assertEqual(cache.get(user, domain), True)
            self.assertEqual(cache.miss_count, 0)

        cache.log_statistic()
