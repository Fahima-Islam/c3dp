from collections import OrderedDict
# elements_number_of_atoms_gasket = [(k,elements_weight_percentage_gasket[k]*
#                                    Avogrados_number/atomic_weight[k])for k in
#                                    elements_weight_percentage_gasket.keys()]
# elements_number_of_atoms_gasket= {}
# elements_number_of_atoms_seat= {}


def atomic_percentage_from_weight_percentage(weight_percentage=OrderedDict(), atomic_weight=OrderedDict()):
    number_of_atoms = {}
    atomic_percentage = OrderedDict()
    Avogrados_number = 6.023e23
    for k in weight_percentage.keys():
        number_of_atoms[k] = weight_percentage[k]*Avogrados_number/atomic_weight[k]

    total_number_atoms = sum(number_of_atoms.values())
    # sorted(counter.keys(), key=lambda c: sentence.find(c)])
    # for k in sorted(weight_percentage.keys(), key=lambda k: weight_percentage.keys()):
    for k in weight_percentage.keys():
        atomic_percentage[k] = number_of_atoms[k]*100. / total_number_atoms

    return (atomic_percentage)
