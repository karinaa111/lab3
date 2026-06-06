from django import forms

class CalibrationForm(forms.Form):
    data_text = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'placeholder': 'Вставте дані, наприклад:\n1abc2\npqr3stu8vwx\ntreb7uchet',
            'rows': 8,
        }),
        label='Дані (текст)'
    )
    data_file = forms.FileField(
        required=False,
        label='Або завантажте .txt файл'
    )

    def clean(self):
        cleaned = super().clean()
        if not cleaned.get('data_text') and not cleaned.get('data_file'):
            raise forms.ValidationError('Введіть дані або завантажте файл.')
        return cleaned
