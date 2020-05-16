def get_platforms(values):
    platforms = []
    for item in values:
        platform = item.split(" ")[-1]
        if platform == 'win':
            platforms.append('Windows')
        if platform == 'mac':
            platforms.append('Mac OS')
        if platform == 'linux':
            platforms.append('Linux')
        if platform == 'vr_required':
            platforms.append('VR Only')
        if platform == 'vr_supported':
            platforms.append('VR Supported')
    return platforms

values = [
    'win',
    'mac',
    'linux',
    'vr_required',
    'vr_supported'
]

print(get_platforms(values))