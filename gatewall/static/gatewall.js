const defaultRedirectPath = '/';

const query = window.location.search;
const urlParams = new URLSearchParams(query);
const next = urlParams.has('next') ? urlParams.get('next') : defaultRedirectPath;
const auto = urlParams.has('espresso') ? true : false;

const redirect = () => { window.location.href = next; }