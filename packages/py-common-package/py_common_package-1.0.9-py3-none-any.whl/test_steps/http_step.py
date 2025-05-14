# -*- coding:utf-8 -*-
from hamcrest import *
from behave import given,use_step_matcher
use_step_matcher("re")



@given(u'.*[校验].*接口响应status是:(?P<status_code>.*)')
def check_http_code(context, status_code):
    assert_that(context.res.status_code, is_(int(status_code)), "接口响应状态错误")

@given('执行(?P<sc_from>.*)脚本')
def test_temp(context, sc_from):
    print('124')
    print(sc_from)
