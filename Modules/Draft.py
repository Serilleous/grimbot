# A module to run us a draft!

import RoboGrimConfig
import RoboGrim
import time
import re
import PIL
import sys
import pyautogui

import Overlay

from configparser import ConfigParser
from tkinter import *
from PIL import Image, ImageDraw

CONFIG_SECTION = "Draft"

VOTE_DURATION = None
CLEANUP_DURATION = None

MODE_ORDER = ["!", "@", "#"]

DEFAULT_CARDS_IN_PACK = 12
DEFAULT_PACKS_IN_DRAFT = 4
DEFAULT_VOTE_SHAPE = ["1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1"]


class Draft:
    communicator = None
    active_phase = None
    start_state = None
    overlays = []

    def __init__(self, communicator, arguments):
        print("Draft Initialized.")
        self.communicator = communicator
        if len(arguments) == 0:
            self.start_state = DraftState();
        if len(arguments) == 2:
            self.start_state = DraftState(arguments[0], arguments[1])
            self.start_state.reset_valid_votes()
            print("Starting at pack " + str(arguments[0]) + ", pick " + str(arguments[1]))

        # update globals from config
        config = ConfigParser()
        config.read(RoboGrimConfig.CONFIG)
        global VOTE_DURATION
        VOTE_DURATION = float(config.get(CONFIG_SECTION, "MainPhaseTime")) + 0.99
        global CLEANUP_DURATION
        CLEANUP_DURATION = float(config.get(CONFIG_SECTION, "CleanupPhaseTime")) + 0.99

    def input(self, username, message):
        self.active_phase.input(username, message)

    def start(self):
        self.active_phase = MainPhase(self.start_state)

    def tick(self):

        # tick the phase and move to the next on if appropriate
        should_continue, next_phase = self.active_phase.tick()
        if next_phase is not None:
            self.active_phase = next_phase

        # tick the overlay elements
        for element in self.start_state.overlay_elements:
            element.tick()

        return should_continue


class DraftState:
    votes = [[] * DEFAULT_CARDS_IN_PACK for i in range(DEFAULT_CARDS_IN_PACK)]
    pick = 1
    pack = 1
    mode = MODE_ORDER[-1]
    valid_votes = None
    skip_to_count = False

    #UI elements
    overlay_elements = []
    timer = None
    timer_label = None

    def __init__(self, pack=None, pick=None):
        self.pack = int(pack) if pack is not None else 1
        self.pick = int(pick) if pick is not None else 1
        self.valid_votes = list(range(0, DEFAULT_CARDS_IN_PACK))

        self.timer = Overlay.CountdownTimer()
        self.overlay_elements.append(self.timer)

        self.timer_label = Overlay.Label("Vote!")
        self.overlay_elements.append(self.timer_label)

        self.vote_numbers = Overlay.TextGrid("Draft Numbers")
        self.vote_numbers.set_text(["1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1"])
        self.overlay_elements.append(self.vote_numbers)

        self.vote_count = Overlay.TextGrid("Vote Count")
        self.vote_count.set_text(["0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0"])
        self.overlay_elements.append(self.vote_count)

    def reset_votes(self):
        self.votes = [[] * DEFAULT_CARDS_IN_PACK for i in range(DEFAULT_CARDS_IN_PACK)]

        self.vote_count.set_text(["0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0"])

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
        draft_state = draft_state if draft_state is not None else DraftState()

        if draft_state.pack > DEFAULT_PACKS_IN_DRAFT:
            #end the draft
            return False, None

        self.start_time = time.time()

        draft_state.timer.set_timer(VOTE_DURATION)
        draft_state.timer_label.set_text("Vote!", 300)
        draft_state.increment_mode()
        draft_state.reset_votes()
        self.draft_state = draft_state


        new_vote_numbers = ["" for x in range(len(DEFAULT_VOTE_SHAPE))]

        for i in range(0, len(draft_state.valid_votes)):
            new_vote_numbers[draft_state.valid_votes[i]] = draft_state.mode + str(draft_state.valid_votes[i] + 1)

        draft_state.vote_numbers.set_text(new_vote_numbers)

        print("Starting main voting phase.  Mode: " + draft_state.mode)

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
        self.draft_state.timer.set_timer(CLEANUP_DURATION)
        self.draft_state.timer_label.set_text("Counting\n  Votes...", 150)

    def tick(self):
        if (time.time() - self.start_time) > CLEANUP_DURATION or self.draft_state.skip_to_count:
            print("Cleanup phase ending, counting votes.")
            self.draft_state.skip_to_count = False
            result = self.draft_state.count_votes()

            # if there's a winner, pick a card
            if len(result) == 1:
                print("Winner:" + str(result[0]))
                return True, PickPhase(result[0], self.draft_state)

            # otherwise, do a runoff
            print("Vote tied: " + str(result))
            self.draft_state.valid_votes = result

            return True, MainPhase(self.draft_state)

        return True, None

    def input(self, user, message):
        symbol, vote = parse_vote(user, message, self.draft_state)
        tally_vote(user, symbol, vote, self.draft_state)


class PickPhase:

    mouse_click_delay = 1
    start_time = None
    mouse_moved = False

    def __init__(self, winner, draft_state):
        self.start_time = time.time()
        self.winner = winner
        self.draft_state = draft_state

        config = ConfigParser()
        config.read("GrimBot.ini")
        grid_width = config.getint("Draft", "GridWidth")
        grid_height = config.getint("Draft", "GridHeight")
        column_offset = round(grid_width * config.getfloat("Draft", "ColumnOffset"))
        row_offset = round(grid_height * config.getfloat("Draft", "RowOffset"))
        column_spacing = round(grid_width * config.getfloat("Draft", "ColumnSpacing"))
        row_spacing = round(grid_height * config.getfloat("Draft", "RowSpacing"))
        x_position = column_offset + column_spacing * (winner % 4)
        y_position = row_offset + row_spacing * int(winner / 4)

        self.winner_position = (x_position, y_position)

    def tick(self):
        x, y = self.winner_position

        if not self.mouse_moved:
            pyautogui.moveTo(x, y)
            self.mouse_moved = True

        if time.time() - self.start_time > self.mouse_click_delay:
            try:
                pyautogui.click(x, y)
            except Exception as exception:
                # swallow that error that always happens for some reason :(
                pass
            self.draft_state.next_card()
            self.draft_state.reset_valid_votes()
            return True, MainPhase(self.draft_state)

        return True, None


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

    new_vote_text = []
    for vote in draft_state.votes:
        new_vote_text.append(str(len(vote)))

    draft_state.vote_count.set_text(new_vote_text)