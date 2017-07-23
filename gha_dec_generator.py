from skyfield.api import load

planets = load('de421.bsp')
earth, mars = planets['earth'], planets['mars']
ts = load.timescale()

for i in range(366):
    for k in range(24):
        t = ts.utc(2017, 1, i, k)
        ra, dec, distance  = earth.at(t).observe(mars).apparent().radec(epoch='date')
        gha = 15*(t.gast - ra.hours)
        if gha < 0:
            print(t.utc_datetime(), 'GHA =', 360 + gha, 'Dec =', dec)
        else:
            print(t.utc_datetime(), 'GHA =', gha, 'Dec =', dec)


