import re
from django import forms
from .models import Photo, Review
from .mixins import StyleFormMixin

BANNED_WORDS = ['дурак', 'идиот', 'дебил', 'тупой', 'урод']


def censor_text(text):
    for word in BANNED_WORDS:
        pattern = re.compile(re.escape(word), re.IGNORECASE)
        text = pattern.sub('*' * len(word), text)
    return text


class PhotoForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['title', 'category', 'image', 'description', 'price']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if self.user and not self.user.has_subscription:
            self.fields.pop('price', None)

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if len(title) < 2:
            raise forms.ValidationError('Название должно быть не менее 2 символов')
        return title

    def clean_description(self):
        description = self.cleaned_data.get('description', '')
        return censor_text(description)


class ReviewForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Review
        fields = ['text', 'rating']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Ваш отзыв...'}),
            'rating': forms.RadioSelect(choices=[(i, i) for i in range(1, 6)]),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.photo = kwargs.pop('photo', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        if self.user and self.photo:
            if not self.user.has_subscription:
                existing = Review.objects.filter(user=self.user, photo=self.photo).count()
                if existing >= 1:
                    raise forms.ValidationError(
                        'Без подписки можно оставить только один отзыв на фотографию. '
                        'Оформите подписку для безлимитных отзывов.'
                    )
        return cleaned_data

    def clean_text(self):
        text = self.cleaned_data.get('text', '')
        return censor_text(text)