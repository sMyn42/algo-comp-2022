import numpy as np
from typing import List, Tuple

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

    print(scores)

    # Change the compatibility scores based on gender preferences.
    for i in range(scores.shape[0]):
        for j in range(scores.shape[1]):
            if gender_pref[i] == "Men":
                if "Male" != gender_id[j]:
                    scores[i][j] = 0
            elif gender_pref[i] == "Women":
                if "Female" != gender_id[j]:
                    scores[i][j] = 0

    #Partition Array
    group_index = scores.shape[0]//2

    proposers = np.arange(0, group_index)
    proposer_preferences = np.ndarray((group_index, group_index)) #The first half
    for j in range(0, group_index): 
        proposer_preferences[j] = np.argsort(scores[j][group_index:]) + np.repeat(group_index, group_index)

    receivers = np.arange(group_index, scores.shape[0])
    receiver_preferences = np.ndarray((group_index, group_index)) #The second half
    for i in range(group_index, scores.shape[0]):
        receiver_preferences[i - group_index] = np.argsort(scores[i][:group_index])

    print(scores)

    print("Proposer Preferences")
    print(proposer_preferences)

    print("Receiver Preferences")
    print(receiver_preferences)

    # Carry out matching algorithm:

    # GALE-SHAPLEY ALGORITHM
    # ----------

    # Everyone starts free

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

    matches = []

    free_proposers = {i: True for i in range(group_index)} #keeps track of free proposers
    free_receivers = [i for i in range(group_index, scores.shape[0])] #keeps track of free receivers
    receiver_matches = {i: None for i in range(group_index, scores.shape[0])}
    to_propose = [list(proposer_preferences[i]) for i in range(proposer_preferences.shape[0])]

    print(free_proposers)

    print("Proposal Order")
    print(np.array(to_propose))

    while (sum(free_proposers.values()) >= 1):
        for (k, v) in free_proposers.items():
            if v:
                p = k
        # pick the first unproposed r:
        r = to_propose[k].pop(0)
        print(p, "  proposing to  ", r)
        print(np.array(to_propose))

        # if statment
        if r in free_receivers:
            receiver_matches[r] = p
            free_proposers[p] = False
            free_receivers.pop(free_receivers.index(r))

        # if this p is better
        elif list(receiver_preferences[r - group_index]).index(p) > list(receiver_preferences[r - group_index]).index(receiver_matches[r]):
            free_proposers[receiver_matches[r]] = True
            receiver_matches[r] = p

        # reject p if neither
        else:
            free_proposers[p] = False

    for (k, v) in receiver_matches.items():
        matches.append((int(v), int(k)))


    print("-------------------------\n\n\nMATCHES:")
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

    
