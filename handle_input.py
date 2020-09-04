import unidecode

def string_no_accent(string):
    return unidecode.unidecode(string).lower()

# print(string_no_accent("Nguyễn đức tới"))