import numpy as np
from math import radians, sin, asin
from collections import namedtuple


class CollimatorSection(object):
    r"""
    thickness: float
        Distance from upstream and downstream collimator faces, in mili-meters
    sample_distance: float
        Distance from the sample to the middle of the section, in mili-meters
    aperture: float
        Angle subtended by the section to the sample, in degrees
    """

    def __init__(self, thickness, sample_distance, aperture):
        self.thickness = thickness
        self.sample_distance = sample_distance
        self.aperture = aperture
        self.blade_angles = list()  # interior blade angles
        self.blade_thickness = 0.0

    @property
    def sample_upstream_distance(self):
        r"""Distance from sample to upstream collimator face"""
        return self.sample_distance - self.thickness / 2.0

    def n_blades_from_thickness(self, channel_thickness):
        r"""
        Number of interior blades given a channel thickness. Blade
        thickness is also taken into account.

        Calculations using the upstream face of the collimator section

        Parameters
        ----------
        channel_thickness: float

        Returns
        -------
        int
        """
        delta = 2 * asin((channel_thickness + self.blade_thickness)/
                         (2 * self.sample_upstream_distance))
        return int(radians(self.aperture) / delta - 1)

    def chanel_thickness(self, n_blades=None):
        r"""
        Chanel thickness given a number of interior blades. Blade
        thickness is also taken into account.

        Calculations using the upstream face of the collimator section.

        Parameters
        ----------
        n_blades: int
            Number of interior blades. If none, the number of blade angles
            is used

        Returns
        -------
        float
        """
        if n_blades is None:
            n_blades = self.n_blades
        delta = radians(self.aperture / (1 + n_blades))
        return 2 * self.sample_upstream_distance * sin(delta / 2) - self.blade_thickness

    def set_blade_angles(self, n_blades):
        r"""
        Angle positions of the blades. Origin of angles at the top surface.

        Parameters
        ----------
        n_blades: int
            number of interior blades

        Returns
        -------
        numpy.ndarray
        """
        delta = self.aperture / (1 + n_blades)
        self.blade_angles = delta * np.arange(1, 1 + n_blades)
        return self.blade_angles

    @property
    def n_blades(self):
        return len(self.blade_angles)

    def blade_blade_angle_distances(self, blade_angles):
        r"""
        In the boundary between two collimator sections, the interior
        blades of each collimator section may overlap on top of each other.
        Here we look at the upstream face of the collimator section, that is
        the boundary between this section and the collimator section
        immediately nearer to the sample.
        For each interior blade of the collimator section,
        we calculate the angle difference to each of the blades of the
        neighbor collimator section, retaining only the minimum of these
        differences.
        In the end, we obtain an angle difference between each blade of
        the collimator section and the set of blades from the neighbor
        collimator section.

        Parameters
        ----------
        blade_angles: numpy.ndarray
            Blade angle positions for the neighbor collimator section
        Returns
        -------
        numpy.ndarray
            Angle differences, in degrees
        """
        bbd = list()
        for angle in self.blade_angles:
            bbd.append(min(np.abs(blade_angles - angle)))
        return bbd

    def blade_blade_distances(self, blade_angles):
        r"""
        In the boundary between two collimator sections, the interior
        blades of each collimator section may overlap on top of each other.
        Here we look at the upstream face of the collimator section, that is
        the boundary between this section and the collimator section
        immediately nearer to the sample.
        For each interior blade of the collimator section,
        we calculate the distance to each of the blades of the
        neighbor collimator section, retaining only the minimum of these
        distances.
        In the end, we obtain a distance between each blade of
        the collimator section and the set of blades from the neighbor
        collimator section.

        Parameters
        ----------
        blade_angles: numpy.ndarray
            Blade angle positions for the neighbor collimator section

        Returns
        -------
        numpy.ndarray
            Distances between neighboring blades, in mili-meters
        """
        bbd = np.radians(self.blade_blade_angle_distances(blade_angles))
        return self.sample_upstream_distance * bbd

    def minimal_blade_blade_distance(self, blade_angles):
        r"""
        Minimal distance between the set of interior blades of the
        collimator section and the set of interior blades of the
        collimator section immediately nearer to the sample.

        Parameters
        ----------
        blade_angles: numpy.ndarray
            Blade angle positions for the neighbor collimator section

        Returns
        -------
        float
            Minimal distance, in mili-meters
        """
        return np.min(self.blade_blade_distances(blade_angles))


def valid_blade_pair_configurations(upstream_section, max_upstream_blades,
                                    downstream_section, max_downstream_blades,
                                    tolerance=1.0):
    r"""
    List of pairs, each pair containing a number of interior blades
    for the upstream collimator section and a number of interior blades
    for the downstream collimator section.
    For each valid pair, it is guaranteed that no blade from the upstream
    collimator is closer than the tolerance distance to any blade from the
    downstream collimator.
    Also for each pair, the minimal blade-to-blade distance is reported

    Parameters
    ----------
    upstream_section: CollimatorSection
        Upstream collimator section
    max_upstream_blades: int
        Maximum number of interior blades for the upstream collimator section
    downstream_section: CollimatorSection
        Downstream collimator section
    max_downstream_blades: int
        Maximum number of interior blades for the downstream collimator section
    tolerance: float
        Minimal blade-to-blade distance between adjacent collimator sections.

    Returns
    -------
    tuple
        Tuple containing a list of valid pairs and a list of minimal distances
    """
    valid_pairs = list()
    min_dists = list()
    for n_upstream_blades in range(1, 1 + max_upstream_blades):
        uba = upstream_section.set_blade_angles(n_upstream_blades)
        for n_downstream_blades in range(1, 1 + max_downstream_blades):
            downstream_section.set_blade_angles(n_downstream_blades)
            min_dist = downstream_section.minimal_blade_blade_distance(uba)
            if min_dist > tolerance:
                valid_pairs.append((n_upstream_blades, n_downstream_blades))
                min_dists.append(min_dist)
    return valid_pairs, min_dists


"""
`blades` is a tuple (n1, n2, n3) indicating the number of interior blades
    for the first, middle and last collimator sections
`d` is the minimal distance among all distances between blades
    of adjacent collimator sections
`widths` is a tuple (w1, w2, w3) indicating the channel width, or thickness,
    for each collimator section
"""
Triad = namedtuple('Triad', 'blades d widths')


def valid_blade_triad_configurations(sections, max_blades, tolerance=1.0):
    r"""
    List of triads, each triad containing number of interior blades for
    each collimator sections.
    For each triad, it is guaranteed that no blade from a collimator
    section is closer than the tolerance distance to any blade from the
    adjacent collimator(s).

    Parameters
    ----------
    sections: list
        List of collimator sections, beginning with the section closer to
        the sample
    max_blades: list
        Maximum number of interior blades per collimator section.
    tolerance: float
        Minimal blade-to-blade distance between adjacent collimator sections.

    Returns
    -------
    list
        a list of Triad objects
    """
    # Valid blade configurations between first and middle collimator sections
    args = [sections[0], max_blades[0], sections[1], max_blades[1]]
    pairs01, min_d01 = valid_blade_pair_configurations(*args,
                                                       tolerance=tolerance)
    # Valid blade configurations between middle and last collimator sections
    args = [sections[1], max_blades[1], sections[2], max_blades[2]]
    pairs12, min_d12 = valid_blade_pair_configurations(*args,
                                                       tolerance=tolerance)
    # Find valid blade configurations for the three collimator sections.
    triads = list()
    for i, (n_blades_0, n_blades_1_01) in enumerate(pairs01):
        for j, (n_blades_1_12, n_blades_2) in enumerate(pairs12):
            if n_blades_1_01 == n_blades_1_12:
                n_blades_1 = n_blades_1_12
                blades = [n_blades_0, n_blades_1, n_blades_2]
                mind_dist = min(min_d01[i], min_d12[j])
                channel_widths = [sections[k].chanel_thickness(n)
                                  for k, n in enumerate(blades)]
                triads.append(Triad(blades, mind_dist, channel_widths))
    return triads


def blade_configurations(upstream_distance, collimator_thickness, aperture,
                         minimum_channel_width=3.0, blade_thickness=1.0,
                         blade_gap=1.1):
    r"""
    List of blade configurations. Each configuratio avoids blade overlap
    between adjacent collimator sections.

    Parameters
    ----------
    upstream_distance: float
        Distance from sample to the upstream face of the collimator.
    thickness: float
        Distance of each collimator section. Assumed all three same thickness.
    aperture: float
        Collimator aperture angle, in degrees
    minimum_channel_width: float
        Units in mili meters
    blade_thickness: float
        Units in mili meters
    blade_gap: float
        Minimal distance between blades from adjacent sections

    Returns
    -------
    list
        List of Triad objects, that can later be filtered and sorted
    """
    sdds = list()  # distances from sample to collimator sections
    sdds.append(upstream_distance + collimator_thickness /2)
    sdds.append(sdds[0] + collimator_thickness)
    sdds.append(sdds[1] + collimator_thickness)
    sections = [CollimatorSection(collimator_thickness, sdd, aperture)
                for sdd in sdds]
    for s in sections:
        s.blade_thickness = blade_thickness
    max_n_blades = [s.n_blades_from_thickness(minimum_channel_width)
                    for s in sections]
    return valid_blade_triad_configurations(sections, max_n_blades, blade_gap)


def sort_filter_confs(confs, min_n_blades=None, max_channel_width=None,
                      sort_by_total_blades=False, sort_max_section_blades=None):
    r"""
    Sort or filter according to different criteria
    Parameters
    ----------
    confs: list
        List of Triad objects
    min_n_blades: int
        Discard Triads having one collimator section with a number of blades
        smaller than this number.
    max_channel_width: float
        Discard Triads having one collimator section with a channel width
        bigger than this value.
    sort_by_total_blades: Bool
        Sort by decreasing total number of blades in the collimator.
    sort_max_section_blades: str
        One of 'first', 'middle', 'last'. Sort list of Triads according to
        decreasing number of blades in either the 'first', 'middle', or
        'last' collimator section.
    Returns
    -------
    list
        sorted or filtered list of Triad objects
    """
    if isinstance(min_n_blades, int):
        filtered = list()
        for conf in confs:
            if min(conf.blades) >= min_n_blades:
                filtered.append(conf)
        return filtered
    if isinstance(max_channel_width, float) or\
       isinstance(max_channel_width, int):
        filtered = list()
        for conf in confs:
            if max(conf.widths) <= max_channel_width:
                filtered.append(conf)
        return filtered
    if sort_by_total_blades is True:
        def sorting_hat(c): return sum(c.blades)
        return sorted(confs, key=sorting_hat, reverse=True)
    if sort_max_section_blades is not None:
        def sorting_hat(c):
            options = ('first', 'middle', 'last')
            return c.blades[options.index(sort_max_section_blades)]
        return sorted(confs, key=sorting_hat, reverse=True)


if __name__ == '__main__':
    # distance from sample to upstream face of first section
    collimator_upstream_distance = 74
    thickness = 60  # collimator section thickness
    aperture = 26.5

    confs = blade_configurations(collimator_upstream_distance,
                                 thickness, aperture)
    # Filter out configurations with less than three blades in any
    # collimator section
    confs = sort_filter_confs(confs, min_n_blades=3)
    # Filter out configurations with a channel thickness bigger
    # than 9 mili meters
    confs = sort_filter_confs(confs, max_channel_width=9)
    # sort configurations by maximum total number of blades
    confs = sort_filter_confs(confs, sort_by_total_blades=True)
    # sort configurations by maximum number of blades in the first
    # collimator section
    confs = sort_filter_confs(confs, sort_max_section_blades='first')

print("I'll be back!")