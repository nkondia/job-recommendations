import requests
import re


NEGATIVE_DESCRIPTORS = [
    'outside of'
]
OVERRIDING_POSITIVE_DESCRIPTORS = [
    'relocate to'
]
OPERATOR_IS = 'IS'
OPERATOR_NOT = 'NOT'
KEY_WORD_EXTENSIONS = {
    'designer': ['design']
}

def get_input_data(type: str):
    response = requests.get(f"https://bn-hiring-challenge.fly.dev/{type}.json")
    return response.json()

def get_full_word_regex_pattern(word: str):
    return fr'\b{word}\b'

def is_negative_descriptor(descriptor: str):
    return descriptor in NEGATIVE_DESCRIPTORS

def is_overriding_positive_descriptor(descriptor: str):
    return descriptor in OVERRIDING_POSITIVE_DESCRIPTORS

def get_location_operator(negate: bool):
    return OPERATOR_NOT if negate else OPERATOR_IS

def extend_key_words(key_words: list[str]):
    return key_words + [ext for key_word in key_words for ext in KEY_WORD_EXTENSIONS.get(key_word.lower(), [])]



def main():
    members = get_input_data("members")
    jobs = get_input_data("jobs")
    locations = set()

    for job in jobs:
        key_words = job["title"].split()
        job["key_words"] = extend_key_words(key_words)
        locations.add(job["location"])

    for member in members:
        bio = member["bio"]
        job_matches = []
        for job in jobs:
            key_words = job["key_words"]
            for key_word in key_words:
                pattern = get_full_word_regex_pattern(key_word)
                if re.search(pattern, bio, re.IGNORECASE):
                    job_matches.append(job)
                    break

        raw_location_preferences = []
        for location in locations:
            pattern = get_full_word_regex_pattern(location)
            if re.search(pattern, bio, re.IGNORECASE):
                loc_index = bio.find(location)
                location_leading_words = bio[:loc_index].strip().split()[-2:]
                raw_location_preferences.append({
                    'descriptor': ' '.join(location_leading_words),
                    'location': location
                })

        recomended_jobs = []
        location_preference = {}
        if len(raw_location_preferences) == 1:
            negate = is_negative_descriptor(raw_location_preferences[0]["descriptor"])
            location_preference['operator'] = get_location_operator(negate)
            location_preference['location'] = raw_location_preferences[0]['location']
        elif len(raw_location_preferences) == 2:
            for raw_location_preference in raw_location_preferences:
                negate = is_negative_descriptor(raw_location_preference["descriptor"])
                location_operator = get_location_operator(negate)
                if not location_preference:
                    location_preference['location'] = raw_location_preference['location']
                    location_preference['operator'] = location_operator
                elif is_overriding_positive_descriptor(raw_location_preference['descriptor']):
                    location_preference['location'] = raw_location_preference['location']
                    location_preference['operator'] = location_operator

        if not location_preference:
            recomended_jobs.extend(job_matches)
        elif location_preference['operator'] == OPERATOR_IS:
            recomended_jobs.extend(
                [job for job in job_matches if job['location'] == location_preference['location']]
            )
        else:
            recomended_jobs.extend(
                [job for job in job_matches if job['location'] != location_preference['location']]
            )
        
        print(f"{member['name']} - {member['bio']}")
        formatted_recommendations = '\n'.join(
            [f"Title: {job['title']}; Location:{job['location']}" for job in recomended_jobs]
        )
        print(f"Recommended jobs for {member['name']}:\n{formatted_recommendations}\n")


if __name__ == "__main__":
    main()