# Category: Arrays and Hashing

# --- Valid Anagram ---
# Difficulty: Easy
# @problem
# Given two strings s and t, return true if the two strings are
# anagrams of each other, otherwise return false.
#
# Two strings are anagrams if they contain the same characters, with
# each character appearing the same number of times, regardless of
# order.
# @hint
# You don't need to sort anything. Try counting how many times each
# character appears using an auxiliary dictionary (a hash map), then
# compare the counts between the two strings.
# @solution

def is_anagram(s, t):
    if len(s) != len(t):
        return False

    counts = {}
    for char in s:
        counts[char] = counts.get(char, 0) + 1
    for char in t:
        counts[char] = counts.get(char, 0) - 1

    for count in counts.values():
        if count != 0:
            return False
    return True

# @explanation
# First, if the two strings have different lengths they can't be
# anagrams, so we return False right away.
#
# Otherwise, we build a single dict that counts how many times each
# character appears. We add 1 for every character we see in s, and
# subtract 1 for every character we see in t, using dict.get(char, 0)
# so a character we haven't seen yet defaults to 0 instead of raising
# a KeyError.
#
# If s and t are true anagrams, every character's count cancels out
# back to 0. If any count is left over (positive or negative), the
# strings used different characters or different amounts of them, so
# we return False.

# --- Valid Sudoku ---
# Difficulty: Medium
# @problem
# You are given a 9 x 9 Sudoku board board. A Sudoku board is valid if
# the following rules are followed:
#
# Each row must contain the digits 1-9 without duplicates.
# Each column must contain the digits 1-9 without duplicates.
# Each of the nine 3 x 3 sub-boxes of the grid must contain the digits
# 1-9 without duplicates.
#
# Return true if the Sudoku board is valid, otherwise return false.
#
# Note: A board does not need to be full or be solvable to be valid.
# @hint
# Try keeping a set for each row, each column, and each 3x3 box (nine
# of each). As you scan the board once, cell by cell, you just need a
# way to figure out which box a given (row, col) belongs to.
# @solution

def is_valid_sudoku(board):
    rows = [set() for _ in range(9)]
    cols = [set() for _ in range(9)]
    boxes = [set() for _ in range(9)]

    for r in range(9):
        for c in range(9):
            value = board[r][c]
            if value == ".":
                continue

            box_index = (r // 3) * 3 + c // 3

            if value in rows[r] or value in cols[c] or value in boxes[box_index]:
                return False

            rows[r].add(value)
            cols[c].add(value)
            boxes[box_index].add(value)

    return True

# @explanation
# We keep one set per row, one per column, and one per 3x3 box, all
# indexed 0-8. As we scan every cell on the board, "." means empty, so
# we skip it and move on.
#
# For a filled cell, we first figure out which box it belongs to with
# (r // 3) * 3 + c // 3 — this maps the 9x9 grid's 3x3 blocks to box
# indexes 0 through 8, reading left to right, top to bottom.
#
# Before adding the value, we check whether it's already in that row's
# set, that column's set, or that box's set. If it is, we've found a
# duplicate and the board is invalid, so we return False immediately.
# Otherwise we add the value to all three sets and keep going. If we
# get through every cell with no duplicates, the board is valid.

# --- Two Sum ---
# Difficulty: Easy
# @problem
# Given an array of integers nums and an integer target, return the
# indices i and j such that nums[i] + nums[j] == target and i != j.
#
# You may assume that every input has exactly one pair of indices i
# and j that satisfy the condition.
#
# Return the answer with the smaller index first.
# @hint
# Try using a hash map: as you scan the array, check whether the
# complement (target minus the current number) has already been seen
# before you add the current number to the map.
# @solution:Junior

def two_sum(nums, target):
    # Maps a number we've already scanned to the index where it was
    # found, so we can look it back up in O(1) instead of scanning
    # again.
    seen = {}

    for i in range(len(nums)):
        current_number = nums[i]
        # This is the value we'd need from an earlier position to
        # hit the target together with current_number.
        complement = target - current_number

        if complement in seen:
            # complement was added on an earlier loop, so its index
            # is always smaller than i — this already returns the
            # smaller index first.
            j = seen[complement]
            return [j, i]

        # No match yet, so remember this number for a later lookup.
        seen[current_number] = i

    return []

# @solution:Senior

def two_sum(nums, target):
    seen = {}  # number -> index, filled in as we scan

    for i, n in enumerate(nums):
        # Walrus operator: look up the complement and bind it to j
        # in the same expression, then check it was actually found.
        if (j := seen.get(target - n)) is not None:
            return [j, i]  # j was inserted earlier, so it's the smaller index
        seen[n] = i

    return []

# @explanation
# Both versions use the same O(n) one-pass hash map approach: walk
# the array once, and before adding the current number to the map,
# check whether its complement (target minus the current number) is
# already in there.
#
# Since the complement can only be in the map if it was added on an
# earlier iteration, the index we find for it (j) is always smaller
# than the current index (i), so returning [j, i] already satisfies
# "smaller index first" for free, with no extra comparison needed.
#
# The Junior version spells out each step with explicit variable
# names and an if-shaped check. The Senior version reaches for
# enumerate() instead of manual indexing, and the walrus operator
# (:=) to look up and bind the complement in the same expression —
# same algorithm, same time and space complexity, fewer lines.
