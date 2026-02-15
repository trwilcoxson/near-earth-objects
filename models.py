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
import logging

from helpers import cd_to_datetime, datetime_to_str

logger = logging.getLogger(__name__)


class NearEarthObject:
    """A near-Earth object (NEO).

    An NEO encapsulates semantic and physical parameters about the
    object, such as its primary designation (required, unique), IAU
    name (optional), diameter in kilometers (optional - sometimes
    unknown), and whether it's marked as potentially hazardous to
    Earth.

    A `NearEarthObject` also maintains a collection of its close approaches -
    initialized to an empty collection, but eventually populated in the
    `NEODatabase` constructor.
    """

    def __init__(self, **info):
        """Create a new `NearEarthObject`.

        :param info: A dictionary of excess keyword arguments supplied to
            the constructor.
        """
        self.designation = str(info.get('designation', ''))
        name = info.get('name', None)
        self.name = name if name else None

        diameter = info.get('diameter', float('nan'))
        try:
            self.diameter = float(diameter) if diameter != '' else float('nan')
        except (ValueError, TypeError):
            self.diameter = float('nan')

        hazardous = info.get('hazardous', False)
        if isinstance(hazardous, str):
            self.hazardous = hazardous.upper() == 'Y'
        else:
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
        return (
            f"NEO {self.fullname} has a diameter of {self.diameter:.3f} km "
            f"and {hazard_str} potentially hazardous."
        )

    def __repr__(self):
        """Return `repr(self)`."""
        return (
            f"NearEarthObject(designation={self.designation!r}, "
            f"name={self.name!r}, "
            f"diameter={self.diameter:.3f}, "
            f"hazardous={self.hazardous!r})"
        )

    def serialize(self):
        """Produce a dictionary of attributes for CSV/JSON serialization.

        :return: A dictionary of this NEO's attributes.
        """
        return {
            'designation': self.designation,
            'name': self.name if self.name else '',
            'diameter_km': self.diameter,
            'potentially_hazardous': self.hazardous,
        }


class CloseApproach:
    """A close approach to Earth by an NEO.

    A `CloseApproach` encapsulates information about the NEO's close
    approach to Earth, such as the date and time (in UTC) of closest
    approach, the nominal approach distance in astronomical units, and
    the relative approach velocity in kilometers per second.

    A `CloseApproach` also maintains a reference to its `NearEarthObject` -
    initially, this information (the NEO's primary designation) is saved in a
    private attribute, but the referenced NEO is eventually replaced in the
    `NEODatabase` constructor.
    """

    def __init__(self, **info):
        """Create a new `CloseApproach`.

        :param info: A dictionary of excess keyword arguments supplied to
            the constructor.
        """
        self._designation = str(info.get('designation', ''))

        time = info.get('time', None)
        if isinstance(time, str):
            self.time = cd_to_datetime(time)
        else:
            self.time = time

        self.distance = float(info.get('distance', 0.0))
        self.velocity = float(info.get('velocity', 0.0))
        self.neo = None

    @property
    def time_str(self):
        """Return a formatted representation of this approach time.

        The value in `self.time` should be a Python `datetime` object.
        While a `datetime` object has a string representation, the
        default representation includes seconds - significant figures
        that don't exist in our input data set.

        The `datetime_to_str` method converts a `datetime` object to a
        formatted string that can be used in human-readable representations and
        in serialization to CSV and JSON files.
        """
        return datetime_to_str(self.time)

    def __str__(self):
        """Return `str(self)`."""
        return (
            f"On {self.time_str}, '{self.neo.fullname}' approaches Earth "
            f"at a distance of {self.distance:.2f} au and a velocity of "
            f"{self.velocity:.2f} km/s."
        )

    def __repr__(self):
        """Return `repr(self)`."""
        return (
            f"CloseApproach(time={self.time_str!r}, "
            f"distance={self.distance:.2f}, "
            f"velocity={self.velocity:.2f}, neo={self.neo!r})"
        )

    def serialize(self):
        """Produce a dictionary of attributes for CSV/JSON serialization.

        :return: A dictionary of this close approach's attributes.
        """
        return {
            'datetime_utc': self.time_str,
            'distance_au': self.distance,
            'velocity_km_s': self.velocity,
        }
