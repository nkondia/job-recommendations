
from helpers import (
    get_input_data,
    make_location_preference,
    make_raw_location_preferences,
    make_recommended_jobs,
    match_jobs_with_bio,
    output_recommendations,
    process_jobs
)


def main():
    members = get_input_data("members")
    jobs = get_input_data("jobs")
    jobs, locations = process_jobs(jobs)
    
    for member in members:
        bio = member["bio"]
        job_matches = match_jobs_with_bio(jobs, bio)
        raw_location_preferences = make_raw_location_preferences(locations, bio)
        location_preference = make_location_preference(raw_location_preferences)
        recommended_jobs = make_recommended_jobs(location_preference, job_matches)

        output_recommendations(member, recommended_jobs)


if __name__ == "__main__":
    main()