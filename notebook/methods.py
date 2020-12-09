from django.utils.text import slugify
from django.utils.html import escape
from markdown import markdown

class generate:
    LEAD_MAX_CHAR = 160
    SLUG_MAX_CHAR = 20

    @classmethod
    def slug(cls, text, uuid=None, unicode=False):
        slugified = text.replace('ı', 'i')
        slugified = slugified[:cls.SLUG_MAX_CHAR]
        slugified = slugify(slugified, allow_unicode=unicode)
        if uuid:
            uuid = str(uuid)
            slugified += ('-' + uuid[:8])
        return slugified
    
    @classmethod
    def html(cls, text):
        safe = escape(text)
        return markdown(safe)

        #  markdown styling enabled
        safe = safe.replace('\n\n', '</p><p>')
        safe = safe.replace('\n', '<br>')
        safe = f'<p>{safe}</p>'
        return safe
    
    @classmethod
    def lead(cls, text, append_dots=True):
        texthead = text.split('. ')[0][:cls.LEAD_MAX_CHAR]
        texthead = texthead.replace('\n', ' ')
        texthead = texthead.replace('\r', ' ')
        while texthead.endswith(' '):
            texthead = texthead[:-1]
        if append_dots: texthead += '...'
        return texthead
    
    @classmethod
    def clean(cls, text):
        import cleantext
        
        cleaned = cleantext.replace_urls(text, replace_with='')
        cleaned = cleantext.replace_emails(cleaned, replace_with='')
        return cleaned
    
