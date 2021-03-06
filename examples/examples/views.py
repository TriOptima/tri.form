from os.path import dirname, abspath, join
from tri.struct import Struct

from django.http import HttpResponse
from django.utils.safestring import mark_safe
from django.utils.html import format_html

from .models import Foo, Bar
from tri_form import Form, Field, Link, choice_parse
from tri_form.views import create_object, edit_object

for i in range(100 - Foo.objects.count()):
    Foo.objects.create(name=f'X{i}', a=i, b=True)


def index(request):
    return HttpResponse(
        """<html><body>
        <a href="example_1/">Example 1</a><br/>
        <a href="example_2/">Example 2 create</a><br/>
        <a href="example_3/">Example 3 edit</a><br/>
        <a href="example_4/">Example 4 custom buttons</a><br/>
        <a href="example_5/">Example 5 automatic AJAX endpoint</a><br/>
        <a href="kitchen/">Kitchen sink</a><br/>
        </body></html>""")


def style(request):
    return HttpResponse(open(join(dirname(dirname(dirname(abspath(__file__)))), 'form.css')).read())


def example_1(request):
    class MyForm(Form):
        foo = Field()
        bar = Field()

    form = MyForm(request=request)

    message = mark_safe("\n".join(
        format_html(
            "{}: {}",
            name,
            bound_field.value
        )
        for name, bound_field in form.fields_by_name.items()))

    return HttpResponse(format_html(
        """
            <html>
                <body>
                    {}
                    {}
                </body>
            </html>
        """,
        form.render(),
        message))


def example_2(request):
    return create_object(request, model=Foo)


def example_3(request):
    return edit_object(request, instance=Foo.objects.all().first())


def example_4(request):
    return edit_object(
        request,
        instance=Foo.objects.all().first(),
        form__links=[
            Link.submit(attrs__value='Foo'),
            Link.submit(attrs__value='Bar'),
            Link(title='Back to index', attrs__href='/'),
        ]
    )


def example_5(request):
    return create_object(
        request,
        model=Bar,
        form__base_template='tri_form/base_select2.html',
        form__field__b__input_template='tri_form/choice_select2.html',
        form__links=[
            Link.submit(attrs__value='Foo'),
            Link.submit(attrs__value='Bar'),
            Link(title='Back to index', attrs__href='/'),
        ]
    )


class KitchenForm(Form):
    class Meta:
        name = 'kitchen'

    foo = Field()

    fisk = Field.multi_choice(
        choices=[1, 2, 3, 4],
        parse=choice_parse,
        initial_list=[1, 2],
        editable=False
    )


class SinkForm(Form):
    class Meta:
        name = 'sink'

    foo = Field()


def kitchen(request):
    kitchen_form = KitchenForm(request)
    sink_form = SinkForm(request)
    sink_form2 = SinkForm(request, name='sinkform2')

    if request.method == 'POST':
        if kitchen_form.is_target() and kitchen_form.is_valid():
            values = kitchen_form.apply(Struct())
            return HttpResponse(format_html("Kitchen values was {}", values))

        if sink_form.is_target() and sink_form.is_valid():
            values = sink_form.apply(Struct())
            return HttpResponse(format_html("Sink values was {}", values))

    return HttpResponse(format_html(
        """\
            <html>
                <body>
                    <h2>Kitchen</h2>
                    {}
                    <h2>Sink</h2>
                    {}
                    <h2>Sink</h2>
                    {}
                </body>
            </html>
        """,
        kitchen_form.render(),
        sink_form.render(),
        sink_form2.render()))
