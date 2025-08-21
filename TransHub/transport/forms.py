from django import forms
from .models import Transport, BodyType, LoadUnload, Permissions
from main.models import Country, City, Region


class TransportForm(forms.ModelForm):
    loading_date = forms.DateField(label='Дата завантаження', widget=forms.DateInput(
        attrs={'class': 'form-control', 'placeholder': 'Дата завантаження', 'type': 'date'}))

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

    brand = forms.CharField(label='Бренд', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Бренд'}))
    model = forms.CharField(label='Модель', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Модель'}))
    license_plate = forms.CharField(label='Номерний знак', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Номерний знак'}))
    year = forms.IntegerField(label='Рік випуску', widget=forms.NumberInput(attrs={'class': 'form-control', 'min': 1950, 'max': 2024, 'placeholder': 2000}))
    max_weight = forms.DecimalField(label='Максимальна вага (кг)', widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Макс. вага'}))
    max_volume = forms.DecimalField(label="Максимальний об'єм (м³)", widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': "Макс. об'єм"}))
    body_type = forms.ModelMultipleChoiceField(label='Тип кузова', queryset=BodyType.objects.all(), widget=forms.SelectMultiple(attrs={'class': 'form-control'}))
    load_unload = forms.ModelMultipleChoiceField(label='Завантаження/Розвантаження', queryset=LoadUnload.objects.all(), widget=forms.SelectMultiple(attrs={'class': 'form-control'}))
    permissions = forms.ModelMultipleChoiceField(label='Дозволи', queryset=Permissions.objects.all(), widget=forms.SelectMultiple(attrs={'class': 'form-control'}))
    photo = forms.ImageField(label='Фото', required=False, widget=forms.ClearableFileInput(attrs={'class': 'form-control-file'}))
    notes = forms.CharField(label='Примітки', required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Примітки'}))
    published = forms.BooleanField(label='Публікація', required=False,initial=True, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))

    class Meta:
        model = Transport
        fields = ['loading_date', 'country_from', 'region_from', 'city_from', 'country_to', 'region_to', 'city_to',
                  'brand', 'model', 'license_plate', 'year',
                  'max_weight', 'max_volume','body_type', 'load_unload',
                  'permissions', 'photo', 'notes', 'published']

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


class TranportFilterForm(forms.Form):
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

    max_weight = forms.IntegerField(
        required=False,
        label="Вага до (кг)",
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Максимальный вес'})
    )

    max_volume = forms.IntegerField(
        required=False,
        label="Объем до (м³)",
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Максимальный объем'})
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