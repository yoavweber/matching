
from collections import defaultdict
from matching.games import HospitalResident

import numpy as np
import yaml

NUM_RESIDENTS = 200
CAPACITY = 30
SEED = 0

# Fake data
resident_names = ["yoav", "tal", "may", "dor", "nir", "gil"]
hospital_names = [
    "fabio", "adam", "fabian"
]


def create_resident_to_preferences_map():
    """Create a map from resident names to an ordered subset of the hospital
    names."""

    resident_to_preference_size = {
        resident: np.random.randint(1, len(hospital_names) + 1)
        for resident in resident_names
    }

    print(resident_to_preference_size, "size")

    resident_to_preference_idxs = {
        resident: np.random.choice(
            len(hospital_names), size=size, replace=False
        )
        for resident, size in resident_to_preference_size.items()
    }

    print(resident_to_preference_idxs, "idxs")

    resident_to_preferences = {
        resident: np.array(hospital_names)[idxs].tolist()
        for resident, idxs in resident_to_preference_idxs.items()
    }
    students = {"yoav": ["fabio", "adam", "fabian"], "tal": [
        "fabian", "adam", "fabio"], "may": ["adam", "fabian", "fabio"], "dor": ["adam", "fabio", "fabian"], "gil": ["fabio", "adam", "fabian"], "nir": ["adam", "fabian", "fabio"]}
    # print(students, "prefrence")

    # print(resident_to_preferences, "!")

    return students


def create_hospital_to_preferences_map(resident_to_preferences):
    """Create a map from hospital names to a permutation of all those residents
    who ranked them."""

    hospital_to_residents = defaultdict(set)
    for resident, hospitals in resident_to_preferences.items():
        for hospital in hospitals:
            hospital_to_residents[hospital].add(resident)

    hospital_to_preferences = {
        hospital: np.random.permutation(list(residents)).tolist()
        for hospital, residents in hospital_to_residents.items()
    }
    print(hospital_to_preferences, "mentor prefrences")

    return hospital_to_preferences


def create_hospital_to_capacity_map():
    """ Create a map from hospital names to their capacity. """

    mentors = {"fabio": 3, "adam": 2, "fabian": 1}

    return mentors


def save_dictionaries_to_yaml(
    resident_preferences, hospital_preferences, capacities
):

    for dictionary, name in zip(
        (resident_preferences, hospital_preferences, capacities),
        ("residents", "hospitals", "capacities"),
    ):
        with open(f"{name}.yml", "w") as f:
            yaml.dump(dictionary, f, indent=4)


def main():
    """ Create the required maps to form the players, and then save them. """

    resident_preferences = create_resident_to_preferences_map()
    hospital_preferences = create_hospital_to_preferences_map(
        resident_preferences
    )
    capacities = create_hospital_to_capacity_map()
    print(capacities, "!!!!")
    print("Player dictionaries created...")

    save_dictionaries_to_yaml(
        resident_preferences, hospital_preferences, capacities
    )

    game = HospitalResident.create_from_dictionaries(
        resident_preferences, hospital_preferences, capacities
    )

    matching = game.solve(optimal="resident")
    print(matching, "Dictionaries saved.")


if __name__ == "__main__":
    main()
