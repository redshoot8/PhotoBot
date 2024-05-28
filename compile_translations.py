import polib

locales = ['en', 'ru']

for locale in locales:
    po_path = f'locale/{locale}/LC_MESSAGES/messages.po'
    mo_path = f'locale/{locale}/LC_MESSAGES/messages.mo'
    po = polib.pofile(po_path)
    po.save_as_mofile(mo_path)
