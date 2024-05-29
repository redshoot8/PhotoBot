import polib

locales = ['en', 'ru']

if __name__ == "__main__":
    for locale in locales:
        po_path = f'{locale}/LC_MESSAGES/messages.po'
        mo_path = f'{locale}/LC_MESSAGES/messages.mo'
        po = polib.pofile(po_path)
        po.save_as_mofile(mo_path)
    print("Translation files compiled successfully!")