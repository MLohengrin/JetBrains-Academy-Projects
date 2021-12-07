# University Admission Procedure

departments = {'Biotech': [], 'Chemistry': [], 'Engineering': [], 'Mathematics': [], 'Physics': []}
applicants = []

max_dep = int(input())

with open('applicants.txt') as f:
    id = 0
    for line in f:
        name, surname, grade_physics, grade_chemistry, grade_math, grade_computer, grade_extra, first, second, third = line.split()
        applicants.append({
            'id': id,
            'name': name,
            'surname': surname,
            'grade_physics': float(grade_physics),
            'grade_chemistry': float(grade_chemistry),
            'grade_math': float(grade_math),
            'grade_computer': float(grade_computer),
            'grade_extra': float(grade_extra),
            'first': first,
            'second': second,
            'third': third
        })
        id += 1


def is_available(dep):
    return len(departments[dep]) < max_dep


def bio_grade(student):
    return max(round((student['grade_physics'] + student['grade_chemistry']) / 2, 1), student['grade_extra'])


def chem_grade(student):
    return max(student['grade_chemistry'], student['grade_extra'])


def eng_grade(student):
    return max(round((student['grade_math'] + student['grade_computer']) / 2, 1), student['grade_extra'])


def mat_grade(student):
    return max(student['grade_math'], student['grade_extra'])


def phys_grade(student):
    return max(round((student['grade_physics'] + student['grade_math']) / 2, 1), student['grade_extra'])


def select_students(n_pref):
    global applicants
    if n_pref == 0:
        n_pref = 'first'
    elif n_pref == 1:
        n_pref = 'second'
    elif n_pref == 2:
        n_pref = 'third'
    else:
        print('Troppi giri di preferenza')

    bio_applicants = list()
    chem_applicants = list()
    eng_applicants = list()
    mat_applicants = list()
    phys_applicants = list()

    for student in applicants:
        if student[n_pref] == 'Biotech':
            bio_applicants.append(student)
        elif student[n_pref] == 'Chemistry':
            chem_applicants.append(student)
        elif student[n_pref] == 'Engineering':
            eng_applicants.append(student)
        elif student[n_pref] == 'Mathematics':
            mat_applicants.append(student)
        elif student[n_pref] == 'Physics':
            phys_applicants.append(student)
        else:
            print('Dipartimento inesistente')

    # applicants = sorted(applicants, key=lambda x: (x[n_pref], -x[2], x[0], x[1]))
    bio_applicants = sorted(bio_applicants, key=lambda x: (-bio_grade(x), x['name'], x['surname']))
    chem_applicants = sorted(chem_applicants, key=lambda x: (-chem_grade(x), x['name'], x['surname']))
    eng_applicants = sorted(eng_applicants, key=lambda x: (-eng_grade(x), x['name'], x['surname']))
    mat_applicants = sorted(mat_applicants, key=lambda x: (-mat_grade(x), x['name'], x['surname']))
    phys_applicants = sorted(phys_applicants, key=lambda x: (-phys_grade(x), x['name'], x['surname']))

    selected = list()
    for student in bio_applicants:
        if is_available('Biotech'):
            departments['Biotech'].append(student)
            selected.append(student['id'])
    for student in chem_applicants:
        if is_available('Chemistry'):
            departments['Chemistry'].append(student)
            selected.append(student['id'])
    for student in eng_applicants:
        if is_available('Engineering'):
            departments['Engineering'].append(student)
            selected.append(student['id'])
    for student in mat_applicants:
        if is_available('Mathematics'):
            departments['Mathematics'].append(student)
            selected.append(student['id'])
    for student in phys_applicants:
        if is_available('Physics'):
            departments['Physics'].append(student)
            selected.append(student['id'])

    blacklist = []
    for ind, student in enumerate(applicants):
        if student['id'] in selected:
            blacklist.append(ind)
    for x in reversed(blacklist):
        applicants.pop(x)


for n_pref in range(3):
    select_students(n_pref)


def dep_grade(dep, student):
    if dep == 'Biotech':
        grade = bio_grade(student)
    elif dep == 'Chemistry':
        grade = chem_grade(student)
    elif dep == 'Engineering':
        grade = eng_grade(student)
    elif dep == 'Mathematics':
        grade = mat_grade(student)
    elif dep == 'Physics':
        grade = phys_grade(student)
    return grade


def print_admitted():
    for dep in departments:
        sorted_applicants = sorted(departments[dep], key=lambda x: (-dep_grade(dep, x), x['name'], x['surname']))
        with open(f'{dep.lower()}.txt', 'w') as out:
            print(dep)
            for student in sorted_applicants:
                out.write(student['name'] + ' ' + student['surname'] + ' ' + str(dep_grade(dep, student)) + '\n')
        print()


print_admitted()
