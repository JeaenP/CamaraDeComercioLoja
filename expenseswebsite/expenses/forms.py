from django import forms
from .models import Expense

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = '__all__'
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date'}),
            'fecha_inscripcion': forms.DateInput(attrs={'type': 'date'}),
            # Agrega widgets para otras fechas según sea necesario
        }