from typing import List, Tuple
import numpy as np

def run_matching(scores: List[List], gender_id: List, gender_pref: List) -> List[Tuple]:
    """
    TODO: Implement Gale-Shapley stable matching!
    :param scores: raw N x N matrix of compatibility scores. Use this to derive a preference rankings.
    :param gender_id: list of N gender identities (Male, Female, Non-binary) corresponding to each user
    :param gender_pref: list of N gender preferences (Men, Women, Bisexual) corresponding to each user
    :return: `matches`, a List of (Proposer, Acceptor) Tuples representing monogamous matches
    
    Some Guiding Questions/Hints:
        - This is not the standard Men proposing & Women receiving scheme Gale-Shapley is introduced as
        - Instead, to account for various gender identity/preference combinations, it would be better to choose a random half of users to act as "Men" (proposers) and the other half as "Women" (receivers)
            - From there, you can construct your two preferences lists (as seen in the canonical Gale-Shapley algorithm; one for each half of users
        - Before doing so, it is worth addressing incompatible gender identity/preference combinations (e.g. gay men should not be matched with straight men).
            - One easy way of doing this is setting the scores of such combinations to be 0
            - Think carefully of all the various (Proposer-Preference:Receiver-Gender) combinations and whether they make sense as a match
        - How will you keep track of the Proposers who get "freed" up from matches?
        - We know that Receivers never become unmatched in the algorithm.
            - What data structure can you use to take advantage of this fact when forming your matches?
        - This is by no means an exhaustive list, feel free to reach out to us for more help!
    """

    # may result in suboptimal pairings, which are then igrnoed; people may be unpaired.

    # Ease of Debugging
    np.set_printoptions(precision=2)

    # Allow numpy functions to be used
    scores = np.array(scores)

    # print(scores)

    # Since the genders don't line up well, I'll be implementing friend matching

    # # Change the compatibility scores based on gender preferences.
    # for i in range(scores.shape[0]):
    #     for j in range(scores.shape[1]):
    #         if gender_pref[i] == "Men":
    #             if "Male" != gender_id[j]:
    #                 scores[i][j] = 0
    #         elif gender_pref[i] == "Women":
    #             if "Female" != gender_id[j]:
    #                 scores[i][j] = 0

    #Partition Array
    group_index = scores.shape[0]//2

    proposers = np.arange(0, group_index, dtype=int)
    proposer_preferences = np.ndarray((group_index, group_index), dtype=int) #The first half
    for j in range(0, group_index): 
        proposer_preferences[j] = np.repeat(group_index, group_index) - np.argsort(scores[j][group_index:]) + np.repeat(group_index, group_index)

    receivers = np.arange(group_index, scores.shape[0], dtype=int)
    receiver_preferences = np.ndarray((group_index, group_index), dtype=int) #The second half
    for i in range(group_index, scores.shape[0]):
        receiver_preferences[i - group_index] = np.repeat(group_index, group_index) - np.argsort(scores[i][:group_index])

    print(scores)

    print("\nProposer Preferences")
    print(proposer_preferences)

    print("\nReceiver Preferences")
    print(receiver_preferences)
    print("\n\n")

    # Carry out matching algorithm:

    # GALE-SHAPLEY ALGORITHM
    # ----------

    # Everyone starts free

    matches = []

    free_proposers = [1, 2, 3, 4, 5]
    receivers = [6, 7, 8, 9, 10]
    proposal_list = [list(proposer_preferences[i]) for i in range(proposer_preferences.shape[1])]
    receiver_matches = {i: None for i in receivers}

    print(proposal_list)
    print("\n\n\n\n")

    # while proposer is free:
    
    #     Choose a proposer p
    #     r is the first receiver r on m’s list to whom m has not yet proposed
    #     if r is free then
    #         Match p + r
    #     else if r prefers p to her current match p_prev
    #         then
    #         Match p and r, and free up p_prev
    #     else
    #          rejects p
    # END

    while (len(free_proposers) != 0):

        print(proposal_list)

        p = free_proposers.pop(0)
        r = proposal_list[p - 1].pop(0)

        
        print(p, "  proposing to  ", r)
        
        
        if receiver_matches.get(r) is None:
            receiver_matches[r] = p
            print(r, " matched with ", p)

        # If index of current match is greater than that of the proposed match: (TODO)
        elif np.where(receiver_preferences[r - group_index - 1] == receiver_matches.get(r)) > np.where(receiver_preferences[r - group_index - 1] == p):
            free_proposers.insert(0, receiver_matches[r])
            receiver_matches[r] = p
            print(r, " was taken from ", free_proposers[0], " by ", p)

        else:
            free_proposers.insert(0, p)

        print(free_proposers)
        print()

    # Update + Show Answers

    for (r, p) in receiver_matches.items():
        matches.append((p, r))

    print("-------------------------\n\n\nMATCHES:\n\n")
    print(matches)
    print("\n\n\n--------------------------")

    return matches

if __name__ == "__main__":
    raw_scores = np.loadtxt('raw_scores.txt').tolist()
    genders = []
    with open('genders.txt', 'r') as file:
        for line in file:
            curr = line[:-1]
            genders.append(curr)

    gender_preferences = []
    with open('gender_preferences.txt', 'r') as file:
        for line in file:
            curr = line[:-1]
            gender_preferences.append(curr)

    gs_matches = run_matching(raw_scores, genders, gender_preferences)