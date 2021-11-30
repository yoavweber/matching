
from collections import defaultdict
from matching.games import HospitalResident

import numpy as np


# Fake data
student_names = ["yoav", "tal", "may", "dor", "nir", "gil"]
mentor_names = [
    "fabio", "adam", "fabian"
]

students = {"yoav": ["fabio", "adam", "fabian"], "tal": [
    "fabian", "adam", "fabio"], "may": ["adam", "fabian", "fabio"], "dor": ["adam", "fabio", "fabian"], "gil": ["fabio", "adam", "fabian"], "nir": ["adam", "fabian", "fabio"]}

mentor_capacity = {"fabio": 3, "adam": 2, "fabian": 1}


def create_mentor_to_preferences_map(student_to_preferences):
    """Create a map from hospital names to a permutation of all those residents
    who ranked them."""

    hospital_to_residents = defaultdict(set)
    for resident, hospitals in student_to_preferences.items():
        for hospital in hospitals:
            hospital_to_residents[hospital].add(resident)

    hospital_to_preferences = {
        hospital: np.random.permutation(list(residents)).tolist()
        for hospital, residents in hospital_to_residents.items()
    }

    return hospital_to_preferences


def main():

    # this is required in the algorithm, but don't have any wight
    mentor_preferences = create_mentor_to_preferences_map(
        students
    )

    game = HospitalResident.create_from_dictionaries(
        students, mentor_preferences, mentor_capacity
    )

    # optimizing the algorithem to match the students
    matching = game.solve(optimal="resident")
    print("matching: ", matching)


if __name__ == "__main__":
    main()
