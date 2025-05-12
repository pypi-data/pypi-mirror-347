from django import forms
from django.db import models

from crispy_forms.helper import FormHelper


class SampleForm(forms.Form):
    is_company = forms.BooleanField(label="company", required=False)
    email = forms.EmailField(
        label="email",
        max_length=30,
        help_text="Insert your email",
    )
    password1 = forms.CharField(
        label="password", max_length=30, widget=forms.PasswordInput()
    )
    password2 = forms.CharField(
        label="re-enter password",
        max_length=30,
        widget=forms.PasswordInput(),
    )
    first_name = forms.CharField(label="first name", max_length=5)
    last_name = forms.CharField(label="last name", max_length=5)
    datetime_field = forms.SplitDateTimeField(
        label="date time", widget=forms.SplitDateTimeWidget()
    )

    def clean(self):
        super().clean()
        password1 = self.cleaned_data.get("password1", None)
        password2 = self.cleaned_data.get("password2", None)
        if not password1 and not password2 or password1 != password2:
            raise forms.ValidationError("Passwords dont match")
        return self.cleaned_data


class SampleForm2(SampleForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)


class CheckboxesSampleForm(forms.Form):
    checkboxes = forms.MultipleChoiceField(
        choices=((1, "Option one"), (2, "Option two"), (3, "Option three")),
        initial=(1,),
        widget=forms.CheckboxSelectMultiple,
    )

    alphacheckboxes = forms.MultipleChoiceField(
        choices=(
            ("option_one", "Option one"),
            ("option_two", "Option two"),
            ("option_three", "Option three"),
        ),
        initial=("option_two", "option_three"),
        widget=forms.CheckboxSelectMultiple,
    )

    numeric_multiple_checkboxes = forms.MultipleChoiceField(
        choices=((1, "Option one"), (2, "Option two"), (3, "Option three")),
        initial=(1, 2),
        widget=forms.CheckboxSelectMultiple,
    )


class CrispyTestModel(models.Model):
    email = models.CharField(max_length=20)
    password = models.CharField(max_length=20)


class SampleForm3(forms.ModelForm):
    class Meta:
        model = CrispyTestModel
        fields = ["email", "password"]
        exclude = ["password"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)


class SampleForm4(forms.ModelForm):
    class Meta:
        model = CrispyTestModel
        fields = "__all__"


class SampleForm5(forms.Form):
    choices = [
        (1, 1),
        (2, 2),
        (1000, 1000),
    ]
    checkbox_select_multiple = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple, choices=choices
    )
    radio_select = forms.ChoiceField(widget=forms.RadioSelect, choices=choices)
    pk = forms.IntegerField()


class SampleFormWithMedia(forms.Form):
    class Media:
        css = {"all": ("test.css",)}
        js = ("test.js",)


class SampleFormWithMultiValueField(forms.Form):
    multi = forms.SplitDateTimeField()


class CrispyEmptyChoiceTestModel(models.Model):
    fruit = models.CharField(
        choices=[("apple", "Apple"), ("pear", "Pear")],
        null=True,
        blank=True,
        max_length=20,
    )


class SampleForm6(forms.ModelForm):
    class Meta:
        """
        When allowing null=True in a model field,
        the corresponding field will have a choice
        for the empty value.

        When the form is initialized by an instance
        with initial value None, this choice should
        be selected.
        """

        model = CrispyEmptyChoiceTestModel
        fields = ["fruit"]
        widgets = {"fruit": forms.RadioSelect()}


class SampleForm7(forms.ModelForm):
    is_company = forms.CharField(
        label="company", required=False, widget=forms.CheckboxInput()
    )
    password2 = forms.CharField(
        label="re-enter password",
        max_length=30,
        widget=forms.PasswordInput(),
    )

    class Meta:
        model = CrispyTestModel
        fields = ("email", "password", "password2")


class SampleForm8(forms.ModelForm):
    is_company = forms.CharField(
        label="company", required=False, widget=forms.CheckboxInput()
    )
    password2 = forms.CharField(
        label="re-enter password",
        max_length=30,
        widget=forms.PasswordInput(),
    )

    class Meta:
        model = CrispyTestModel
        fields = ("email", "password2", "password")


class FakeFieldFile:
    """
    Quacks like a FieldFile (has a .url and string representation), but
    doesn't require us to care about storages etc.
    """

    url = "something"

    def __str__(self):
        return self.url


class FileForm(forms.Form):
    file_field = forms.FileField(widget=forms.FileInput)
    clearable_file = forms.FileField(
        widget=forms.ClearableFileInput, required=False, initial=FakeFieldFile()
    )


class FileFormRequired(forms.Form):
    file_field = forms.FileField(widget=forms.FileInput)
    clearable_file = forms.FileField(widget=forms.ClearableFileInput)


class InputsForm(forms.Form):
    choices = [
        (1, "Option one"),
        (2, "Option two"),
        (3, "Option three"),
        (4, "Option four"),
        (5, "Option five"),
        (6, "Option six"),
    ]
    text_input = forms.CharField()
    text_area = forms.CharField(widget=forms.Textarea())
    input_with_icon = forms.CharField()

    checkbox = forms.CharField(
        label="company", required=False, widget=forms.CheckboxInput()
    )
    checkboxes = forms.MultipleChoiceField(
        choices=choices[:3],
        initial=(1,),
        widget=forms.CheckboxSelectMultiple,
    )
    inline_checkboxes = forms.MultipleChoiceField(
        choices=choices[:3],
        initial=(1,),
        widget=forms.CheckboxSelectMultiple,
    )

    radio = forms.ChoiceField(widget=forms.RadioSelect, choices=choices[:3])
    inline_radios = forms.ChoiceField(
        widget=forms.RadioSelect, choices=choices[:3], initial=2
    )

    select_input = forms.ChoiceField(choices=choices[:3])
    select_multiple = forms.MultipleChoiceField(choices=choices)


class LabelForm(forms.Form):
    text_input = forms.CharField(label="Test html <b>escape</b>")


class CustomRadioSelect(forms.RadioSelect):
    pass


class CustomCheckboxSelectMultiple(forms.CheckboxSelectMultiple):
    pass


class SampleFormCustomWidgets(forms.Form):
    inline_radios = forms.ChoiceField(
        choices=(
            ("option_one", "Option one"),
            ("option_two", "Option two"),
        ),
        widget=CustomRadioSelect,
        initial="option_two",
    )

    checkboxes = forms.MultipleChoiceField(
        choices=((1, "Option one"), (2, "Option two"), (3, "Option three")),
        initial=(1,),
        widget=CustomCheckboxSelectMultiple,
    )


class GroupedChoiceForm(forms.Form):
    choices = [
        (
            "Audio",
            [
                ("vinyl", "Vinyl"),
                ("cd", "CD"),
            ],
        ),
        (
            "Video",
            [
                ("vhs", "VHS Tape"),
                ("dvd", "DVD"),
            ],
        ),
        ("unknown", "Unknown"),
    ]
    checkbox_select_multiple = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple, choices=choices
    )
    radio = forms.MultipleChoiceField(widget=forms.RadioSelect, choices=choices)


class HelpTextForm(forms.Form):
    email = forms.EmailField(
        label="email",
        help_text="Insert your <b>email</b>",
    )


class FormGroupForm(forms.Form):
    text_input = forms.CharField(
        help_text="help on a text_input",
    )
    fruit = forms.ChoiceField(
        choices=[("apple", "Apple"), ("pear", "Pear")],
    )
