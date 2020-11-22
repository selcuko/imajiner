const capitalize = (s) => {
    if (typeof s !== 'string') return ''
    return s.charAt(0).toUpperCase() + s.slice(1)
}
const title = (s) => {
    return s.split(' ').map(p=>capitalize(p)).join(seperator=' ');
}