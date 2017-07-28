from skyfield.api import load
from skyfield.units import Angle
import datetime

class Planet:
    def __init__(self, obs_planet_name, ref_planet_name, start_date, timewindow):
        '''
        :param obs_planet_name: Observed Planet Name
        :param ref_planet_name: Reference Planet Name  (where the observer is located)
        :param start_date: Almanac Start Date
        :param timewindow: Alamanac Time Windown (days)
        '''
        self.obs_planet_name = obs_planet_name.lower()
        self.ref_planet_name = ref_planet_name.lower()
        self.start_date = start_date
        self.timewindow = timewindow
        if self.obs_planet_name == 'jupiter' or 'saturn':
            self.obs_planet_name += ' barycenter'

    def gha_dec_generator(self):
        planets = load('de422.bsp')
        ts = load.timescale()
        for day in range(self.timewindow):
            for hour in range(24):
                t = ts.utc(self.start_date.year, self.start_date.month, day + self.start_date.day, hour)
                ra, dec, distance  = planets[self.ref_planet_name].at(t).observe(planets[self.obs_planet_name]).apparent().radec(epoch='date')
                gha = 15*(t.gast - ra.hours)
                if gha < 0:
                    print(f'{t.utc_datetime()}, GHA = {Angle(degrees= gha + 360)}, Dec = {dec}')
                else:
                    print(f'{t.utc_datetime()}, GHA = {Angle(degrees= gha)}, Dec = {dec}')

f37 = Planet('jupiter', 'earth', datetime.date(1981,3,20), 2)
f37.gha_dec_generator()

