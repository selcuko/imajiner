namespace = 'philosophy'
filename = 'main.css'
new_filename = filename.split('.')
new_filename = ''.join(new_filename[:-1]) + '.encapsulated.' + new_filename[-1]

file = open(filename, 'r+t')
mod = open(new_filename, 'wt')

html_tags = [
    'div',
    '*',
    'h1',
    'h2',
    'h3',
    'h4',
    'h5',
    'h6',
    'span',
    'a',
    'i',
    'p',
    'href',
    'html',
    'body',
    'main',
    'pre',
    'code',
    'b',
    'samp',
    'kbd',
    'dfn',
    'small',
    'sub',
    'sup',
    'abbr',
    'audio',
    'video',
    'strong',
    'img',
    'svg',
    'button',
    'input',
    'textarea',
    'select',
    'optgroup',
    'fieldset',
    'legend',
    'progress',
    'canvas',
]

chunk = file.read()
lines = chunk.split('\n')

for l in lines:
    for tag in html_tags:
        if tag in l:
            print(l)
            input()

