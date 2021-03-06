import pytest
from tri_struct import merged

from tri_form import Field, Form
from tri_form.compat import render_to_string, format_html, field_defaults_factory, render_template, Template
from .compat import RequestFactory, SafeText


def test_render_to_string():
    assert render_to_string(
        template_name='tri_form/non_editable.html',
        request=RequestFactory().get('/'),
        context=dict(
            field=dict(
                id=SafeText('<a b c><d><e>'),
                rendered_value=SafeText('<a b c><d><e>'),
            ),
        )
    ).strip() == '<span id="<a b c><d><e>"><a b c><d><e></span>'


def test_format_html():
    assert format_html('<{a}>{b}{c}', a='a', b=format_html('<b>'), c='<c>') == '<a><b>&lt;c&gt;'


def test_format_html2():
    assert render_template(RequestFactory().get('/'), Template('{{foo}}'), dict(foo=format_html('<a href="foo">foo</a>'))) == '<a href="foo">foo</a>'


def test_format_html3():
    assert render_template(RequestFactory().get('/'), Template('{{foo}}'), dict(foo=format_html('{}', format_html('<a href="foo">foo</a>')))) == '<a href="foo">foo</a>'


def test_format_html4():
    actual = render_template(
        RequestFactory().get('/'),
        Template('{{foo}}'),
        dict(
            foo=Form(fields=[Field(name='foo')]),
        )
    )
    print(actual)
    assert '<input type="text" value="" name="foo" id="id_foo"' in actual


def test_format_html5():
    actual = Form(fields=[Field(name='foo')], request=RequestFactory().get('/')).render()
    print(actual)
    assert type(actual) == SafeText


def test_format_html6():
    form = Form(fields=[Field(name='foo')], request=RequestFactory().get('/'))
    actual = form.fields_by_name.foo.render()
    print(actual)
    assert type(actual) == SafeText


def test_render_template():
    actual = render_template(RequestFactory().get('/'), Template('{{foo}}'), dict(foo=1))
    print(actual)
    assert type(actual) == SafeText


@pytest.mark.django
def test_field_defaults_factory():
    from django.db import models
    base = dict(parse_empty_string_as_none=True, required=True, display_name=None)

    assert field_defaults_factory(models.CharField(null=False, blank=False)) == merged(base, dict(parse_empty_string_as_none=False))
    assert field_defaults_factory(models.CharField(null=False, blank=True)) == merged(base, dict(parse_empty_string_as_none=False, required=False))

    assert field_defaults_factory(models.CharField(null=True, blank=False)) == merged(base, dict(required=False))
    assert field_defaults_factory(models.CharField(null=True, blank=True)) == merged(base, dict(required=False))


@pytest.mark.django
def test_field_defaults_factory_boolean():
    from django.db import models

    django_null_default = not models.BooleanField().null

    base = dict(parse_empty_string_as_none=django_null_default, display_name=None)

    assert field_defaults_factory(models.BooleanField(null=False, blank=False)) == merged(base, dict(parse_empty_string_as_none=False))
    assert field_defaults_factory(models.BooleanField(null=False, blank=True)) == merged(base, dict(parse_empty_string_as_none=False))

    assert field_defaults_factory(models.BooleanField(null=True, blank=False)) == base
    assert field_defaults_factory(models.BooleanField(null=True, blank=True)) == base
