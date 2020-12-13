from django.utils.text import slugify
from django.utils.html import escape, strip_tags
from markdown import markdown
from uuid import UUID

class generate:
    LEAD_MAX_CHAR = 160
    SLUG_MAX_CHAR = 20

    @classmethod
    def slug(cls, text, uuid=None, unicode=False):
        """[summary]

        Args:
            text (str): Text to be slugified
            uuid (str, optional): Optional UUID to be appended to slug. Defaults to None.
            unicode (bool, optional): Allow unicode characters. Defaults to False.

        Raises:
            ValueError: Argument type mismatch

        Returns:
            str: Slugified versions of given arguments.
        """
        if not isinstance(text, str):
            raise ValueError(f"'text' argument must be an instance of str, not {typeof(text)}")
        if uuid is not None:
            if isinstance(uuid, str):
                pass
            elif isinstance(uuid, UUID):
                uuid = str(uuid)
            else:
                raise ValueError(f"'uuid' argument must be an instance of str or UUID, not {typeof(str)}")
        
        unicode = bool(unicode)
        slugified = text.lower().replace('ı', 'i')
        slugified = slugified[:cls.SLUG_MAX_CHAR]
        slugified = slugify(slugified, allow_unicode=unicode)
        if uuid:
            slugified += ('-' + uuid[:8])
        return slugified
    
    @classmethod
    def raw(cls, text):
        """Returns the text in given HTML.

        Args:
            text (str): HTML

        Returns:
            str: Inner text
        """
        return strip_tags(text)

    @classmethod
    def html(cls, text, use_markdown=True):
        """Returns HTMLified version of given text.

        Args:
            text (str): Source text
            use_markdown (bool, optional): Treat source text as markdown. Defaults to True.

        Returns:
            str: HTML
        """
        if use_markdown:
            safe = escape(text)
            return markdown(safe)
        else:
            safe = safe.replace('\n\n', '</p><p>')
            safe = safe.replace('\n', '<br>')
            safe = f'<p>{safe}</p>'
            return safe
    
    @classmethod
    def lead(cls, text, append_dots=None):
        """Provides a summary, a lead, of given text.

        Args:
            text (str): Source text
            append_dots (bool, optional): Append dots (...) to lead. Defaults to None.

        Returns:
            str: Lead text
        """
        texthead = text[:cls.LEAD_MAX_CHAR]
        texthead = texthead.replace('\n', ' ').replace('\r', ' ')
        while texthead.endswith(' ') and len(texthead) > 0:
            texthead = texthead[:-1]

        if append_dots is None:
            append_dots = len(text) - 3 > LEAD_MAX_CHAR
        if append_dots: texthead += '...'
        return texthead
    
    @classmethod
    def clean(cls, text):
        """Cleans text for language classification.

        Args:
            text (str): Source text

        Returns:
            str: Cleaned text
        """
        import cleantext
        
        cleaned = cleantext.clean(text, replace_with='', all=True)
        return cleaned
    
