import normal_modes_tools as nmt
from normal_modes_tools.decomposition import find_nmodes_displacement
from normal_modes_tools.conversions import aa_to_au, dq_to_dQ
from normal_modes_tools.huang_rhys_factors import huang_rhys_factor


x_nms = nmt.xyz_file_to_NormalModesList('../data/f0_Mulliken.xyz')
a_nms = nmt.xyz_file_to_NormalModesList('../data/f0a_Mulliken.xyz')

g0_geom = x_nms[0].at
g0a_geom = a_nms[0].at

g0a_m_g0_nmodes = find_nmodes_displacement(
    start=g0_geom,
    end=g0a_geom,
    nmodes=x_nms,
)

for idx, (mode, dq) in enumerate(zip(x_nms, g0a_m_g0_nmodes), start=1):
    dQ = dq_to_dQ(dq=dq, wavenumber=mode.frequency)
    print(f'{idx:2d} {mode.frequency:4.0f} {dq:8.4f} {dQ:8.4f}'
          f' {huang_rhys_factor(dq, mode.frequency):3.1f}')

g0a_m_g0_nmodes *= aa_to_au
