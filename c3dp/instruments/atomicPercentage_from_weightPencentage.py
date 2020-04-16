from collections import OrderedDict

def atomic_percentage_from_weight_percentage(weight_percentage=OrderedDict(), atomic_weight=OrderedDict()):
    """
    
    calculating atomic percentage from weight percentage

    Parameters
    ----------
    weight_percentage: ordered dictionary
        elements as keys and their weight percentage as values in a component
    atomic_weight: ordered dictionary
        elements as keys and their atomic weights as values in a component

    Returns
    -------
    atomic percentage: ordered dictionary
            elements as keys and their atomic percentage as values in a component

    """
    number_of_atoms = {}
    atomic_percentage = OrderedDict()
    Avogrados_number = 6.023e23
    for k in weight_percentage.keys():
        number_of_atoms[k] = weight_percentage[k]*Avogrados_number/atomic_weight[k]

    total_number_atoms = sum(number_of_atoms.values())

    for k in weight_percentage.keys():
        atomic_percentage[k] = number_of_atoms[k]*100. / total_number_atoms

    return (atomic_percentage)
