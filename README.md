# form2dict
This takes an element tree from lxml parsed html and finds any forms within the input.
It generates a dictionary for each form with keys for each input element adn their corresponding values.
It wraps all dictionaries into a single dictionary.
The function also returns `factions` which is the action for each form (as a dictionary).

Useful for automating bot activities [however this will not work for forms where there are multiple
inputs with the same name (looking at you SUPREME).

The other issue is that if there are multiple fields with the same ID, the form inputs for both
will be MERGED.

 @danielz_ / dteh

# kwargs:
    noscript (default = False)
        Includes input elements enclosed in noscript tags
    submit (default = False)
        Includes input elements that have the type "submit"


# example use:

html = lxml.html.fromstring(somehtmlbytes)
form_actions, form_dictionaries = form2dict.parse_html(html,noscript=True)