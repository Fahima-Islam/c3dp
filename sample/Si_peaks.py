from mccomponents.sample.diffraction.SimplePowderDiffractionKernel import Peak

peaks = [
    Peak(q=2.0040025900612473, F_squared=542.0969307916806, multiplicity=8, intrinsic_line_width=0, DebyeWaller_factor=0),
    Peak(q=3.272522525910632, F_squared=1054.1698472687892, multiplicity=12, intrinsic_line_width=0, DebyeWaller_factor=0),
    Peak(q=3.837372807477102, F_squared=518.2780088084941, multiplicity=24, intrinsic_line_width=0, DebyeWaller_factor=0),
    Peak(q=4.628045739314274, F_squared=1007.8512132332618, multiplicity=6, intrinsic_line_width=0, DebyeWaller_factor=0),
    Peak(q=5.043295920938727, F_squared=495.5056543526544, multiplicity=24, intrinsic_line_width=0, DebyeWaller_factor=0),
    Peak(q=5.668175283790852, F_squared=963.5677501566406, multiplicity=24, intrinsic_line_width=0, DebyeWaller_factor=0),
    Peak(q=6.012007770183743, F_squared=473.73388282460456, multiplicity=24, intrinsic_line_width=0, DebyeWaller_factor=0),
    Peak(q=6.012007770183743, F_squared=473.73388282460485, multiplicity=8, intrinsic_line_width=0, DebyeWaller_factor=0),
    Peak(q=6.545045051821264, F_squared=921.2300356948058, multiplicity=12, intrinsic_line_width=0, DebyeWaller_factor=0),
    Peak(q=6.844971958404374, F_squared=452.91873011877385, multiplicity=48, intrinsic_line_width=0, DebyeWaller_factor=0),
    Peak(q=7.58703135580279, F_squared=433.01816384611783, multiplicity=24, intrinsic_line_width=0, DebyeWaller_factor=0),
    Peak(q=8.016010360244989, F_squared=842.0536360160481, multiplicity=8, intrinsic_line_width=0, DebyeWaller_factor=0),
    Peak(q=8.262714352833893, F_squared=413.9919984574102, multiplicity=24, intrinsic_line_width=0, DebyeWaller_factor=0),
    Peak(q=8.887173462868818, F_squared=395.80181409588045, multiplicity=24, intrinsic_line_width=0, DebyeWaller_factor=0),
    Peak(q=10.020012950306239, F_squared=361.7840754071958, multiplicity=8, intrinsic_line_width=0, DebyeWaller_factor=0),
    ]

# unit: \AA
unitcell_volume = 160.149892567

# unit: barns
class cross_sections:
    coh = 0
    inc = 0
    abs = 1.368
