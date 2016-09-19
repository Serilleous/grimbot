# A module to run us a draft!

import RoboGrimConfig
import RoboGrim
import time
import re


class Draft:
    communicator = None
    start_time = None

    vote_duration = RoboGrimConfig.DRAFT_PICK_DURATION
    vote_cleanup_duration = RoboGrimConfig.DRAFT_STREAM_DELAY
    vote_start_time = None

    mode_order = ["!", "@", "#"]
    mode = None

    pick_number = 0
    pack_number = 1
    cards_in_pack = 12
    packs_in_draft = 4

    valid_vote_values = list(range(0, cards_in_pack))
    votes = {
        "!": [[]*12 for i in range(12)],
        "@": [[]*12 for i in range(12)],
        "#": [[]*12 for i in range(12)]
    }

    START = 'start'
    CLEANUP = 'cleanup'
    VOTE = 'vote'
    DONE = 'done'
    timer_phase = START

    def __init__(self, communicator, arguments):
        print("Draft Initialized.")
        self.communicator = communicator
        #parse arguments incase we want to start a draft midway

    def input(self, username, message):
        self.tally_vote(username, message)

    def start(self):
        self.start_time = time.time()
        print("Draft started")
        self.communicator.chat("Draft Started!")
        self.increment_vote_mode()

    def tick(self):

        if (time.time() - self.vote_start_time) > self.vote_duration + self.vote_cleanup_duration\
                or self.vote_start_time == 0:
            if self.timer_phase is not self.CLEANUP:
                print("Cleanup time is over, picking a card")
                self.timer_phase = self.CLEANUP

            results = self.count_votes()
            if len(results) == 1: # there's a winner, pick the card and start next thing
                self.pick_card(results[0])

                # reset for next vote
                self.cards_in_pack -= 1
                if self.cards_in_pack == 0:
                    self.pack_number += 1
                    self.cards_in_pack = 12
                    # stop the draft if we're done
                    if self.pack_number > self.packs_in_draft:
                        print('Draft complete')
                        return False
                self.valid_vote_values = list(range(0, self.cards_in_pack))

            else: # there's a tie, do a runoff
                print("A tie between " + str(results))
                self.valid_vote_values = results
                pass

            self.increment_vote_mode()
            return True

        if (time.time() - self.vote_start_time) > self.vote_duration:
            if self.timer_phase is not self.VOTE:
                print("Pick time is up.")
                self.timer_phase = self.VOTE

            return True
        return True

    def increment_vote_mode(self):
        if self.mode is None:
            next_mode_index = 0
        else:
            current_mode_index = self.mode_order.index(self.mode)
            next_mode_index = (current_mode_index + 1) % len(self.mode_order)

        self.mode = self.mode_order[next_mode_index]
        self.votes[self.mode] = [[]*12 for i in range(12)] # reset the vote count for this mode
        self.vote_start_time = time.time()

        print("Starting " + self.mode + " draft mode")

    # adds vote to the vote list
    def tally_vote(self, name, vote):

        # get vote symbol
        vote_symbol = vote[:1]
        if vote_symbol not in self.mode and not (name == RoboGrimConfig.ME and vote_symbol is '~'):
            return

        # get vote number
        vote_value = None
        try:
            vote_value = int(vote[1 - len(vote):]) - 1
        except ValueError:
            return

        # validate vote
        if vote_value not in self.valid_vote_values:
            return

        # end the vote if the king demands
        if vote_symbol is '~':
            # clear everyone elses votes
            self.votes[self.mode] = [[]*12 for i in range(12)]
            self.vote_start_time = 0

        # add that vote
        if name not in self.votes[self.mode][vote_value]:
            self.votes[self.mode][vote_value].append(name)

    # count the votes and turn an array with the highest indices
    def count_votes(self):
        this_rounds_votes = self.votes[self.mode]
        winners = None
        for potential_winner in self.valid_vote_values:

            # if card has higher vote than current, clear list and add as winner
            if winners is None or len(this_rounds_votes[potential_winner]) > len(this_rounds_votes[winners[0]]):
                winners = [potential_winner]

            # if card has equal votes as winner append to list
            elif len(this_rounds_votes[potential_winner]) == len(this_rounds_votes[winners[0]]):
                winners.append(potential_winner)

        return winners

    def pick_card(self, pick_index):

        pass
