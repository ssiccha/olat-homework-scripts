__all__ = ['find_student']

def substitute_umlauts(s):
    s = s.replace('ö', 'oe')
    s = s.replace('ä', 'ae')
    s = s.replace('ü', 'ue')
    return s

# We try to deduce Vorname and Nachname of the student from `folder_name`.
# The `folder_name` created by Olat is of the form
# Nachname_Vorname_UniqueIdentifier, where Olat chooses some unique identifier
# for each student (I have no idea how). If Vorname or Nachname consists of
# several names, then they again are separated by underscores.
def find_student(folder_name, table):
    folder_name_parts = folder_name.split('_')
    folder_name_parts = [part.casefold() for part in folder_name_parts]
    for student in table:
        first_name = substitute_umlauts(student["Vorname"].casefold())
        first_name = first_name.split(' ')
        last_name = substitute_umlauts(student["Nachname"].casefold())
        last_name = last_name.split(' ')
        l = len(folder_name_parts)
        # First we check which of the first parts of `folder_name` correspond
        # to the last name. Then we check which following parts correspond to
        # the first name.
        for i in range(l-1):
            if (last_name == folder_name_parts[0:i]):
                for j in range(i+1, l):
                    if first_name == folder_name_parts[i:j]:
                        return student
    print("Did not find student with folder " + ' '.join(folder_name_parts))
    return False

