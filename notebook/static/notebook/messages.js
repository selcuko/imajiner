const statusMessage = {
    syncing: capitalize(gettext('syncing')) + '...',
    waiting: capitalize(gettext('waiting for you')) + '.',
    responseNotOk: gettext('Something bad happened. You better save your writing somewhere else manually.'),
    languageNotOk: gettext("We couldn't detect the language of this masterpiece, therefore it won't be visible to public."),
    autosaveOk: gettext('Changes are saved.'),
    proceedAnyway: capitalize(gettext('proceed anyway')),
    processing: capitalize(gettext('processing')) + '...',
}


const titleSuffix = ' • Imajiner';
const titleDefault = title(gettext('entitled narrative'));