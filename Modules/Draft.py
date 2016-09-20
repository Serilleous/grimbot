# A module to run us a draft!

import RoboGrimConfig
import RoboGrim
import time
import re
import PIL

VOTE_DURATION = 10
CLEANUP_DURATION = 10

MODE_ORDER = ["!", "@", "#"]

DEFAULT_CARDS_IN_PACK = 12
DEFAULT_PACKS_IN_DRAFT = 4


class Draft:
    communicator = None
    active_phase = None
    start_state = None

    def __init__(self, communicator, arguments):
        print("Draft Initialized.")
        self.communicator = communicator
        if len(arguments) == 0:
            self.start_state = DraftState();
        if len(arguments) == 2:
            self.start_state = DraftState(arguments[0], arguments[1])
            self.start_state.reset_valid_votes()
            print("Starting at pack " + str(arguments[0]) + ", pick " + str(arguments[1]))

    def input(self, username, message):
        self.active_phase.input(username, message)

    def start(self):
        self.active_phase = MainPhase(self.start_state)

    def tick(self):
        should_continue, next_phase = self.active_phase.tick()
        if next_phase is not None:
            self.active_phase = next_phase

        return should_continue


class DraftState:
    votes = [[] * DEFAULT_CARDS_IN_PACK for i in range(DEFAULT_CARDS_IN_PACK)]
    pick = 1
    pack = 1
    mode = MODE_ORDER[0]
    valid_votes = None
    skip_to_count = False

    def __init__(self, pack=None, pick=None):
        self.pack = int(pack) if pack is not None else 1
        self.pick = int(pick) if pick is not None else 1
        self.valid_votes = list(range(0, DEFAULT_CARDS_IN_PACK))

    def reset_votes(self):
        self.votes = [[] * DEFAULT_CARDS_IN_PACK for i in range(DEFAULT_CARDS_IN_PACK)]

    def reset_valid_votes(self):
        self.valid_votes = list(range(0, DEFAULT_CARDS_IN_PACK - self.pick + 1))

    def increment_mode(self):
        if self.mode is None:
            next_mode_index = 0
        else:
            current_mode_index = MODE_ORDER.index(self.mode)
            next_mode_index = (current_mode_index + 1) % len(MODE_ORDER)

        self.mode = MODE_ORDER[next_mode_index]

    def next_card(self):
        self.pick += 1
        if self.pick > DEFAULT_CARDS_IN_PACK:
            self.pick = 1
            self.pack += 1
            print("Opening pack " + str(self.pack))

    def count_votes(self):
        winners = None

        for potential_winner in list(range(0, DEFAULT_CARDS_IN_PACK)):
            if potential_winner not in self.valid_votes:
                continue
            # if card has higher vote than current, clear list and add as winner
            if winners is None or len(self.votes[potential_winner]) > len(self.votes[winners[0]]):
                winners = [potential_winner]

            # if card has equal votes as winner append to list
            elif len(self.votes[potential_winner]) == len(self.votes[winners[0]]):
                winners.append(potential_winner)

        return winners


class MainPhase:
    start_time = None
    draft_state = None

    def __init__(self, draft_state: DraftState=None):
        self.start_time = time.time()
        self.draft_state = draft_state if draft_state is not None else DraftState()
        print("Starting main voting phase.  Mode: " + self.draft_state.mode)

    def tick(self):
        if (time.time() - self.start_time) > VOTE_DURATION or self.draft_state.skip_to_count:
            print("Main vote phase ending.")
            return True, CleanupPhase(self.draft_state)
        return True, None

    def input(self, user, message):
        symbol, vote = parse_vote(user, message, self.draft_state)
        tally_vote(user, symbol, vote, self.draft_state)


class CleanupPhase:
    start_time = None
    draft_state = None

    def __init__(self, draft_state: DraftState):
        print("Starting vote cleanup phase.")
        self.start_time = time.time()
        self.draft_state = draft_state

    def tick(self):
        if (time.time() - self.start_time) > CLEANUP_DURATION or self.draft_state.skip_to_count:
            print("Cleanup phase ending, counting votes.")
            self.draft_state.skip_to_count = False
            result = self.draft_state.count_votes()
            if len(result) > 1:
                # if there's a tie, do a runoff
                print("Vote tied: " + str(result))
                self.draft_state.valid_votes = result
            else:
                # if there's one winner, pick a card
                print("Winner:" + str(result[0]))
                pick_card(result[0])
                self.draft_state.next_card()
                if self.draft_state.pack > DEFAULT_PACKS_IN_DRAFT:
                    #end the draft
                    return False, None

                self.draft_state.reset_valid_votes()

            self.draft_state.increment_mode()
            self.draft_state.reset_votes()

            return True, MainPhase(self.draft_state)
        return True, None

    def input(self, user, message):
        symbol, vote = parse_vote(user, message, self.draft_state)
        tally_vote(user, symbol, vote, self.draft_state)


def parse_vote(user, vote, draft_state: DraftState):
    # get vote symbol
    vote_symbol = vote[:1]
    if vote_symbol not in draft_state.mode and not (user == RoboGrimConfig.ME and vote_symbol is '~'):
        vote_symbol = None

    # get vote number
    vote_value = None
    try:
        vote_value = int(vote[1 - len(vote):]) - 1
    except ValueError:
        pass

    # validate vote
    if vote_value not in draft_state.valid_votes:
        vote_value = None

    return vote_symbol, vote_value


def tally_vote(user, symbol, vote, draft_state: DraftState):
    if symbol is None or vote is None:
        return

    # if symbol is ~, clear all votes but the kings, and skip to the counting phase
    if symbol in "~":
        draft_state.reset_votes()
        draft_state.votes[vote].append(user)
        draft_state.skip_to_count = True
    elif symbol == draft_state.mode and not any(user in sublist for sublist in draft_state.votes):
        draft_state.votes[vote].append(user)


def pick_card(index):
    pass


class OverlayWriter:
    def __init__(self):
        pass

    def tick(self):
        pass

    def set_valid_votes(self):
        pass

    def set_phase_message(self):
        pass

    def set_timer(self):
        pass