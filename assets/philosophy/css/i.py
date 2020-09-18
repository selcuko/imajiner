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


def variations(tag):
    return [
        (f'{tag} {{', f'{tag}.{namespace} {{'),

        (f'\n{tag},', f'\n{tag}.{namespace},'),

        (f', {tag}:', f', {tag}.{namespace}:'),
        (f'\n{tag}:', f'\n{tag}.{namespace}:'),
        ]


identifiers = []
for tag in html_tags:
    vars = variations(tag)
    for var in vars:
        identifiers.append(var)



def findall(p, s):
    '''Yields all the positions of
    the pattern p in the string s.'''
    i = s.find(p)
    while i != -1:
        yield i
        i = s.find(p, i+1)

c=0
chunk = file.read()

for identifier, newer in identifiers:
    for index in findall(identifier, chunk):
        #print(f'[{identifier}]@{index}\n', chunk[index:index+20], '\n|\n|\n', chunk[index:index+20].replace(identifier, newer))
        chunk=chunk.replace(identifier, newer)
        c+=1

mod.write(chunk)
print('Done, total', c, 'line(s) modified.')