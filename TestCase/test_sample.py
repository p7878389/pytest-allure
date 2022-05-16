import allure


def inc(x):
    return x + 1


def test_answer():
    assert inc(4) == 5


@allure.feature("test")
class TestAllUre:

    @allure.story("测试用例")
    def test_1(self):
        print("xxxx")
