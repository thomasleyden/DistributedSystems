#A = Array of Applicants with each a list of preferences
#P = Array of Posts
#N = Number of Applicants and Posts

#Lets create tests with N = 5 Mac

#Applicant_array meaning -> 0 no preference


### Notes
### https://discrete.openmathbooks.org/dmoi3/sec_matchings.html
### https://www.youtube.com/watch?v=i5AWE-OoOsY
### https://en.wikipedia.org/wiki/Stable_marriage_with_indifference

import copy
from colorama import Fore, Back, Style

test_cases = []
# Test Case 1
applicant_array =  [[1, 0, 0],
                    [0, 1, 0],
                    [0, 0, 1]]

is_applicant_complete = True
test_cases.append((applicant_array, is_applicant_complete))

# Test Case 2
applicant_array =  [[1, 0, 0],
                    [1, 0, 0],
                    [1, 0, 0]]

is_applicant_complete = False
test_cases.append((applicant_array, is_applicant_complete))

# Test Case 3
applicant_array =  [[1, 0, 0, 0],
                    [0, 1, 0, 0],
                    [0, 1, 2, 0],
                    [0, 0, 0, 1]]
is_applicant_complete = True
test_cases.append((applicant_array, is_applicant_complete))

# Test Case 4
applicant_array =  [[1, 0, 0, 0],
                    [0, 1, 0, 0],
                    [0, 1, 2, 0],
                    [2, 0, 0, 1]]
is_applicant_complete = True
test_cases.append((applicant_array, is_applicant_complete))

# Test Case 5
applicant_array =  [[1, 0, 0, 2],
                    [0, 1, 2, 0],
                    [0, 0, 1, 2],
                    [1, 0, 2, 0]]
is_applicant_complete = True
test_cases.append((applicant_array, is_applicant_complete))

# Test Case 5
applicant_array =  [[1, 0, 0, 2],
                    [0, 1, 2, 0],
                    [0, 0, 1, 2],
                    [0, 0, 2, 1]]
is_applicant_complete = True
test_cases.append((applicant_array, is_applicant_complete))

# Test Case 6
applicant_array =  [[1, 2, 0],
                    [0, 1, 2],
                    [0, 2, 1]]
is_applicant_complete = True
test_cases.append((applicant_array, is_applicant_complete))

# Test Case 7
applicant_array =  [[1, 2, 0, 0, 0, 0, 0, 0, 0],
                    [0, 2, 0, 1, 3, 0, 0, 0, 0],
                    [0, 0, 2, 1, 3, 0, 0, 0, 0],
                    [1, 3, 2, 0, 0, 0, 0, 0, 0],
                    [0, 2, 0, 0, 1, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 2, 1, 0, 0],
                    [0, 0, 0, 0, 0, 0, 1, 2, 0],
                    [0, 0, 0, 0, 0, 0, 1, 0, 2]]
is_applicant_complete = True
test_cases.append((applicant_array, is_applicant_complete))

# Test Case 7
applicant_array =  [[1, 2, 0, 0, 0, 0, 0, 0, 0],
                    [0, 2, 0, 1, 3, 0, 0, 0, 0],
                    [3, 0, 2, 1, 3, 0, 0, 0, 0],
                    [1, 0, 2, 3, 4, 0, 0, 0, 0],
                    [0, 2, 0, 0, 1, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 2, 1, 0, 0],
                    [0, 0, 0, 0, 0, 0, 1, 2, 0],
                    [0, 0, 0, 0, 0, 0, 1, 0, 2]]
is_applicant_complete = True
test_cases.append((applicant_array, is_applicant_complete))

# Test Case 8
applicant_array =  [[2, 1, 0, 0],
                    [0, 1, 3, 2],
                    [0, 0, 2, 1],
                    [0, 0, 0, 1]]
is_applicant_complete = True
test_cases.append((applicant_array, is_applicant_complete))

# Test Case 9
applicant_array =  [[1, 4, 0, 2, 0, 3, 5, 0, 0], #a1
                    [0, 0, 4, 0, 1, 2, 0, 5, 0], #a2
                    [2, 0, 0, 3, 1, 0, 0, 4, 0], #a3
                    [1, 0, 0, 4, 3, 0, 0, 2, 5], #a4
                    [2, 4, 0, 0, 1, 5, 3, 0, 0], #a5
                    [0, 0, 0, 0, 0, 2, 1, 0, 0], #a6
                    [0, 4, 0, 2, 0, 0, 1, 3, 0], #a7
                    [3, 0, 6, 2, 4, 0, 1, 0, 5]] #a8
is_applicant_complete = True
test_cases.append((applicant_array, is_applicant_complete))

# Test Case 10
applicant_array =  [[0, 2, 1],
                    [0, 1, 2],
                    [0, 2, 1],
                    [1, 2, 3]]
is_applicant_complete = False
test_cases.append((applicant_array, is_applicant_complete))

def is_applicant_array_valid(applicant_array):
    return True

# We want a function to check is an applicant_array is applicant_complete
def is_applicant_complete_matching_possible(applicant_array):
    matches = []

    # Check that the array is legit
    if not is_applicant_array_valid(applicant_array):
        print("Invalid applicant_array")

    # Magic that reduced the graph to applicants of degree 1 instantly get matched up!
    old_applicant_array = copy.deepcopy(applicant_array)
    (applicant_array, matches) = reduce_applicant_array(applicant_array, matches)
    if(old_applicant_array != applicant_array):
        print("Graph Reduction Produced the following changes:")
        print(old_applicant_array)
        print(applicant_array)
        print(matches)

    # Magic that reduces edges which end at posts with degree 1
    old_applicant_array = copy.deepcopy(applicant_array)
    applicant_array = remove_unused_edges_posts_degree_one(applicant_array, matches)
    if(old_applicant_array != applicant_array):
        print("Unused Edge Reduction Produced the following changes:")
        print(old_applicant_array)
        print(applicant_array)
        print(matches)

    # Finaly check to see if any applicants can't be matched up and also match them
    old_applicant_array = copy.deepcopy(applicant_array)
    (matches, applicant_array) = match_applicants(applicant_array, matches)
    print("Matching applicants Produced the following matches:")
    print(matches)

    return can_all_applicants_match(applicant_array, matches)

def can_all_applicants_match(applicant_array, matches):
    # Check if all applicants are the matches :)
    if len(matches) == 0:
        return False

    matched_applications = []
    for match in matches:
        matched_applications.append(match[0])

    for applicant_index, applicant_preferences in enumerate(applicant_array):
        if applicant_index in matched_applications:
            continue
        else:
            return False

    return True

def match_applicants(applicant_array, matches):
    # Uses the Gale-Shapely algorithm in a sense

    unmatched_applicants = get_unmatched_applicants(applicant_array, matches)
    print("Unmatched applicants:")
    print(unmatched_applicants)
    while len(unmatched_applicants) != 0:
        # m proposes, and becomes engaged, to w;
        for unmatched_applicant_index in unmatched_applicants:
            # print("Attempting to match {}".format(unmatched_applicant_index))
            preferences = get_applicant_posts(applicant_array[unmatched_applicant_index])
            if len(preferences) == 0:
                print("No Applicant Complete Match Possible")
                print("Final Results")
                print(matches)
                print(applicant_array)
                print(get_unmatched_applicants(applicant_array, matches))
                return (() ,[])
            #assign p to be free;
            if is_post_matched(preferences[0], matches):
                other_applicant_matched = get_applicant_matched_with_post(preferences[0], matches)
                if other_applicant_matched < unmatched_applicant_index:
                    if len(get_applicant_posts(applicant_array[other_applicant_matched])) >  len(get_applicant_posts(applicant_array[unmatched_applicant_index])):
                        #print("Removing link between {} {} {}".format(other_applicant_matched, unmatched_applicant_index,  preferences[0]))
                        applicant_array[other_applicant_matched][preferences[0]] = 0
                    else:
                        #print("Removing link between {} {} {}".format(unmatched_applicant_index, other_applicant_matched,  preferences[0]))
                        applicant_array[unmatched_applicant_index][preferences[0]] = 0
                matches = remove_match_post(preferences[0], matches)
            matches = match_applicant_to_post(unmatched_applicant_index, preferences[0], matches)
        unmatched_applicants = get_unmatched_applicants(applicant_array, matches)

    print("Final Results")
    print(matches)
    print(applicant_array)
    print(get_unmatched_applicants(applicant_array, matches))
    return (matches, applicant_array)

def get_applicant_matched_with_post(post_index, matches):
    for match in matches:
        if match[1] == post_index:
            return match[0]

def posts_with_multiple_matches(matches, applicant_array):
    num_posts = len(applicant_array)
    post_match_count = [0] * num_posts
    for match in matches:
        post_match_count[match[1]] = post_match_count[match[1]] + 1

    posts_with_multiple_matches = []
    for index, count in enumerate(post_match_count):
        if count > 1:
            posts_with_multiple_matches.append(index)
    return posts_with_multiple_matches

def remove_match_post(post_index, matches):
    new_matches = copy.deepcopy(matches)
    for match in matches:
        if post_index == match[1]:
            new_matches.remove(match)
    return new_matches

def get_unmatched_applicants(applicant_array, matches):
    unmatched_applicants = []
    for applicant_index, applicant_preferences in enumerate(applicant_array):
        matched = False
        if matches == None:
            unmatched_applicants.append(applicant_index)
            continue
        for match in matches:
            if applicant_index == match[0]:
                matched = True
        if not matched:
            unmatched_applicants.append(applicant_index)

    return unmatched_applicants

def is_post_matched(post_index, matches):
    if matches == None:
        return False
    for match in matches:
        if match[1] == post_index:
            return True
    return False

def match_applicant_to_post(applicant_index, post_index, matches):
    if matches == None:
        matches = []
    if (applicant_index, post_index) not in matches:
        matches.append((applicant_index, post_index))
    return matches

def remove_unused_edges_posts_degree_one(applicant_array, matches):
    reduction_occured = False

    number_posts = len(applicant_array[0])
    # Find posts of degree 1
    for post_index in range(0, number_posts): #Index through all the posts which are unmatched
        # Check if post already matched up
        for match in matches:
            if post_index == match[1]:
                continue
        post_edges = [applicant_preferences[post_index] for applicant_preferences in applicant_array]

        post_input_edge_count = 0
        for post_edge in post_edges:
            if post_edge != 0:
                post_input_edge_count = post_input_edge_count + 1
        if post_input_edge_count == 1:
            # Lets just match up this node for now and remove other edges into the post
            post_applicants = get_post_applicants(applicant_array, post_index)
            applicant_matched = post_applicants[0]
            if (applicant_matched, post_index) not in matches:
                matches.append((applicant_matched, post_index))
            for post_index_loop, post_preference in enumerate(applicant_array[applicant_matched]):
                if post_index == post_index_loop:
                    continue
                if post_preference != 0:
                    applicant_array[applicant_matched][post_index_loop] = 0

    if reduction_occured == True:
        return remove_unused_edges_posts_degree_one(applicant_array, matches)
    else:
        return applicant_array

def is_applicant_degree_one(applicant_preferences):
    post_count = 0
    for post_preference in applicant_preferences:
        if post_preference != 0:
            post_count = post_count + 1

    if post_count != 1:
        return False
    else:
        return True

def get_applicant_posts(applicant_preferences):
    # Get a list of post which an applicant wants in order
    applicant_post_list = []
    preference_number = 1

    for post_number in range(0, len(applicant_preferences)):
        try:
            post_found = applicant_preferences.index(preference_number)
            applicant_post_list.append(post_found)
        except:
            pass
        preference_number = preference_number + 1

    return applicant_post_list

def get_post_applicants(applicant_array, post_number):
    applicants_ordered = []
    for applicant_index, applicant_preferences in enumerate(applicant_array):
        if applicant_preferences[post_number] != 0:
            applicants_ordered.append(applicant_index)

    return applicants_ordered

def reduce_applicant_array(applicant_array, matches):
    reduction_occured = False

    for applicant, applicant_preferences in enumerate(applicant_array):
        if is_applicant_degree_one(applicant_preferences): # This means that an applicant has a single preference! We must match it up!
            posts_matched = get_applicant_posts(applicant_preferences)
            post_matched = posts_matched[0]
            # Only add to matches if not already there
            if (applicant, post_matched) not in matches:
                matches.append((applicant, post_matched))
            # Clear out this post from matching with other applicants
            for other_applicant, other_applicant_preferences in enumerate(applicant_array):
                if other_applicant == applicant:
                    continue
                # This post is not other_applicant's
                if other_applicant_preferences[post_matched] != 0:
                    other_applicant_preferences[post_matched] = 0
                    reduction_occured = True

    if reduction_occured == True:
        return reduce_applicant_array(applicant_array, matches)
    else:
        return (applicant_array, matches)

def main():
    for index, test_case in enumerate(test_cases):
        print("\n\nTest Case {}".format(index))
        test_case_applicant_array = test_case[0]
        test_case_result = test_case[1]
        print(test_case_applicant_array)
        if is_applicant_complete_matching_possible(test_case_applicant_array) != test_case_result:
            print(Fore.RED + "Test case doesn't match result")
            print(Style.RESET_ALL)
        else:
            print(Fore.GREEN + "Test case matches result")
            print(Style.RESET_ALL)

if __name__ == "__main__":
    main()