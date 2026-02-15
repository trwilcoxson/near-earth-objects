"""Extract data on near-Earth objects and close approaches from CSV and JSON files.

The `load_neos` function extracts NEO data from a CSV file, formatted as
described in the project instructions, into a collection of `NearEarthObject`s.

The `load_approaches` function extracts close approach data from a JSON file,
formatted as described in the project instructions, into a collection of
`CloseApproach` objects.

The main module calls these functions with the arguments provided at the command
line, and uses the resulting collections to build an `NEODatabase`.
"""
import csv
import json

from models import NearEarthObject, CloseApproach


def load_neos(neo_csv_path):
    """Read near-Earth object information from a CSV file.

    :param neo_csv_path: A path to a CSV file containing data about near-Earth objects.
    :return: A collection of `NearEarthObject`s.
    """
    neos = []
    with open(neo_csv_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            designation = row['pdes']
            name = row['name'] if row['name'] else None
            diameter = float(row['diameter']) if row['diameter'] else float('nan')
            hazardous = (row['pha'] == 'Y')
            neos.append(NearEarthObject(
                designation=designation,
                name=name,
                diameter=diameter,
                hazardous=hazardous,
            ))
    return neos


def load_approaches(cad_json_path):
    """Read close approach data from a JSON file.

    :param cad_json_path: A path to a JSON file containing data about close approaches.
    :return: A collection of `CloseApproach`es.
    """
    approaches = []
    with open(cad_json_path, 'r') as f:
        data = json.load(f)

    for row in data['data']:
        # Fields: des, orbit_id, jd, cd, dist, dist_min, dist_max, v_rel, v_inf, t_sigma_f, h
        designation = row[0]
        time = row[3]
        distance = float(row[4])
        velocity = float(row[7])
        approaches.append(CloseApproach(
            designation=designation,
            time=time,
            distance=distance,
            velocity=velocity,
        ))
    return approaches
