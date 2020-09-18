namespace = 'philosophy'
filename = 'base.css'
new_filename = filename.split('.')
new_filename = ''.join(new_filename[:-1]) + '.encapsulated.' + new_filename[-1]
print('Writing to new file:', new_filename)

file = open(filename, 'r+t')
mod = open(new_filename, 'wt')

html_tags = [
    'ul',
    'li',
    'ol',
    'div',
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
    'label',
    'form',
    'nav',
    '.row',
    '.entry',
    '.fa',
]


def gen(tag):
    return [
        (f' {tag} ', {}, {'pre': ' ', 'suf': ' '}),
        (f'{tag} ', {'position': 0}, {'pre': '', 'suf': ' '}),
        (f', {tag}, ', {}, {'pre': ', ', 'suf': ', '}),
        (f', {tag} ', {}, {'pre': ', ', 'suf': ' '}),
        (f'{tag},', {'position': 0}, {'pre': '', 'suf': ','}),
        (f' {tag}, ', {}, {'pre': ' ', 'suf': ', '}),

        (f'{tag}:', {'position': 0}, {'pre': '', 'suf': ':'}),
        (f' {tag}:', {}, {'pre': ' ', 'suf': ':'}), 
        (f', {tag}:', {}, {'pre': ', ', 'suf': ':'}), 
    ]

chunk = file.read()
lines = chunk.split('\n')
print('Total', len(lines), 'lines')

c = 0
t = 0
for i, l in enumerate(lines):

    modified=False
    nl = l
    for tag in html_tags:
        vars = gen(tag)
        
        for s, rules, fix in vars:
            if not s in l: continue
            broken = False
            if len(rules):
                for k, v in rules.items():
                    if not (k == 'position' and l.find(s) == v): 
                        broken = True
                        break                    
            if broken: continue
            new = fix['pre'] + tag + '.philosophy' + fix['suf']
            
            nl = nl.replace(s, new)
            modified = True
    if modified:
        print(f'[{i}]', end=' ')
        print(l, end='  --->  ')
        print(nl)
        c+=1
        mod.write(nl + '\n')
    else:
        mod.write(l + '\n')

            
                        
    
print('Total', c, 'variables affected')

