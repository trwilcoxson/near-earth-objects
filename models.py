"""Represent models for near-Earth objects and their close approaches.

The `NearEarthObject` class represents a near-Earth object. Each has a unique
primary designation, an optional unique name, an optional diameter, and a flag
for whether the object is potentially hazardous.

The `CloseApproach` class represents a close approach to Earth by an NEO. Each
has an approach datetime, a nominal approach distance, and a relative approach
velocity.

A `NearEarthObject` maintains a collection of its close approaches, and a
`CloseApproach` maintains a reference to its NEO.

The functions that construct these objects use information extracted from the
data files from NASA, so these objects should be able to handle all of the
quirks of the data set, such as missing names and unknown diameters.
"""
from helpers import cd_to_datetime, datetime_to_str


class NearEarthObject:
    """A near-Earth object (NEO).

    An NEO encapsulates semantic and physical parameters about the object, such
    as its primary designation (required, unique), IAU name (optional), diameter
    in kilometers (optional - sometimes unknown), and whether it's marked as
    potentially hazardous to Earth.

    A `NearEarthObject` also maintains a collection of its close approaches -
    initialized to an empty collection, but eventually populated in the
    `NEODatabase` constructor.
    """

    def __init__(self, designation='', name=None, diameter=float('nan'),
                 hazardous=False, **info):
        """Create a new `NearEarthObject`.

        :param designation: The primary designation of this NEO.
        :param name: The IAU name of this NEO (None if unnamed).
        :param diameter: The diameter of this NEO in km (NaN if unknown).
        :param hazardous: Whether this NEO is potentially hazardous.
        :param info: A dictionary of excess keyword arguments.
        """
        self.designation = str(designation)
        self.name = name if name else None
        self.diameter = float(diameter) if diameter else float('nan')
        self.hazardous = bool(hazardous)
        self.approaches = []

    @property
    def fullname(self):
        """Return a representation of the full name of this NEO."""
        if self.name:
            return f"{self.designation} ({self.name})"
        return f"{self.designation}"

    def __str__(self):
        """Return `str(self)`."""
        hazard_str = "is" if self.hazardous else "is not"
        return (f"NEO {self.fullname} has a diameter of {self.diameter:.3f} km "
                f"and {hazard_str} potentially hazardous.")

    def __repr__(self):
        """Return `repr(self)`, a computer-readable string representation of this object."""
        return (f"NearEarthObject(designation={self.designation!r}, name={self.name!r}, "
                f"diameter={self.diameter:.3f}, hazardous={self.hazardous!r})")

    def serialize(self):
        """Return a dictionary of attributes for serialization."""
        return {
            'designation': self.designation,
            'name': self.name if self.name else '',
            'diameter_km': self.diameter,
            'potentially_hazardous': self.hazardous,
        }


class CloseApproach:
    """A close approach to Earth by an NEO.

    A `CloseApproach` encapsulates information about the NEO's close approach to
    Earth, such as the date and time (in UTC) of closest approach, the nominal
    approach distance in astronomical units, and the relative approach velocity
    in kilometers per second.

    A `CloseApproach` also maintains a reference to its `NearEarthObject` -
    initially, this information (the NEO's primary designation) is saved in a
    private attribute, but the referenced NEO is eventually replaced in the
    `NEODatabase` constructor.
    """

    def __init__(self, designation='', time=None, distance=0.0, velocity=0.0,
                 neo=None, **info):
        """Create a new `CloseApproach`.

        :param designation: The primary designation of the approaching NEO.
        :param time: The date/time of closest approach (as a datetime or string).
        :param distance: The nominal approach distance in astronomical units.
        :param velocity: The relative approach velocity in km/s.
        :param neo: The NearEarthObject that made this close approach (initially None).
        :param info: A dictionary of excess keyword arguments.
        """
        self._designation = str(designation)
        if isinstance(time, str):
            self.time = cd_to_datetime(time)
        else:
            self.time = time
        self.distance = float(distance)
        self.velocity = float(velocity)
        self.neo = neo

    @property
    def time_str(self):
        """Return a formatted representation of this `CloseApproach`'s approach time."""
        if self.time:
            return datetime_to_str(self.time)
        return ''

    def __str__(self):
        """Return `str(self)`."""
        return (f"On {self.time_str}, '{self.neo.fullname if self.neo else self._designation}' "
                f"approaches Earth at a distance of {self.distance:.2f} au "
                f"and a velocity of {self.velocity:.2f} km/s.")

    def __repr__(self):
        """Return `repr(self)`, a computer-readable string representation of this object."""
        return (f"CloseApproach(time={self.time_str!r}, distance={self.distance:.2f}, "
                f"velocity={self.velocity:.2f}, neo={self.neo!r})")

    def serialize(self):
        """Return a dictionary of attributes for serialization."""
        return {
            'datetime_utc': self.time_str,
            'distance_au': self.distance,
            'velocity_km_s': self.velocity,
            'neo': self.neo.serialize() if self.neo else {},
        }
