import re

import pytest

from tri_form.render import render_attrs


def test_render_attrs():
    assert render_attrs(None) == ''
    assert render_attrs({'foo': 'bar', 'baz': 'quux'}) == ' baz="quux" foo="bar"'


def test_render_class():
    assert render_attrs({'apa': True, 'bepa': '', 'cepa': None, 'class': dict(foo=False, bar=True, baz=True)}) == ' apa bepa="" class="bar baz"'


def test_render_attrs_non_standard_types():
    assert render_attrs({'apa': True, 'bepa': '', 'cepa': None, 'class': 'bar baz'}) == ' apa bepa="" class="bar baz"'


def test_render_style():
    assert render_attrs(
        dict(
            style=dict(
                foo='1',
                bar='2',
            )
        )
    ) == ' style="bar: 2; foo: 1"'


def test_render_with_empty():
    assert render_attrs(
        dict(
            a='1',
            style={},
            z='2',
        )
    ) == ' a="1" z="2"'


def test_render_attrs_raises_for_some_common_pitfall_types():
    with pytest.raises(TypeError) as e:
        render_attrs(dict(
            foo=dict(a=1)
        ))

    assert str(e.value) == "Only the class and style attributes can be dicts, you sent {'a': 1}"

    with pytest.raises(TypeError) as e:
        render_attrs(dict(
            foo=[]
        ))

    assert str(e.value) == "Attributes can't be of type list, you sent []"

    with pytest.raises(TypeError) as e:
        render_attrs(dict(
            foo=tuple()
        ))

    assert str(e.value) == "Attributes can't be of type tuple, you sent ()"

    with pytest.raises(TypeError) as e:
        render_attrs(dict(
            foo=lambda foo: foo
        ))

    assert re.match("Attributes can't be callable, you sent <function .*>", str(e.value))
