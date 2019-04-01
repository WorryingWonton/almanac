from datetime import datetime, timedelta
import sys
from skyfield.api import load

class Almanac:

    def __init__(self, observer_location, reference_bodies, start_time, end_time, obs_interval, data_set=None):
        self.observer_location = observer_location
        self.reference_bodies = reference_bodies
        self.start_time = start_time
        self.end_time = end_time
        #obs_interval is the interval between observations as expressed in fractions of a day
        self.obs_interval = timedelta(days=1/int(obs_interval))
        if not data_set:
            self.data_set = load('de422.bsp')
        else:
            self.data_set = load(data_set)
        self.day_dict = {}
        self.timescale = load.timescale()

    def generate_bodies(self):
        self.reference_bodies = list(map(lambda ref_body: Body(name=ref_body, data_set=self.data_set), self.reference_bodies))
        self.observer_location = Body(name=self.observer_location, data_set=self.data_set)
        for body in self.reference_bodies:
            body.generate_body()
        self.observer_location.generate_body()

    def generate_radecs(self):
        observation_time = self.start_time
        while observation_time <= self.end_time:
            observation_dict = {}
            for body in self.reference_bodies:
                observation_dict[body.name] = body.generate_radec(observing_body=self.observer_location, time=observation_time, timescale=self.timescale)
            self.day_dict[observation_time] = observation_dict
            observation_time += self.obs_interval

    def build_tables(self):
        tables = f"Almanac viewed from {self.observer_location.name} between {self.start_time} and {self.end_time} measured every {self.obs_interval} hours"
        tables += "\n\t\t\t" + "\t\t\t\t".join([x.name.upper() for x in self.reference_bodies])
        tables += "\nTime\t\t\t{}".format("GHA\t\tDec\t\t" * len(self.reference_bodies))
        for obs_time in self.day_dict.keys():
            tables += f"\n{obs_time}\t"
            for angles in list(self.day_dict[obs_time].values()):
                tables += "{}\t{}\t".format(str(angles[0]), str(angles[1]))
        return tables


class Body:

    def __init__(self, name, data_set):
        self.name = name
        self.data_set = data_set
        self.obs_distance = None
        self.de_entry = None

    def generate_body(self):
        try:
            self.de_entry = self.data_set[self.name]
        except ValueError:
            return f'{self.name} not found in body data-base'

    def generate_radec(self, observing_body, time, timescale):
        time = timescale.utc(day=time.day, year=time.year, month=time.month, hour=time.hour)
        ra, dec, dist = observing_body.de_entry.at(time).observe(self.de_entry).radec(time)
        gha = 15*(time.gast - ra.hours)
        if gha < 0:
            return (DMSAngle(gha + 360), DMSAngle(dec.degrees))
        else:
            return (DMSAngle(gha), DMSAngle(dec.degrees))

class DMSAngle:

    def __init__(self, angle):
        self.angle = angle
        self.degrees = int(angle)
        self.minutes = (angle - int(angle))*60
        self.deci_minutes = round((angle - int(angle))*60, 1)
        self.seconds = int(((angle - int(angle))*60 - self.minutes)*60)

    def __str__(self):
        return f'{self.degrees}°{self.deci_minutes}\'' if self.deci_minutes >= 10 else f'{self.degrees}°{self.deci_minutes}\''


def convert_to_date_time(date_string):
    try:
        date = datetime.strptime(date_string, '%m-%d-%Y-%H')
        return date
    except ValueError:
        return None


if __name__ == '__main__':
    alm_instance = Almanac(observer_location=sys.argv[4], reference_bodies=sys.argv[5:], start_time=convert_to_date_time(sys.argv[1]), end_time=convert_to_date_time(sys.argv[2]), obs_interval=sys.argv[3])
    alm_instance.generate_bodies()
    alm_instance.generate_radecs()
    print(alm_instance.build_tables())