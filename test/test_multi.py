from pipeline.multi_runner import run_multiple_patients

patients = [
    {
        "patient_data": {
            "name": "Anonymous-1",
            "age": 21,
            "gender": "male",
            "known_conditions": ["anxiety"],
            "medications": [],
            "past_similar_episodes": True,
        },
        "episode_data": {
            "symptoms": [
                "sudden fear",
                "heart racing",
                "shortness of breath",
                "dizziness",
            ],
            "duration_minutes": 10,
            "severity": 7,
            "triggers": ["stress"],
        },
    },
    {
        "patient_data": {
            "name": "Anonymous-2",
            "age": 45,
            "gender": "female",
            "known_conditions": ["hypertension"],
            "medications": ["amlodipine"],
            "past_similar_episodes": False,
        },
        "episode_data": {
            "symptoms": [
                "chest tightness",
                "palpitations",
                "lightheadedness",
            ],
            "duration_minutes": 20,
            "severity": 6,
            "triggers": ["physical exertion"],
        },
    },
    {
        "patient_data": {
            "name": "Anonymous-3",
            "age": 30,
            "gender": "male",
            "known_conditions": [],
            "medications": [],
            "past_similar_episodes": False,
        },
        "episode_data": {
            "symptoms": [
                "shortness of breath",
                "tingling in hands",
                "sense of impending doom",
            ],
            "duration_minutes": 15,
            "severity": 8,
            "triggers": ["crowded place"],
        },
    },
]

run_multiple_patients(patients)
