class Peak:
    def __init__(self, label='Si 111', d_spacing=3.345, d_min=3., d_max=3.5):
        self.label = label
        self.d_spacing = d_spacing
        self.dmin = d_min
        self.dmax = d_max

Si_111_peak = Peak(label='Si 111', d_spacing=3.345, d_min=3., d_max=3.5)
Al_111_peak = Peak(label='Al 111', d_spacing=2.3, d_min=2.2, d_max=2.5)
Cu_111_peak = Peak(label='Cu 111', d_spacing=2.08, d_min=2., d_max=2.1)
Si_220_peak = Peak(label='Si 220', d_spacing=1.9, d_min=1.86, d_max=2)
Cu_200_peak = Peak(label='Cu 200', d_spacing=1.8, d_min=1.78, d_max=1.85)
