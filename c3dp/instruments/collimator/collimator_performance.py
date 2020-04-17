import numpy as np

def collimator_inefficiency(diffraction_pattern,scattered_beam_intensity):
    """
    calculing collimator inefficiency
    Parameters
    ----------
    diffraction_pattern: tuple
        tuple of d-spacing, intensity and error
    scattered_beam_intensity: float
        scattered beam intensity to be fed to collimator

    Returns
    -------
        collimator performance : float
    """

    dcs, I_d, error = diffraction_pattern
    Si_peak_int = I_d[ (dcs<3.5) & (dcs>3)].sum()

    Cu_peak_int=I_d[np.logical_and(dcs<2.2, dcs>2)].sum()

    collimator_performance=(Cu_peak_int/Si_peak_int)+(1-Si_peak_int/scattered_beam_intensity)

    return (collimator_performance)



