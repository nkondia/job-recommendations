import re
import requests

from constants import OPERATOR_IS
from utils import extend_key_words, get_full_word_regex_pattern, get_location_operator, is_negative_descriptor, is_overriding_positive_descriptor



def get_input_data(type: str) -> list[dict]:
    try:
        response = requests.get(f"https://bn-hiring-challenge.fly.dev/{type}.json")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch {type} data: {e}")
        return []


def make_location_preference(raw_location_preferences: dict) -> dict:
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
    return location_preference

def make_raw_location_preferences(locations: list[str], bio: str) -> list[dict]:
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
    return raw_location_preferences

def make_recommended_jobs(location_preference: dict, job_matches: list[dict]) -> list[dict]:
    recomended_jobs = []

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
    
    return recomended_jobs

def output_recommendations(member: dict, recommended_jobs: list[dict]) -> None:
    print(f"{member['name']} - {member['bio']}")
    formatted_recommendations = '\n'.join(
        [f"Title: {job['title']}; Location:{job['location']}" for job in recommended_jobs]
    )
    print(f"Recommended jobs for {member['name']}:\n{formatted_recommendations}\n")


def process_jobs(jobs: list[dict]) -> tuple[list[dict], set]:
    locations = set()
    for job in jobs:
        key_words = job["title"].split()
        job["key_words"] = extend_key_words(key_words)
        locations.add(job["location"])
    return jobs, locations

def match_jobs_with_bio(jobs: list[dict], bio: str) -> list[dict]:
    job_matches = []
    for job in jobs:
        key_words = job["key_words"]
        for key_word in key_words:
            pattern = get_full_word_regex_pattern(key_word)
            if re.search(pattern, bio, re.IGNORECASE):
                job_matches.append(job)
                break
    return job_matches
