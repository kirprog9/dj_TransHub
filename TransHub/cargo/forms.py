from django import forms
from .models import *
from main.models import Country, City, Region


class CargoForm(forms.ModelForm):

    title = forms.CharField(label='Найменування вантажу', widget=forms.TextInput(
        attrs={'class': 'form-control','placeholder': 'Найменування вантажу', "id": "{{form.title.id_for_label}}"}))

    country_from = forms.ModelChoiceField(
        queryset=Country.objects.all(),
        required=False,
        label="Країна відправлення",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    region_from = forms.ModelChoiceField(
        queryset=Region.objects.none(),
        required=False,
        label="Регіон відправлення",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    city_from = forms.ModelChoiceField(
        queryset=City.objects.none(),
        required=False,
        label="Місто відправлення",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    country_to = forms.ModelChoiceField(
        queryset=Country.objects.all(),
        required=False,
        label="Країна призначення",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    region_to = forms.ModelChoiceField(
        queryset=Region.objects.none(),
        required=False,
        label="Регіон призначення",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    city_to = forms.ModelChoiceField(
        queryset=City.objects.none(),
        required=False,
        label="Місто призначення",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    weight_max = forms.IntegerField(label='Вага до (кг)',min_value=1, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '(тільки цілі числа)', 'min': '1'}))

    volume_max = forms.IntegerField(label='Обʼєм до (м³)', required=False,min_value=1,
                                    widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '(тільки цілі числа)'}))
    length = forms.DecimalField(label='Довжина (м)', required=False,min_value=0.01,max_value=99.99,
                                widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Довжина (м)', 'min': '0.01', 'max': '99.99'}))
    width = forms.DecimalField(label='Ширина (м)', required=False,min_value=0.01,max_value=99.99,
                               widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ширина (м)', 'min': '0.01', 'max': '99.99'}))
    height = forms.DecimalField(label='Висота (м)', required=False,min_value=0.01,max_value=99.99,
                                widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Висота (м)', 'min': '0.01', 'max': '99.99'}))
    packaging = forms.ChoiceField(label='Упаковка', choices=Cargo.PACKAGING_CHOICES,
                                  widget=forms.Select(attrs={'class': 'form-control'}))
    body_type = forms.ModelMultipleChoiceField(label='Тип кузова', queryset=BodyType.objects.all(),
                                                 required=False,
                                                 widget=forms.SelectMultiple(attrs={'class': 'form-control'}))
    load_unload = forms.ModelMultipleChoiceField(label='Завантаження/Вивантаження', queryset=LoadUnload.objects.all(),
                                                 required=False,
                                                 widget=forms.SelectMultiple(attrs={'class': 'form-control'}))
    permissions = forms.ModelMultipleChoiceField(label='Дозволи', queryset=Permissions.objects.all(),
                                                 required=False,
                                                 widget=forms.SelectMultiple(attrs={'class': 'form-control'}))
    payment_type = forms.ChoiceField(label='Форма оплати', choices=Cargo.PAYMENT_TYPE2_CHOICES,
                                  widget=forms.Select(attrs={'class': 'form-control'}))

    amount = forms.IntegerField(label='Сума коштів',min_value=10,max_value=100000000,
                                widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Сума коштів'}))
    currency = forms.CharField(label='Валюта', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Валюта'}))

    payment_moment = forms.ChoiceField(label='Момент оплати', choices=Cargo.PAYMENT_MOMENT_CHOICES,
                                  widget=forms.Select(attrs={'class': 'form-control'}))
    photo = forms.ImageField(label='Фото', required=False,
                             widget=forms.ClearableFileInput(attrs={'class': 'form-control-file'}))
    notes = forms.CharField(label='Примітка', required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Примітка'}))
    published = forms.BooleanField(label='Публікація', required=False,initial=True,
                                   widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))

    class Meta:
        model = Cargo
        fields = [
            'title', 'country_from', 'region_from', 'city_from', 'country_to', 'region_to', 'city_to', 'weight_max',
            'volume_max', 'length', 'width', 'height', 'packaging', 'body_type',
            'load_unload', 'permissions', 'payment_type',
            'amount', 'currency', 'payment_moment', 'photo',
            'notes', 'published'
        ]

    def clean_vehicle_count(self):
        vehicle_count = self.cleaned_data['vehicle_count']
        if vehicle_count is None:
            vehicle_count = 1
        return vehicle_count

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if 'country_to' in self.data:
            try:
                country_id = int(self.data.get('country_to'))
                self.fields['region_to'].queryset = Region.objects.filter(country_id=country_id).order_by('name')
            except (ValueError, TypeError):
                self.fields['region_to'].queryset = Region.objects.none()

        if 'region_to' in self.data:
            try:
                region_id = int(self.data.get('region_to'))
                self.fields['city_to'].queryset = City.objects.filter(region_id=region_id).order_by('name')
            except (ValueError, TypeError):
                self.fields['city_to'].queryset = City.objects.none()

        if 'country_from' in self.data:
            try:
                country_id = int(self.data.get('country_from'))
                self.fields['region_from'].queryset = Region.objects.filter(country_id=country_id).order_by('name')
            except (ValueError, TypeError):
                self.fields['region_from'].queryset = Region.objects.none()

        if 'region_from' in self.data:
            try:
                region_id = int(self.data.get('region_from'))
                self.fields['city_from'].queryset = City.objects.filter(region_id=region_id).order_by('name')
            except (ValueError, TypeError):
                self.fields['city_from'].queryset = City.objects.none()


class CargoFilterForm(forms.Form):
    country_from = forms.ModelChoiceField(
        queryset=Country.objects.all(),
        required=False,
        label="Країна відправлення",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    region_from = forms.ModelChoiceField(
        queryset=Region.objects.none(),
        required=False,
        label="Регіон відправлення",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    city_from = forms.ModelChoiceField(
        queryset=City.objects.none(),
        required=False,
        label="Місто відправлення",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    country_to = forms.ModelChoiceField(
        queryset=Country.objects.all(),
        required=False,
        label="Країна призначення",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    region_to = forms.ModelChoiceField(
        queryset=Region.objects.none(),
        required=False,
        label="Регіон призначення",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    city_to = forms.ModelChoiceField(
        queryset=City.objects.none(),
        required=False,
        label="Місто призначення",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    weight_max = forms.IntegerField(
        required=False,
        label="Вага до (кг)",
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Максимальна вага'})
    )

    volume_max = forms.IntegerField(
        required=False,
        label="Об'єм до (м³)",
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': "Максимальний об'єм"})
    )

    body_type = forms.ModelMultipleChoiceField(
        queryset=BodyType.objects.all(),
        required=False,
        label="Тип кузова",
        widget=forms.SelectMultiple(attrs={'class': 'form-control'})
    )

    load_unload = forms.ModelMultipleChoiceField(
        queryset=LoadUnload.objects.all(),
        required=False,
        label="Завантаження/Розвантаження",
        widget=forms.SelectMultiple(attrs={'class': 'form-control'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if 'country_to' in self.data:
            try:
                country_id = int(self.data.get('country_to'))
                self.fields['region_to'].queryset = Region.objects.filter(country_id=country_id).order_by('name')
            except (ValueError, TypeError):
                self.fields['region_to'].queryset = Region.objects.none()

        if 'region_to' in self.data:
            try:
                region_id = int(self.data.get('region_to'))
                self.fields['city_to'].queryset = City.objects.filter(region_id=region_id).order_by('name')
            except (ValueError, TypeError):
                self.fields['city_to'].queryset = City.objects.none()

        if 'country_from' in self.data:
            try:
                country_id = int(self.data.get('country_from'))
                self.fields['region_from'].queryset = Region.objects.filter(country_id=country_id).order_by('name')
            except (ValueError, TypeError):
                self.fields['region_from'].queryset = Region.objects.none()

        if 'region_from' in self.data:
            try:
                region_id = int(self.data.get('region_from'))
                self.fields['city_from'].queryset = City.objects.filter(region_id=region_id).order_by('name')
            except (ValueError, TypeError):
                self.fields['city_from'].queryset = City.objects.none()