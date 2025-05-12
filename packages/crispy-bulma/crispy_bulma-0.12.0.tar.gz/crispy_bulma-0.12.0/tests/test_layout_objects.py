import pytest

import django
from django import forms
from django.template import Context, Template
from django.utils.translation import activate, deactivate
from django.utils.translation import gettext as _

from crispy_bulma.bulma import InlineCheckboxes, InlineRadios
from crispy_bulma.layout import IconField
from crispy_forms.bootstrap import Tab, TabHolder
from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Field, Layout, MultiWidgetField
from crispy_forms.utils import render_crispy_form

from .forms import (
    CheckboxesSampleForm,
    CustomCheckboxSelectMultiple,
    CustomRadioSelect,
    GroupedChoiceForm,
    InputsForm,
    SampleForm,
    SampleFormCustomWidgets,
)
from .utils import parse_expected, parse_form


def test_email_field():
    form = SampleForm()
    form.helper = FormHelper()
    form.helper.layout = Layout("email")

    if django.VERSION < (5, 0):
        result = "test_email_field__lt50.html"
    else:
        result = "test_email_field.html"
    assert parse_form(form) == parse_expected(result)


def test_field_with_custom_template():
    test_form = SampleForm()
    test_form.helper = FormHelper()
    test_form.helper.layout = Layout(
        Field("email", template="custom_field_template.html")
    )

    html = render_crispy_form(test_form)
    assert "<h1>Special custom field</h1>" in html


def test_multiwidget_field():
    template = Template(
        """
        {% load crispy_forms_tags %}
        {% crispy form %}
    """
    )

    test_form = SampleForm()
    test_form.helper = FormHelper()
    test_form.helper.layout = Layout(
        MultiWidgetField(
            "datetime_field",
            attrs=(
                {"rel": "test_dateinput"},
                {"rel": "test_timeinput", "style": "width: 30px;", "type": "hidden"},
            ),
        )
    )

    c = Context({"form": test_form})

    html = template.render(c)

    assert html.count('class="dateinput') == 1
    assert html.count('rel="test_dateinput"') == 1
    assert html.count('rel="test_timeinput"') == 2
    assert html.count('style="width: 30px;"') == 2
    assert html.count('type="hidden"') == 2


def test_field_type_hidden():
    template = Template(
        """
        {% load crispy_forms_tags %}
        {% crispy test_form %}
    """
    )

    test_form = SampleForm()
    test_form.helper = FormHelper()
    test_form.helper.layout = Layout(
        Field("email", type="hidden", data_test=12),
        Field("datetime_field"),
    )

    c = Context({"test_form": test_form})
    html = template.render(c)

    # Check form parameters
    assert html.count('data-test="12"') == 1
    assert html.count('name="email"') == 1
    assert html.count('class="dateinput') == 1
    assert html.count('class="timeinput') == 1


def test_field_wrapper_class(settings):
    form = SampleForm()
    form.helper = FormHelper()
    form.helper.layout = Layout(Field("email", wrapper_class="testing"))

    html = render_crispy_form(form)
    assert html.count('class="field testing"') == 1


def test_html_with_carriage_returns(settings):
    test_form = SampleForm()
    test_form.helper = FormHelper()
    test_form.helper.layout = Layout(
        HTML(
            """
            if (a==b){
                // some comment
                a+1;
                foo();
            }
        """
        )
    )
    html = render_crispy_form(test_form)
    assert html.count("\n") == 24


def test_i18n():
    activate("es")
    form = SampleForm()
    form.helper = FormHelper()
    form.helper.layout = Layout(HTML(_("Enter a valid value.")))
    html = render_crispy_form(form)
    assert "Introduzca un valor válido" in html

    deactivate()


def test_remove_labels():
    form = SampleForm()
    # remove boolean field as label is still printed in bulma
    del form.fields["is_company"]

    for fields in form:
        fields.label = False

    html = render_crispy_form(form)

    assert "<label" not in html


@pytest.mark.parametrize(
    "form_field,expected",
    [
        ("text_input", "test_text_input.html"),
        ("text_area", "test_text_area.html"),
        ("radio", "test_radio.html"),
        ("inline_radios", "test_inline_radios.html"),
        ("checkbox", "test_checkbox.html"),
        ("checkboxes", "test_checkboxes.html"),
        ("inline_checkboxes", "test_inline_checkboxes.html"),
        ("select_input", "test_select.html"),
        ("select_multiple", "test_selectmultiple.html"),
        ("input_with_icon", "test_input_with_icon.html"),
    ],
)
def test_inputs(form_field, expected):
    form = InputsForm()
    form.helper = FormHelper()
    if form_field == "select_multiple":
        form_field = Field(form_field, size="5")
    if form_field == "inline_radios":
        form_field = InlineRadios(form_field)
    if form_field == "input_with_icon":
        form_field = IconField(
            form_field,
            icon_prepend="fa-solid fa-envelope",
            icon_append="fa-duotone fa-check-double",
            css_class="is-large",
        )

    form.helper.layout = Layout(form_field)

    assert parse_form(form) == parse_expected(expected)


def test_custom_django_widget():
    form = SampleFormCustomWidgets()

    # Make sure an inherited RadioSelect gets rendered as it
    assert isinstance(form.fields["inline_radios"].widget, CustomRadioSelect)
    form.helper = FormHelper()
    form.helper.layout = Layout("inline_radios")
    html = render_crispy_form(form)
    assert 'class="radio"' in html

    # Make sure an inherited CheckboxSelectMultiple gets rendered as it
    assert isinstance(form.fields["checkboxes"].widget, CustomCheckboxSelectMultiple)
    form.helper.layout = Layout("checkboxes")
    html = render_crispy_form(form)
    assert 'class="checkbox"' in html


@pytest.mark.skip(reason="bootstrap")
def test_tab_and_tab_holder():
    test_form = SampleForm()
    test_form.helper = FormHelper()
    test_form.helper.layout = Layout(
        TabHolder(
            Tab(
                "one",
                "first_name",
                css_id="custom-name",
                css_class="first-tab-class active",
            ),
            Tab("two", "password1", "password2"),
        )
    )
    html = render_crispy_form(test_form)

    assert (
        html.count(
            '<ul class="nav nav-tabs"> <li class="nav-item">'
            '<a class="nav-link active" href="#custom-name" data-bs-toggle="tab">'
            "One</a></li>"
        )
        == 1
    )
    assert html.count("tab-pane") == 2

    assert html.count('class="tab-pane first-tab-class active"') == 1

    assert html.count('<div id="custom-name"') == 1
    assert html.count('<div id="two"') == 1
    assert html.count('name="first_name"') == 1
    assert html.count('name="password1"') == 1
    assert html.count('name="password2"') == 1


@pytest.mark.skip(reason="bootstrap")
def test_tab_helper_reuse():
    # this is a proper form, according to the docs.
    # note that the helper is a class property here,
    # shared between all instances
    class SampleForm(forms.Form):
        val1 = forms.CharField(required=False)
        val2 = forms.CharField(required=True)
        helper = FormHelper()
        helper.layout = Layout(
            TabHolder(
                Tab("one", "val1"),
                Tab("two", "val2"),
            )
        )

    # first render of form => everything is fine
    test_form = SampleForm()
    html = render_crispy_form(test_form)

    # second render of form => first tab should be active,
    # but not duplicate class
    test_form = SampleForm()
    html = render_crispy_form(test_form)
    assert html.count('class="nav-item active active"') == 0

    # render a new form, now with errors
    test_form = SampleForm(data={"val1": "foo"})
    html = render_crispy_form(test_form)
    tab_class = "tab-pane"
    # tab 1 should not be active
    assert html.count('<div id="one" \n    class="{} active'.format(tab_class)) == 0
    # tab 2 should be active
    assert html.count('<div id="two" \n    class="{} active'.format(tab_class)) == 1


def test_radio_attrs():
    form = InputsForm()
    form.fields["inline_radios"].widget.attrs = {"class": "first"}
    form.fields["checkboxes"].widget.attrs = {"class": "second"}
    html = render_crispy_form(form)
    assert 'class="first"' in html
    assert 'class="second"' in html


def test_hidden_fields():
    form = SampleForm()
    # All fields hidden
    for field in form.fields:
        form.fields[field].widget = forms.HiddenInput()

    form.helper = FormHelper()
    form.helper.layout = Layout(
        Field("email"),
        InlineCheckboxes("first_name"),
        InlineRadios("last_name"),
    )
    html = render_crispy_form(form)
    assert html.count("<input") == 3
    assert html.count('type="hidden"') == 3
    assert html.count("<label") == 0


def test_multiplecheckboxes():
    test_form = CheckboxesSampleForm()
    html = render_crispy_form(test_form)
    assert html.count("checked") == 5

    test_form.helper = FormHelper(test_form)
    test_form.helper[1].wrap(InlineCheckboxes)
    html = render_crispy_form(test_form)
    assert html.count('class="control"') == 7


def test_multiple_checkboxes_unique_ids():
    test_form = CheckboxesSampleForm()
    html = render_crispy_form(test_form)

    expected_ids = [
        "checkboxes_0",
        "checkboxes_1",
        "checkboxes_2",
        "alphacheckboxes_0",
        "alphacheckboxes_1",
        "alphacheckboxes_2",
        "numeric_multiple_checkboxes_0",
        "numeric_multiple_checkboxes_1",
        "numeric_multiple_checkboxes_2",
    ]
    for id_suffix in expected_ids:
        expected_str = f'id="id_{id_suffix}"'
        assert html.count(expected_str) == 1


@pytest.mark.skip(reason="bootstrap")
def test_grouped_checkboxes_radios():
    form = GroupedChoiceForm()
    form.helper = FormHelper()
    form.helper.layout = Layout("checkbox_select_multiple")
    assert parse_form(form) == parse_expected("test_grouped_checkboxes.html")
    form.helper.layout = Layout("radio")
    assert parse_form(form) == parse_expected("test_grouped_radios.html")

    form = GroupedChoiceForm({})
    form.helper = FormHelper()
    form.helper.layout = Layout("checkbox_select_multiple")
    assert parse_form(form) == parse_expected("test_grouped_checkboxes_failing.html")
    form.helper.layout = Layout("radio")
    assert parse_form(form) == parse_expected("test_grouped_radios_failing.html")
