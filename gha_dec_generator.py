from skyfield.api import load
from skyfield.units import Angle
import datetime
from math import atan, degrees

class Solar_System:
    def __init__(self, obs_body_name, ref_body_name, start_date, timewindow):
        '''
        :param obs_body_name: Observed Planet Name
        :param ref_body_name: Reference Planet Name  (where the observer is located)
        :param start_date: Almanac Start Date
        :param timewindow: Alamanac Time Window (days)
        '''
        if obs_body_name.lower() in ['jupiter', 'saturn', 'uranus', 'neptune', 'pluto']:
            self.obs_body_name = f'{obs_body_name.lower()} barycenter'
        else:
            self.obs_body_name = obs_body_name.lower()
        if ref_body_name.lower() in ['jupiter', 'saturn', 'uranus', 'neptune', 'pluto']:
            self.ref_body_name = f'{ref_body_name.lower()} barycenter'
        else:
            self.ref_body_name = ref_body_name.lower()
        self.start_date = start_date
        self.timewindow = timewindow

    def almanac_generator(self):
        pass

    #Generates gha, dec, hp, SD, d, and v for selected in system bodies.
    def gha_dec_hp(self):
        planets = load('de422.bsp')
        ts = load.timescale()
        # variable radii contains equatorial radii of key solar system objects, used to compute semi-diameter and horizontal parallax.
        radii = {'sun': 695700,
                 'mercury': 2349.7,
                 'venus': 6051.8,
                 'earth': 6378.1,
                 'moon': 1738.1,
                 'mars': 3396.2,
                 'jupiter barycenter': 71492,
                 'saturn barycenter': 60268,
                 'uranus barycenter': 25559,
                 'neptune barycenter': 24764,
                 'pluto barycenter': 1187}
        for day in range(self.timewindow):
            for hour in range(24):
                t = ts.utc(self.start_date.year, self.start_date.month, day + self.start_date.day, hour)
                t2 = ts.utc(self.start_date.year, self.start_date.month, day + self.start_date.day, hour -1)
                ra, dec, distance  = planets[self.ref_body_name].at(t).observe(planets[self.obs_body_name]).apparent().radec(epoch='date')
                ra2, dec2, distance2  = planets[self.ref_body_name].at(t2).observe(planets[self.obs_body_name]).apparent().radec(epoch='date')
                gha = 15*(t.gast - ra.hours)
                gha2 = 15*(t2.gast - ra2.hours)
                hp = Angle(degrees= degrees(atan(radii[self.ref_body_name]/distance.km)))

                if gha < 0:
                    print(f'{t.utc_datetime()}, GHA = {Angle(degrees= gha + 360)}, Dec = {dec}, HP = {hp}, v = {Angle(degrees= abs(14.313333 - abs(gha - gha2)))}')
                else:
                    print(f'{t.utc_datetime()}, GHA = {Angle(degrees= gha)}, Dec = {dec}, HP = {hp}, v = {Angle(degrees= abs(14.313333 - abs(gha - gha2)))}')
                if hour == 0 and day > 0:
                    # 'p' denotes previous, tp is 1 hour behind t.
                    tp = ts.utc(self.start_date.year, self.start_date.month, day + self.start_date.day - 1, hour - 1)
                    rap, decp, distancep = planets[self.ref_body_name].at(tp).observe(planets[self.obs_body_name]).apparent().radec(epoch='date')
                    sd = Angle(degrees=degrees(atan(radii[self.obs_body_name] / distancep.km)))
                    print(f'SD: {sd}')
                    print('\n')

    def v_d_generator(self):
        pass

    def sd_generator(self):
        pass

f37 = Solar_System('moon', 'earth', datetime.date(2017,1,1), 4)
f37.gha_dec_hp()

