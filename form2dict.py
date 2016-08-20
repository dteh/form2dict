# from lxml.html import parse

'''
form2dict @danielz_ / dteh
This takes an element tree from lxml parsed html and finds any forms within the input.
It generates a dictionary for each form with keys for each input element adn their corresponding values.
It wraps all dictionaries into a single dictionary.
The function also returns `factions` which is the action for each form (as a dictionary).

Useful for automating bot activities [however this will not work for forms where there are multiple
inputs with the same name (looking at you SUPREME).

The other issue is that if there are multiple fields with the same ID, the form inputs for both
will be MERGED.

kwargs:
    noscript (default = False)
        Includes input elements enclosed in noscript tags
    submit (default = False)
        Includes input elements that have the type "submit"


example use:

html = lxml.html.fromstring(somehtmlbytes)
form_actions, form_dictionaries = form2dict.parse_html(html,noscript=True)

'''


def parse_html(html, noscript=False, submit=False):
    forms = html.xpath('//form')
    form_dicts = {}
    factions = {}
    for i, form in enumerate(forms):
        try:
            fname = str(form.xpath('@id')[0])
        except:
            fname = i
        factions[fname] = str(form.xpath('@action')[0])
        fdict = {}

        if (submit and noscript):
            inputs = form.xpath('.//input')
            inputs += form.xpath('.//select')
        if not submit and noscript:
            inputs = form.xpath('.//input[@type!="submit"]')
            inputs += form.xpath('.//select[@type!="submit"]')
        if submit and not noscript:
            inputs = form.xpath('.//input[not(ancestor::noscript)]')
            inputs += form.xpath('.//select[not(ancestor::noscript)]')
        if not submit and not noscript:
            inputs = form.xpath('.//input[@type!="submit" and not(ancestor::noscript)]')
            inputs += form.xpath('.//select[@type!="submit" and not(ancestor::noscript)]')

        for input in inputs:
            fdict[input.name] = input.value

        # find inputs outside of forms (that belong to a form)
        query = '@form=\"' + str(fname) + '\"'
        for orphan_input in form.xpath('//@form/parent::*'):
            if orphan_input.xpath(query):
                fdict[orphan_input.name] = orphan_input.value
        try:
            form_dicts[fname].update(fdict)
        except:
            form_dicts[fname] = fdict

    return (factions, form_dicts)
