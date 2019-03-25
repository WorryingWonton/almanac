from datetime import datetime
import sys
from skyfield.api import load



def convert_to_date_time(date_string):
    try:
        date = datetime.strptime(date_string, '%m/%d/%Y %H')
        return date
    except ValueError:
        return None

class TabulatedValue:

    def __init__(self, date_time, body):
        self.date_time = date_time
        self.body = body
        self.gha = None
        self.dec = None
        self.sha = None
        self.l_v = None
        self.l_d = None
        self.l_m = None
        self.h_p = None
        self.s_d = None


class B2BPrediction:

    def __init__(self, name, observation_point):
        self.name = name
        if not observation_point:
            self.observer_location = 'earth'
        else:
            self.observer_location = observation_point

    def compute_angles_and_corrections(self, time):
        return {}

    def compute_angle(self, time, angle_type):
        pass

    def compute_dec(self, time):
        pass

    def compute_sr(self):
        pass

    def compute_bs(self):
        pass

#Distance from observer is less than 0.1 AU
class SatelliteBody(B2BPrediction):
    pass

#Distance from observer is between 0.1 AU and 50 AU
class NearBody(B2BPrediction):
    pass

#Distance from observer is greater than 50 AU
class FarBody(B2BPrediction):
    pass


class DMSAngle:

    def __init__(self, angle):
        self.angle = angle
        self.degrees = int(angle)
        self.minutes = int((angle - int(angle))*60)
        self.deci_minutes = round((angle - int(angle))*60, 1)
        self.seconds = int(((angle - int(angle))*60 - int(self.minutes))*60)

    def __str__(self):
        return f'{self.degrees}°{self.deci_minutes}\'' if self.deci_minutes >= 10 else f'{self.degrees}°0{self.deci_minutes}\''

def construct_bodies(body_list, observing_body, reference_body, observing_time):
    """
    Receives a list of strings representing different bodies, returns a list of Body objects.
    This method attempts to take a list of ideas
    :param body_list:  List of strings referring to various celestial bodies.
    :return List: List of NearBody or FarBody objects.
    """
    bodies = load('de422.bsp')
    for body_candidate in body_list:
        prediction_time = load.timescale().utc(observing_time.year, observing_time.month, observing_time.day - 1, observing_time.hour -1, observing_time.minute - 1)
        spherical_coords = bodies[reference_body].observe(body_list[observing_body]).at(prediction_time).apparent().raded(epoch='date')
        if spherical_coords[2] < 0.1:
            body_list.append(SatelliteBody())
        elif spherical_coords[2] < 50:
            pass
        else:
            pass



    return []

if __name__ == '__main__':
    if sys.argv[1]:
        print(convert_to_date_time(sys.argv[1]))


    #Find distance to each body from observer location
    #Generate a list of Near or Far Body objects by examining the distances found in the step above.
