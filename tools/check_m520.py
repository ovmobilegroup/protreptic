from thinking_mode_selector import MODES_DATA
zh_modes = MODES_DATA['zh']
for k in range(518, 540):
    ks = str(k)
    if ks in zh_modes:
        print(f'M{k}: EXISTS - {zh_modes[ks][0]}')
    else:
        print(f'M{k}: MISSING')