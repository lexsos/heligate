from django.test import TestCase

from .loger import extruct_domain


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

        domain_name = extruct_domain('https://_test.ru_:8080/fdf/dfdf/dfd/121f')
        self.assertEqual(domain_name, '_test.ru_')

        domain_name = extruct_domain('https://1.2.3.4:8080/fdf/dfdf/dfd/121f')
        self.assertEqual(domain_name, '1.2.3.4')
