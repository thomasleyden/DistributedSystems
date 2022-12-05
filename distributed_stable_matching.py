test_cases = []
# Test Case 1
applicant_array =  [[1, 2, 3],
                    [3, 1, 2],
                    [2, 3, 1]]

is_applicant_complete = True
test_cases.append((applicant_array, is_applicant_complete))

# Test Case 1
applicant_array =  [[3, 1, 3],
                    [1, 3, 2],
                    [1, 2, 3]]

is_applicant_complete = True
test_cases.append((applicant_array, is_applicant_complete))

# Test Case 1
applicant_array =  [[1, 2, 3],
                    [3, 1, 2],
                    [3, 1, 2]]

is_applicant_complete = True
test_cases.append((applicant_array, is_applicant_complete))

import logging, multiprocessing
from multiprocessing.pool import ThreadPool as Pool
import time

def myproc(arg):
    return arg*2

def applicant_function(post_msg_queue, preferences, applicant_index, listen_queue, end_queue):
    #Propose to top choice and wait for response
    matched = False
    choice = 0
    top_choice = preferences.index(choice)
    post_msg_queue[top_choice].put("{}.Proposal".format(applicant_index))
    print("Applicant {} proposed to {}".format(applicant_index, choice))
    choice = choice + 1
    algorithm_ended = False
    while not algorithm_ended:
        #Wait for reponse :)
        response = listen_queue.get()
        if matched:
            print("Applicant {} awake again {}".format(applicant_index, response))
        response_tokens = response.split('.')
        if response == "end":
            algorithm_ended = True
            continue
        #print(response)
        if response_tokens[0] == "Accepted":
            matched = True
            print("Applicant {} got accepted by".format(applicant_index, response_tokens[1]))
            end_queue.put("Applicant.{}.{}".format(applicant_index, response_tokens[1]))
        else: #Rejected :()
            if matched:
                matched = False
                #print("{} got unmatched from {} :(".format(applicant_index, response))
            # Propose to next woman in list
            print("Applicant {} got rejected by".format(applicant_index, response_tokens[1]))
            top_choice = preferences.index(choice)
            post_msg_queue[top_choice].put("{}.Proposal".format(applicant_index))
            choice = choice + 1

        #print("Waiting Applicant {}".format(applicant_index))
        #time.sleep(1)

def post_function(post_msg_queue, post_index, applicant_queues, end_queue):
    matched = False
    matched_with = 0

    algorithm_ended = False
    while not algorithm_ended:

        #Wait for proposals and handle them
        proposal = post_msg_queue.get()
        proposal_split = proposal.split(".")
        if proposal == "end":
            algorithm_ended = True
            continue
        #print("Post:{} Got message {}".format(post_index, proposal))
        if not matched: #Accept the match
            matched = True
            matched_with = int(proposal_split[0])
            end_queue.put("Post.{}.{}".format(matched_with, post_index))
            print("Post {} Got matched with {}").format(post_index, matched_with)
            applicant_queues[matched_with].put("Accepted.{}".format(post_index))
            #print("First match {}{}".format(post_index, matched_with))
        else: #If better match accept it and then reject other one
            if matched_with < int(proposal_split[0]): #Reject who just asked
                applicant_queues[int(proposal_split[0])].put("Rejected.{}".format(post_index))
                print("Post {} Rejected {}".format(post_index, proposal_split[0]))
            else: #Accept who just asked and reject previous guy
                applicant_queues[matched_with].put("Rejected.{}".format(post_index))
                print("Post {} Got matched with {} rejected {}").format(post_index, int(proposal_split[0]), matched_with)
                applicant_queues[matched_with].put("Accepted.{}".format(post_index))
                matched_with = int(proposal_split[0])
                end_queue.put("Post.{}.{}".format(matched_with, post_index))
        #print("Waiting Post {}".format(post_index))
        #time.sleep(1)

import random

def main():
    numApplicants = 75
    applicant_preferences = [range(0,numApplicants)] * numApplicants

    for applicant_stuff in applicant_preferences:
        random.shuffle(applicant_stuff)
    print(applicant_preferences)
    end_queue = multiprocessing.Queue()
    post_queue_list = [ multiprocessing.Queue() for i in range(0, numApplicants) ]
    applicant_queue_list = [ multiprocessing.Queue() for i in range(0, numApplicants) ]
    applicant_queue_list = [ multiprocessing.Queue() for i in range(0, numApplicants) ]
    applicant_threads = []
    post_threads = []

    for applicant_index in range(0, numApplicants):
        applicant_thread = multiprocessing.Process(
            target=applicant_function, args=(post_queue_list, applicant_preferences[applicant_index], applicant_index, applicant_queue_list[applicant_index], end_queue),
            name='applicant{}'.format(applicant_index),
        )
        applicant_threads.append(applicant_thread)

    for post_index in range(0, numApplicants):
        post_thread = multiprocessing.Process(
            target=post_function, args=(post_queue_list[post_index], post_index, applicant_queue_list, end_queue),
            name='post{}'.format(post_index),
        )
        post_threads.append(post_thread)

    for post in post_threads:
        post.start()

    for applicant in applicant_threads:
        applicant.start()

    finished = False
    matches = [-1] * numApplicants
    while not finished:
        response = end_queue.get()
        response_things = response.split('.')
        #print(response_things)
        #print(len(response_things))
        response_things[1] = int(response_things[1])    #Applicant
        response_things[2] = int(response_things[2])    #Post
        matches[response_things[1]] = response_things[2]
        if -1 not in matches:
            finished = True
        print(matches)

    for queue in applicant_queue_list:
        queue.put("end")
    for queue in post_queue_list:
        queue.put("end")

    for post in post_threads:
        post.join()

    for applicant in applicant_threads:
        applicant.join()

    print("Preferences")
    print(applicant_preferences)
    print("Matches are:")
    print(matches)


if __name__ == "__main__":
    main()
