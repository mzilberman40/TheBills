# from django.test import SimpleTestCase
# from django.urls import reverse, resolve
# import handbooks.views as hview
# import handbooks.urls as hurls
#
#
# app_name = hurls.app_name
#
# def pattern2url(app_name, url_pattern):
#     url_name = f"{app_name}:{url_pattern.name}"
#     url_args = url_pattern.pattern.converters.keys()
#     return reverse(url_name, args=url_args)
#
#
# # def get_test_funcs(urls):
# #     app_name = urls.app_name
# #     for u in hurls.urlpatterns:
# #         url_name = f"{app_name}:{u.name}"
# #         url_args = u.pattern.converters.keys()
# #         url = reverse(url_name, args=url_args)
# #         if u.callback.__name__ == 'view':
# #             self.assertEqual(resolve(url).func.view_class, )
# #
# #         # print(u)
# #         # print(u.__dict__)
# #         # print(dir(u))
# #         # print(u.check)
# #         # print(u.callback)
# #         print(u.default_args)
# #         print(u.lookup_str)
# #         print(u.name)
# #         print(u.pattern)
# #         # print(u.resolve())
#
#
# class TestUrls(SimpleTestCase):
#
#     # def test_urls(self):
#     #     for url_pattern in hurls.urlpatterns:
#     #         with self.subTest(url_pattern=url_pattern.name):
#     #             url = pattern2url(app_name, url_pattern)
#     #             r = resolve(url).func
#     #             resolver = r.view_class if hasattr(r, 'view_class') else r
#     #             print(resolver)
#     #             # self.assertEqual(resolver, hview.CurrenciesList)
#
#     def test_currencies_list(self):
#         url_pattern = hurls.urlpatterns[0]
#         # url = reverse('handbooks:currencies_list_url')
#         # url = reverse('handbooks:currencies')
#         url = pattern2url(app_name, url_pattern)
#         # self.assertEqual(resolve(url).func.view_class, hview.CurrenciesList)
#         self.assertEqual(resolve(url).func, hview.show_currencies)
#
#     def test_currency_create(self):
#         url_pattern = hurls.urlpatterns[1]
#         # url = reverse('handbooks:currencies_list_url')
#         # url = reverse('handbooks:currencies')
#         url = pattern2url(app_name, url_pattern)
#         # self.assertEqual(resolve(url).func.view_class, hview.CurrenciesList)
#         self.assertEqual(resolve(url).func, hview.show_currencies)