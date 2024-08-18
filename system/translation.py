from modeltranslation.translator import register, TranslationOptions
from .models import Reviewer

@register(Reviewer)
class ReviewerTranslationOptions(TranslationOptions):
    fields = ('key', 'content')
