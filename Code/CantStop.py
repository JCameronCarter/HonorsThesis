import random 
from typing import List, Tuple, Set, Optional
from collections import defaultdict
import time

class CantStopBoard:
    #Represents the Can't Stop game board
    
    # Number of spaces needed to complete each column
    Column_Heights = {
        2: 3, 3: 5, 4: 7, 5: 9, 6: 11,
        7: 13, 8: 11, 9: 9, 10: 7, 11: 5, 12: 3
    }
    # Probablity of being able to move at least one coloumn given all 3 markers are placed
    # All possible 3 pairs are listed
    ## Probabilities follow geometric dist. such that # of rolls before the chance we don't bust less than the chance we do bust is 1/p-1 - 1/p, 
    # Expected value of roll #'s to first bust minus expected value of of roll #'s to first not bust.
    Prob_Table = { (2, 3, 4): 0.52, (2, 3, 5): 0.58, (2, 3, 6): 0.68, (2, 3, 7): 0.75, (2, 3, 8): 0.76, (2, 3, 9): 0.71,
        (2, 3, 10): 0.63, (2, 3, 11): 0.53, (2, 3, 12): 0.44, (2, 4, 5): 0.66, (2, 4, 6): 0.76, (2, 4, 7): 0.81,
        (2, 4, 8): 0.82, (2, 4, 9): 0.76, (2, 4, 10): 0.74, (2, 4, 11): 0.63, (2, 4, 12): 0.55, (2, 5, 6): 0.77, 
        (2, 5, 7): 0.81, (2, 5, 8): 0.83, (2, 5, 9): 0.76, (2, 5, 10): 0.76, (2, 5, 11): 0.71, (2, 5, 12): 0.63,
        (2, 6, 7): 0.86, (2, 6, 8): 0.88, (2, 6, 9): 0.83, (2, 6, 10): 0.81, (2, 6, 11): 0.76, (2, 6, 12): 0.74,
        (2, 7, 8): 0.89, (2, 7, 9): 0.84, (2, 7, 10): 0.83, (2, 7, 11): 0.78, (2, 7, 12): 0.78, (2, 8, 9): 0.82, 
        (2, 8, 10): 0.82, (2, 8, 11): 0.74, (2, 8, 12): 0.74, (2, 9, 10): 0.71, (2, 9, 11): 0.64, (2, 9, 12): 0.63,
        (2, 10, 11): 0.58, (2, 10, 12): 0.55, (2, 11, 12): 0.44, (3, 4, 5): 0.67, (3, 4, 6): 0.74, (3, 4, 7): 0.79,
        (3, 4, 8): 0.80, (3, 4, 9): 0.78, (3, 4, 10): 0.76, (3, 4, 11): 0.66, (3, 4, 12): 0.58, (3, 5, 6): 0.77, 
        (3, 5, 7): 0.79, (3, 5, 8): 0.81, (3, 5, 9): 0.78, (3, 5, 10): 0.76, (3, 5, 11): 0.71, (3, 5, 12): 0.64,
        (3, 6, 7): 0.86, (3, 6, 8): 0.85, (3, 6, 9): 0.83, (3, 6, 10): 0.82, (3, 6, 11): 0.76, (3, 6, 12): 0.74,
        (3, 7, 8): 0.89, (3, 7, 9): 0.84, (3, 7, 10): 0.84, (3, 7, 11): 0.78, (3, 7, 12): 0.78, (3, 8, 9): 0.84, 
        (3, 8, 10): 0.83, (3, 8, 11): 0.76, (3, 8, 12): 0.76, (3, 9, 10): 0.78, (3, 9, 11): 0.71, (3, 9, 12): 0.71,
        (3, 10, 11): 0.66, (3, 10, 12): 0.63, (3, 11, 12): 0.53, (4, 5, 6): 0.80, (4, 5, 7): 0.85, (4, 5, 8): 0.85,
        (4, 5, 9): 0.80, (4, 5, 10): 0.82, (4, 5, 11): 0.78, (4, 5, 12): 0.71, (4, 6, 7): 0.89, (4, 6, 8): 0.91, 
        (4, 6, 9): 0.86, (4, 6, 10): 0.88, (4, 6, 11): 0.83, (4, 6, 12): 0.82, (4, 7, 8): 0.90, (4, 7, 9): 0.89, 
        (4, 7, 10): 0.88, (4, 7, 11): 0.84, (4, 7, 12): 0.83, (4, 8, 9): 0.86, (4, 8, 10): 0.88, (4, 8, 11): 0.82,
        (4, 8, 12): 0.81, (4, 9, 10): 0.82, (4, 9, 11): 0.76, (4, 9, 12): 0.76, (4, 10, 11): 0.76, (4, 10, 12): 0.74,
        (4, 11, 12): 0.63, (5, 6, 7): 0.89, (5, 6, 8): 0.90, (5, 6, 9): 0.87, (5, 6, 10): 0.86, (5, 6, 11): 0.84, 
        (5, 6, 12): 0.82, (5, 7, 8): 0.91, (5, 7, 9): 0.85, (5, 7, 10): 0.89, (5, 7, 11): 0.84, (5, 7, 12): 0.84,
        (5, 8, 9): 0.87, (5, 8, 10): 0.86, (5, 8, 11): 0.83, (5, 8, 12): 0.83, (5, 9, 10): 0.80, (5, 9, 11): 0.78, 
        (5, 9, 12): 0.76, (5, 10, 11): 0.78, (5, 10, 12): 0.76, (5, 11, 12): 0.71, (6, 7, 8): 0.92, (6, 7, 9): 0.91, 
        (6, 7, 10): 0.90, (6, 7, 11): 0.89, (6, 7, 12): 0.89, (6, 8, 9): 0.90, (6, 8, 10): 0.91, (6, 8, 11): 0.85,
        (6, 8, 12): 0.88, (6, 9, 10): 0.85, (6, 9, 11): 0.81, (6, 9, 12): 0.83, (6, 10, 11): 0.80, (6, 10, 12): 0.82,
        (6, 11, 12): 0.76, (7, 8, 9): 0.89, (7, 8, 10): 0.89, (7, 8, 11): 0.86, (7, 8, 12): 0.86, (7, 9, 10): 0.85, 
        (7, 9, 11): 0.79, (7, 9, 12): 0.81, (7, 10, 11): 0.79, (7, 10, 12): 0.81, (7, 11, 12): 0.75, (8, 9, 10): 0.80, 
        (8, 9, 11): 0.77, (8, 9, 12): 0.77, (8, 10, 11): 0.74, (8, 10, 12): 0.76, (8, 11, 12): 0.68, (9, 10, 11): 0.67, 
        (9, 10, 12): 0.66, (9, 11, 12): 0.58, (10, 11, 12): 0.52 
        }

    def __init__(self):
        # Permanent markers for each player (column -> position)
        self.player_markers = defaultdict(lambda: defaultdict(int))
        # Temporary markers during a turn (column -> position)
        self.temp_markers = {}
        # Completed columns
        self.completed = set()
        
    def is_column_complete(self, column: int) -> bool:
        #Check if a column is completed
        return column in self.completed
    
    def get_available_columns(self, player: int) -> Set[int]:
        #get columns that can still be climbed by any player
        return set(range(2, 13)) - self.completed
    
    def can_place_marker(self, column: int) -> bool:
        #Check if a marker can be placed in this column
        return column not in self.completed
    
    def get_success_probability(self, temp_markers: dict) -> float:
        #Get probability of hitting at least one active column
        if not temp_markers:
            return 1.0  # No columns active yet
        
        # Get sorted tuple of active columns
        active_cols = tuple(sorted(temp_markers.keys()))
        #num_cols = len(active_cols)
        return self.Prob_Table.get(active_cols,0.0)
        # Look up in probability table
        #if active_cols in self.Prob_Table:
        #    return self.Prob_Table[active_cols]
        
        #return 0.0


class CantStopGame:
    # game logic 
    
    def __init__(self, num_players = 2):
        self.board = CantStopBoard()
        self.num_players = num_players
        self.current_player = 0
        self.winner = None
        
    def roll_dice(self) -> List[int]:
        # roll 4 dice
        return [random.randint(1, 6) for _ in range(4)]
    
    def get_possible_pairs(self, dice: List[int]) -> List[Tuple[int, int]]:
        #Get all possible pairs from 4 dice
        #returns list of tuples with the two sums.
        
        d1, d2, d3, d4 = dice #orginally sorted(dice)
        
        pairs = []
        # Three ways to pair 4 dice
        pairs.append(tuple(sorted([d1 + d2, d3 + d4])))
        pairs.append(tuple(sorted([d1 + d3, d2 + d4])))
        pairs.append(tuple(sorted([d1 + d4, d2 + d3])))
        
        # Remove duplicates while preserving order
        seen = set()
        unique_pairs = []
        for pair in pairs:
            if pair not in seen:
                seen.add(pair)
                unique_pairs.append(pair)
        
        return unique_pairs
    
    def is_valid_move(self, columns: Tuple[int, int]) -> bool:
        #Check if chosen columns can be played
        temp_cols = set(self.board.temp_markers.keys())
        ##chosen = set(columns)
        ##
        ## #Can't place on completed columns
        ##if any(self.board.is_column_complete(c) for c in chosen):
        ##    return False
        
        # Above statment changed for below statement as bug fix
        #valid_chosen = set(c for c in columns if not self.board.is_column_complete(c))

        # Filters out completed columns as valid moves
        valid_chosen = set()
        for c in columns:
            # check if permant markers have reached column height
            if self.board.is_column_complete(c):
                continue
            # check if temp markers have reached column height
            if c in self.board.temp_markers and self.board.temp_markers[c] >= self.board.Column_Heights[c]:
                continue
            valid_chosen.add(c)

        if not valid_chosen:
            return False
        # Calc how many new columns this move would add
        #new_columns = chosen - temp_cols
        #total_columns_after = len(temp_cols) + len(new_columns)
        #
        # Can't have more than 3 different columns with temp markers
        #if total_columns_after > 3:
        #    return False
        #
        #return True

        # Above commented code was a bug

        # less than 3 cloumns, any move is valid
        if len(temp_cols) < 3:
            return True
        # if we have 3 columns, a pair must at least 1 current cloumn to be a valid move
        if len(temp_cols) ==3:  # 8==D
            return len(valid_chosen & temp_cols) > 0 # chosen -> valid_chosen for bug fix
        return False

    def get_valid_moves(self, dice: List[int]) -> List[Tuple[int, int]]:
        possible_pairs = self.get_possible_pairs(dice)
        valid = []
        
        for pair in possible_pairs:
            if self.is_valid_move(pair):
                valid.append(pair)
        
        return valid
    
    def make_move(self, columns: Tuple[int, int]): 
        for col in columns:
            # added IF statement as bug fix
            if self.board.is_column_complete(col):
                continue

            if col in self.board.temp_markers:
                self.board.temp_markers[col] += 1
            #else:
                # Start from player's permanent position
            #    start_pos = self.board.player_markers[self.current_player][col]
            #    self.board.temp_markers[col] = start_pos + 1
            elif len(self.board.temp_markers) <3: # changed the above ELSE for bug fix 
                start_pos = self.board.player_markers[self.current_player][col]
                self.board.temp_markers[col] = start_pos + 1
            
    def bust(self): # Lose progess
        self.board.temp_markers = {}
        self.next_player()
    
    def stop(self): # Keep progress
        for col, pos in self.board.temp_markers.items():
            self.board.player_markers[self.current_player][col] = pos
            
            # Check if column is completed
            if pos >= self.board.Column_Heights[col]:
                self.board.completed.add(col)
                
                # Check win condition (3 columns completed)
                completed_by_player = sum(
                    1 for c in self.board.completed 
                    if self.board.player_markers[self.current_player][c] >= self.board.Column_Heights[c]
                )
                if completed_by_player == 3:
                    self.winner = self.current_player
        
        self.board.temp_markers = {}
        self.next_player()
    
    def next_player(self):
        # move to next player
        self.current_player = (self.current_player + 1) % self.num_players
    
    def is_game_over(self) -> bool:
        # check for game over
        return self.winner is not None

class PlayerStrategy:
    
    def decide_to_roll(self,game:CantStopGame) -> bool:
        #Decide to stop
        raise NotImplementedError

    def choose_move(self, game: CantStopGame, valid_moves: List[Tuple[int, int]]) -> Optional[Tuple[int, int]]:
        # pick a valid move
        raise NotImplementedError

class RuleOf28:
    # Calculator for Rule of 28 points
    # [6, 5, 4, 3, 2, 1, 2, 3, 4, 5, 6] points for moving cols 2-12
    # Double for first placement 
    # After all 3 markers are placed:
    # All odd: +2
    # All even: -2
    # All below col 8 or above col 6: +4

    COLUMN_POINTS = {
        2: 6, 3: 5, 4: 4, 5: 3, 6: 2,
        7: 1, 8: 2, 9: 3, 10: 4, 11: 5, 12: 6
    }

    def calulate_points(game: CantStopGame, columns_started_this_turn: Set[int]) -> float:
        # Calcs RO28 for the turn
        temp_sum=0
        current_player = game.current_player

        for col, temp_pos in game.board.temp_markers.items():
            permanent_pos = game.board.player_markers[current_player][col]
            progress_this_turn = temp_pos - permanent_pos

            points_per_space = RuleOf28.COLUMN_POINTS[col]
            # Check for 1st time column placement 
            if col in columns_started_this_turn:
                temp_sum += points_per_space * 2 #double points for 1st placement
                temp_sum += (progress_this_turn-1) * points_per_space # regular points
            else:
                temp_sum += progress_this_turn*points_per_space # regular points

        # Additonal point cases
        active_cols = list(game.board.temp_markers.keys())
        if len(active_cols) ==3:
            if all(col%2 ==1 for col in active_cols):
                temp_sum += 2 # +2 for all even cols
            elif all(col%2 ==0 for col in active_cols):
                temp_sum -= 2 # -2 for all odd cols
            if all(col<8 for col in active_cols) or all(col >6 for col in active_cols):
                temp_sum += 4 # +4 for cols<8 or cols>6
        
        return temp_sum

class BasicCautiousPlayer(PlayerStrategy): 
# Basic Cautious strategy: always stops after 3 successful rolls, picks moves at random
    def __init__(self, max_rolls = 3, stop_probability = 0.5):
        self.max_rolls = max_rolls
        self.rolls_this_turn = 0
        self.stop_probability = stop_probability
        self.columns_started_this_turn = set() # Ro28

    def decide_to_roll(self, game: CantStopGame):
        # Must roll at least once
        if self.rolls_this_turn == 0:
            self.columns_started_this_turn = set() # Ro28
            return True
        # Can'r roll more than the max (3)
        if self.rolls_this_turn >= self.max_rolls:
            return False
        # Choice to roll again is 50%
        return random.random() >= self.stop_probability
    
    def choose_move(self, game: CantStopGame, valid_moves: List[Tuple[int, int]]) -> Tuple[int, int]:
        #if not valid_moves:
        #    return None
        #
        self.rolls_this_turn += 1
        # move choice is random
        return random.choice(valid_moves)
    
        # -- Bug Fixs
        # Stop after max rolls
        #if self.rolls_this_turn <= self.max_rolls:
        #    #self.rolls_this_turn = 0
        #    if random.random() < self.stop_probability:
        #        return None
        #    return random.choice(valid_moves) 
        # Stop when rolls > 3
        #
        #return None      

class DecentCautiousPlayer(PlayerStrategy):
# Decent Cautious strategy: always stops until after 3 successful rolls, picks moves with strategry
    def __init__(self, max_rolls = 3, risk_threshold = 0.75): 
        self.max_rolls = max_rolls
        self.rolls_this_turn = 0
        self.risk_threshold = risk_threshold

        self.columns_started_this_turn = set() #Ro28
    
    def decide_to_roll(self, game: CantStopGame) -> bool:
        #if not valid_moves:
        #    return None

        # Must roll at least once
        if self.rolls_this_turn == 0:
            self.columns_started_this_turn = set() #Ro28
            return True

        #self.rolls_this_turn += 1
        
        # Stop if move completed the column
        for col in game.board.temp_markers:
            if game.board.temp_markers[col] >= game.board.Column_Heights[col]:
                return False

        # Always stop after max rolls (3)
        if self.rolls_this_turn >= self.max_rolls:
            return False
        
        #Check for all 3 markers placed
        temp_cols = set(game.board.temp_markers.keys())
        if len(temp_cols) ==3: # Check if all 3 markers are down
            success_prob = game.board.get_success_probability(game.board.temp_markers)
            if success_prob < self.risk_threshold: # If chance of getting a valid move < threshold, stop
                return False

        return True
        # Bug code 
        #if self.rolls_this_turn <= self.max_rolls:
        #    temp_cols = set(game.board.temp_markers.keys()) 
        #    if len(temp_cols) == 3: # Check if all 3 markers are down
        #        success_prob = game.board.get_success_probability(game.board.temp_markers)
        #        if success_prob < self.risk_threshold: # If chance of getting a valid move < threshold, stop
        #            return None
        #    return self.pick_best_move(game, valid_moves) # Pick best move
        # Always stop after max_rolls is achvied
        #return None
        
    def choose_move(self, game: CantStopGame, valid_moves: List[Tuple[int, int]]) -> Tuple[int, int]:
        self.rolls_this_turn += 1
        return self.pick_best_move(game, valid_moves)
    
    def pick_best_move(self, game: CantStopGame, valid_moves: List[Tuple[int, int]]) -> Tuple[int, int]:
        #Pick the best move strategically
        temp_cols = set(game.board.temp_markers.keys())
        
        # Prefer moves that use existing columns
        for move in valid_moves:
            if move[0] in temp_cols or move[1] in temp_cols:
                return move
        
        # Otherwise prefer columns closer to center (7)
        return min(valid_moves, key=lambda m: abs(m[0] - 7) + abs(m[1] - 7))

class AdvancedCautiousPlayer(PlayerStrategy):
    def __init__(self, max_rolls = 3, risk_threshold = 0.75): 
        self.max_rolls = max_rolls
        self.rolls_this_turn = 0
        self.risk_threshold = risk_threshold

        self.columns_started_this_turn = set() #Ro28
    
    def decide_to_roll(self, game: CantStopGame) -> bool:
        # Must roll at least once
        if self.rolls_this_turn == 0:
            self.columns_started_this_turn = set() #Ro28
            return True

        # Stop if move completed the column
        for col in game.board.temp_markers:
            if game.board.temp_markers[col] >= game.board.Column_Heights[col]:
                return False

        # Always stop after max rolls (3)
        if self.rolls_this_turn >= self.max_rolls:
            return False
        
        #Check for all 3 markers placed
        temp_cols = set(game.board.temp_markers.keys())
        if len(temp_cols) ==3: # Check if all 3 markers are down
            success_prob = game.board.get_success_probability(game.board.temp_markers)
            if success_prob < self.risk_threshold: # If chance of getting a valid move < threshold, stop
                return False

        return True
        
    def choose_move(self, game: CantStopGame, valid_moves: List[Tuple[int, int]]) -> Tuple[int, int]:
        self.rolls_this_turn += 1
        return self.pick_best_move(game, valid_moves)
    
    def pick_best_move(self, game: CantStopGame, valid_moves: List[Tuple[int, int]]) -> Tuple[int, int]:
        #Pick the best move strategically
        temp_cols = set(game.board.temp_markers.keys())
        current_player = game.current_player
        opponent_id = 1 - current_player
    
        # get columns with progress
        existing_moves = [m for m in valid_moves if m[0] in temp_cols or m[1] in temp_cols]

        # calc number of oppent completed columns
        opponent_completed = sum(
            1 for col in game.board.completed
            if game.board.player_markers[opponent_id][col] >= game.board.Column_Heights[col])

        # Early game stragies, when the opponent doesn't pose threat of winning
        if opponent_completed == 0:
            
            # Calc columns with progress
            progress_moves = [
            m for m in valid_moves 
            if game.board.player_markers[current_player][m[0]] > 0 
            or game.board.player_markers[current_player][m[1]] > 0]

            if progress_moves: # pick permeant progress moves further from the center
                return max(progress_moves, key=lambda m: abs(m[0] - 7) + abs(m[1] - 7))
            
            if existing_moves: # else proitize moves with progress already 
                return existing_moves[0]
            
            if random.random() > 0.5: # otherwise just pick non center or center randomly
                return max(valid_moves, key=lambda m: abs(m[0] - 7) + abs(m[1] - 7)) # prefer short columns
            else: 
                return min(valid_moves, key=lambda m: abs(m[0] - 7) + abs(m[1] - 7)) # prefer long columns
            
        # Among existing columns, avoid opponent threatened ones    
        if existing_moves: 
            return min(existing_moves, key=lambda m: self._move_score(game, m, current_player))
    
        # For new columns, pick based on opponent threat and position
        return min(valid_moves, key=lambda m: self._move_score(game, m, current_player))

    def _move_score(self, game: CantStopGame, move: Tuple[int, int], current_player: int) -> float:
        #Calculate move score (lower is better), considers opponent threats and column preference
        score = 0
        
        for col in move:
            if col in game.board.completed:
                score += 1000  # Can't play completed columns
                continue
            
            col_height = game.board.Column_Heights[col]
            my_progress = game.board.player_markers[current_player][col]
            
            # Check opponent threat on this column
            for player in range(game.num_players):
                if player == current_player:
                    continue
                
                opponent_progress = game.board.player_markers[player][col]
                if opponent_progress > 0:
                    completion_ratio = opponent_progress / col_height
                    
                    # Penalize columns where opponents are close to winning
                    if completion_ratio > 0.7:
                        score += 50  # Very threatened
                    elif completion_ratio > 0.5:
                        score += 20  # Moderately threatened
                    elif completion_ratio > 0.3:
                        score += 5   # Slightly threatened
            
            # Bonus for columns where we have progress
            if my_progress > 0:
                score -= 10 * (my_progress / col_height)
            
            # Slight preference for center columns
            score += abs(col - 7) * 0.5
        
        return score 

class BasicAggressivePlayer(PlayerStrategy):
    #Basic Aggressive strategy: doens't consider stop until after 3 successful rolls, randomly picks moves
    def __init__(self, min_rolls= 3, stop_probability = 0.5):
        self.min_rolls = min_rolls
        self.rolls_this_turn = 0
        self.stop_probability = stop_probability
        self.columns_started_this_turn = set() # Ro28

    def decide_to_roll(self, game: CantStopGame) -> bool:
        if self.rolls_this_turn < self.min_rolls:
            self.columns_started_this_turn = set() # Ro28
            return True
        return random.random() >= self.stop_probability # added for bug fixes
    
    def choose_move(self, game: CantStopGame, valid_moves: List[Tuple[int, int]]) -> Tuple[int, int]:
        #if not valid_moves:
        #    return None
        
        self.rolls_this_turn += 1
        
        # Buggy code
        #if self.rolls_this_turn <= self.min_rolls:
        #    return random.choice(valid_moves)
        # Once # of rolls > 3, 50% to stop
        #if random.random() < self.stop_probability:
        #    return None

        # cant stop after min rolls
        return random.choice(valid_moves) 

class DecentAggressivePlayer(PlayerStrategy):
    def __init__(self, min_rolls= 3, risk_threshold = 0.75):
        self.min_rolls = min_rolls
        self.rolls_this_turn = 0
        self.risk_threshold = risk_threshold
        self.columns_started_this_turn = set() # Ro28

    def decide_to_roll(self, game: CantStopGame) -> bool:
        # Must roll at least min times (3)
        if self.rolls_this_turn < self.min_rolls:
            self.columns_started_this_turn = set() # Ro28
            return True
        
        # Stop if column complete
        for col in game.board.temp_markers:
            if game.board.temp_markers[col] >= game.board.Column_Heights[col]:
                return False
        
        #Check risk after 3 markers are down
        temp_cols = set(game.board.temp_markers.keys()) 
        if len(temp_cols) == 3: # Check if all 3 markers are down
            success_prob = game.board.get_success_probability(game.board.temp_markers)       
            if success_prob < self.risk_threshold: # If chance of getting a valid move < threshold, stop
                return False
            
        # Will roll max of p/(1-p) times, rounded down to nearest integer
            max_rolls = round((1/(1-success_prob))-(1/success_prob))
            if self.rolls_this_turn > (max_rolls+self.min_rolls):
                return False
            
        return True
    
    def choose_move(self, game: CantStopGame, valid_moves: List[Tuple[int, int]]) -> Optional[Tuple[int, int]]:
        #if not valid_moves:
        #    return None
        
        self.rolls_this_turn += 1
        return self.pick_best_move(game, valid_moves)
    
        # Retired Buggy code
        # Stop if move completed the column
        #for col in game.board.temp_markers:
        #    if game.board.temp_markers[col] >= game.board.Column_Heights[col]:
        #        return None
        #    
        #if self.rolls_this_turn <= self.min_rolls: # always roll at least 3 times
        #    return self.pick_best_move(game, valid_moves) # Pick best move
        # After rolling 3 times, check if all 3 markers are placed
        #temp_cols = set(game.board.temp_markers.keys()) 
        #if len(temp_cols) == 3: # Check if all 3 markers are down
        #    success_prob = game.board.get_success_probability(game.board.temp_markers)       
        #    if success_prob < self.risk_threshold: # If chance of getting a valid move < threshold, stop
        #        return None
        #    # Will roll a maximum of p/1-p times
        #    max_rolls = round(success_prob/(1-success_prob))
        #    if self.rolls_this_turn > max_rolls:
        #        return None
        #return self.pick_best_move(game, valid_moves)

    def pick_best_move(self, game: CantStopGame, valid_moves: List[Tuple[int, int]]) -> Tuple[int, int]:
        #Pick the best move strategically
        temp_cols = set(game.board.temp_markers.keys())
        
        # Prefer moves that use existing columns
        for move in valid_moves:
            if move[0] in temp_cols or move[1] in temp_cols:
                return move
        
        # Otherwise prefer columns closer to center (7)
        return min(valid_moves, key=lambda m: abs(m[0] - 7) + abs(m[1] - 7))
    
class AdvancedAggressivePlayer(PlayerStrategy):
    def __init__(self, min_rolls= 3, risk_threshold = 0.75):
        self.min_rolls = min_rolls
        self.rolls_this_turn = 0
        self.risk_threshold = risk_threshold
        self.columns_started_this_turn = set() # Ro28
    
    def decide_to_roll(self, game: CantStopGame) -> bool:
      # Must roll at least min times (3)
        if self.rolls_this_turn < self.min_rolls:
            self.columns_started_this_turn = set() # Ro28
            return True

        temp_cols = set(game.board.temp_markers.keys()) 
        if len(temp_cols) != 3: # Always roll if 3 markers aren't placed
            return True
        
        # Stop if column complete
        for col in game.board.temp_markers:
            if game.board.temp_markers[col] >= game.board.Column_Heights[col]:
                return False
        
        #Check risk after 3 markers are down
        temp_cols = set(game.board.temp_markers.keys()) 
        if len(temp_cols) == 3: # Check if all 3 markers are down
            success_prob = game.board.get_success_probability(game.board.temp_markers)       
            if success_prob < self.risk_threshold: # If chance of getting a valid move < threshold, stop
                return False

        # Will roll max of 1/(1-p)-1/p times, rounded down to nearest integer
            max_rolls = round((1/(1-success_prob))-(1/success_prob))
            if self.rolls_this_turn > (max_rolls+self.min_rolls):
                return False

        return True # If points are less than 28, all 3 markes are placed, and a column hasn't been finished this turn -> roll the dice
    
    def choose_move(self, game: CantStopGame, valid_moves: List[Tuple[int, int]]) -> Tuple[int, int]:
        self.rolls_this_turn += 1
        return self.pick_best_move(game, valid_moves)
    
    def pick_best_move(self, game: CantStopGame, valid_moves: List[Tuple[int, int]]) -> Tuple[int, int]:
        #Pick the best move strategically
        temp_cols = set(game.board.temp_markers.keys())
        current_player = game.current_player
        opponent_id = 1 - current_player
    
        # get columns with progress
        existing_moves = [m for m in valid_moves if m[0] in temp_cols or m[1] in temp_cols]
        
        # calc number of oppent completed columns
        opponent_completed = sum(
            1 for col in game.board.completed
            if game.board.player_markers[opponent_id][col] >= game.board.Column_Heights[col])

        # Early game stragies, when the opponent doesn't pose threat of winning
        if opponent_completed == 0:
            
            # Calc columns with progress
            progress_moves = [
            m for m in valid_moves 
            if game.board.player_markers[current_player][m[0]] > 0 
            or game.board.player_markers[current_player][m[1]] > 0]

            if progress_moves: # pick permeant progress moves further from the center
                return max(progress_moves, key=lambda m: abs(m[0] - 7) + abs(m[1] - 7))
            
            if existing_moves: # else proitize moves with progress already 
                return existing_moves[0]
            
            if random.random() > 0.5: # otherwise just pick non center or center randomly
                return max(valid_moves, key=lambda m: abs(m[0] - 7) + abs(m[1] - 7)) # prefer short columns
            else: 
                return min(valid_moves, key=lambda m: abs(m[0] - 7) + abs(m[1] - 7)) # prefer long columns
        
        # Among existing columns, avoid opponent threatened ones    
        if existing_moves: 
            return min(existing_moves, key=lambda m: self._move_score(game, m, current_player))
    
        # For new columns, pick based on opponent threat and position
        return min(valid_moves, key=lambda m: self._move_score(game, m, current_player))

    def _move_score(self, game: CantStopGame, move: Tuple[int, int], current_player: int) -> float:
        #Calculate move score (lower is better), considers opponent threats and column preference
        score = 0
        
        for col in move:
            if col in game.board.completed:
                score += 1000  # Can't play completed columns
                continue
            
            col_height = game.board.Column_Heights[col]
            my_progress = game.board.player_markers[current_player][col]
            
            # Check opponent threat on this column
            for player in range(game.num_players):
                if player == current_player:
                    continue
                
                opponent_progress = game.board.player_markers[player][col]
                if opponent_progress > 0:
                    completion_ratio = opponent_progress / col_height
                    
                    # Penalize columns where opponents are close to winning
                    if completion_ratio > 0.7:
                        score += 50  # Very threatened
                    elif completion_ratio > 0.5:
                        score += 20  # Moderately threatened
                    elif completion_ratio > 0.3:
                        score += 5   # Slightly threatened
            
            # Bonus for columns where we have progress
            if my_progress > 0:
                score -= 10 * (my_progress / col_height)
            
            # Slight preference for center columns
            score += abs(col - 7) * 0.5
        
        return score  

class RuleOf28Player(PlayerStrategy): # Follows the Ro28 EXACTLY as explained by Michael Keller
    def __init__(self):
        self.rolls_this_turn = 0
        self.threshold = 28
        self.columns_started_this_turn = set() # Ro28 
    
    def decide_to_roll(self, game: CantStopGame) -> bool:
        if self.rolls_this_turn == 0: # Must roll at least once
            self.columns_started_this_turn = set() #Ro28
            return True
        
        temp_sum = RuleOf28.calulate_points(game, self.columns_started_this_turn)

        temp_cols = set(game.board.temp_markers.keys()) 
        if len(temp_cols) != 3: # Always roll if 3 markers aren't placed
            return True
        
        if temp_sum >= self.threshold: # ONLY Stop once 28 points are reached and 3 markers are places
            return False
        
        return True # points are less than 28, all markes are down -> roll the dice
    
    def choose_move(self, game: CantStopGame, valid_moves: List[Tuple[int, int]]) -> Tuple[int, int]:
        self.rolls_this_turn += 1
        ## Track started columns
        #for col in game.board.temp_markers.keys():
        #    if game.board.player_markers[game.current_player][col] == 0:
        #        self.columns_started_this_turn.add(col)
        return self.pick_best_move(game, valid_moves)
    
    def pick_best_move(self, game: CantStopGame, valid_moves: List[Tuple[int, int]]) -> Tuple[int, int]:
        #Pick the best move strategically
        temp_cols = set(game.board.temp_markers.keys())
        
        # Prefer moves that use existing columns
        for move in valid_moves:
            if move[0] in temp_cols or move[1] in temp_cols:
                return move
        
        # Otherwise prefer columns closer to center (7)
        return min(valid_moves, key=lambda m: abs(m[0] - 7) + abs(m[1] - 7))

class SmartRuleOf28Player(PlayerStrategy): # Smart Ro28 Player, uses the rule to it's advatage while ignoring it when best, similar to how a 'human player' would perform
    def __init__(self):
        self.rolls_this_turn = 0
        self.threshold = 28
        self.columns_started_this_turn = set() # Ro28 
    
    def decide_to_roll(self, game: CantStopGame) -> bool:
        if self.rolls_this_turn == 0: # Must roll at least once
            self.columns_started_this_turn = set() #Ro28
            return True
        
        temp_sum = RuleOf28.calulate_points(game, self.columns_started_this_turn)

        temp_cols = set(game.board.temp_markers.keys()) 
        if len(temp_cols) != 3: # Always roll if 3 markers aren't placed
            return True
        
        for col in game.board.temp_markers: # Stop when a column is completed
            if game.board.temp_markers[col] >= game.board.Column_Heights[col]:
                return False
        
        if temp_sum >= self.threshold: # Stop once 28 points are reached and 3 markers are places
            return False

        return True # If points are less than 28, all 3 markes are placed, and a column hasn't been finished this turn -> roll the dice
    
    def choose_move(self, game: CantStopGame, valid_moves: List[Tuple[int, int]]) -> Tuple[int, int]:
        self.rolls_this_turn += 1
        return self.pick_best_move(game, valid_moves)
    
    def pick_best_move(self, game: CantStopGame, valid_moves: List[Tuple[int, int]]) -> Tuple[int, int]:
        #Pick the best move strategically
        temp_cols = set(game.board.temp_markers.keys())
        current_player = game.current_player
        opponent_id = 1 - current_player
    
        # get columns with progress
        existing_moves = [m for m in valid_moves if m[0] in temp_cols or m[1] in temp_cols]
        '''
        # calc number of oppent completed columns
        opponent_completed = sum(
            1 for col in game.board.completed
            if game.board.player_markers[opponent_id][col] >= game.board.Column_Heights[col])

        # Early game stragies, when the opponent doesn't pose threat of winning
        if opponent_completed == 0:
            
            # Calc columns with progress
            progress_moves = [
            m for m in valid_moves 
            if game.board.player_markers[current_player][m[0]] > 0 
            or game.board.player_markers[current_player][m[1]] > 0]

            if progress_moves: # pick permeant progress moves further from the center
                return max(progress_moves, key=lambda m: abs(m[0] - 7) + abs(m[1] - 7))
            
            if existing_moves: # else proitize moves with progress already 
                return existing_moves[0]
            
            if random.random() > 0.5: # otherwise just pick non center or center randomly
                return max(valid_moves, key=lambda m: abs(m[0] - 7) + abs(m[1] - 7)) # prefer short columns
            else: 
                return min(valid_moves, key=lambda m: abs(m[0] - 7) + abs(m[1] - 7)) # prefer long columns
        '''
        # Among existing columns, avoid opponent threatened ones    
        if existing_moves: 
            return min(existing_moves, key=lambda m: self._move_score(game, m, current_player))
    
        # For new columns, pick based on opponent threat and position
        return min(valid_moves, key=lambda m: self._move_score(game, m, current_player))

    def _move_score(self, game: CantStopGame, move: Tuple[int, int], current_player: int) -> float:
        #Calculate move score (lower is better), considers opponent threats and column preference
        score = 0
        
        for col in move:
            if col in game.board.completed:
                score += 1000  # Can't play completed columns
                continue
            
            col_height = game.board.Column_Heights[col]
            my_progress = game.board.player_markers[current_player][col]
            
            # Check opponent threat on this column
            for player in range(game.num_players):
                if player == current_player:
                    continue
                
                opponent_progress = game.board.player_markers[player][col]
                if opponent_progress > 0:
                    completion_ratio = opponent_progress / col_height
                    
                    # Penalize columns where opponents are close to winning
                    if completion_ratio > 0.7:
                        score += 50  # Very threatened
                    elif completion_ratio > 0.5:
                        score += 20  # Moderately threatened
                    elif completion_ratio > 0.3:
                        score += 5   # Slightly threatened
            
            # Bonus for columns where we have progress
            if my_progress > 0:
                score -= 10 * (my_progress / col_height)
            
            # Slight preference for center columns
            score += abs(col - 7) * 0.5
        
        return score        

class RandomPlayer(PlayerStrategy):
    #Random strategy: randomly chooses moves and when to stop
    def __init__(self, stop_probability = 0.5):
        #Args: stop_probability 50% (coin flip)
        self.stop_probability = stop_probability
        self.rolls_this_turn = 0
        self.columns_started_this_turn = set() #Ro28

    def decide_to_roll(self, game: CantStopGame):
        if self.rolls_this_turn == 0: # Must roll at least once
            self.columns_started_this_turn = set() #Ro28
            return True
        # Random deciede to stop
        return random.random() >= self.stop_probability
    
    def choose_move(self, game: CantStopGame, valid_moves: List[Tuple[int, int]]) -> Tuple[int, int]:
        #if not valid_moves:
        #    return None
        
        self.rolls_this_turn += 1
        return random.choice(valid_moves)

        # Randomly decide whether to stop (but not on first roll of turn)
        #if game.board.temp_markers and random.random() < self.stop_probability:
        #    return None
        
        # Choose randomly pick valid move
        #return random.choice(valid_moves)

def simulate_game(strategies: List[PlayerStrategy], verbose: bool = False) -> int:
    #Simulate a single game with given strategies.
    #Returns the winning player number.

    game = CantStopGame(num_players=len(strategies))
    
    for strategy in strategies:
        if hasattr(strategy, 'rolls_this_turn'):
            strategy.rolls_this_turn = 0
        if hasattr(strategy, 'has_rolled'):
            strategy.has_rolled = False

    while not game.is_game_over():
        player = game.current_player
        strategy = strategies[player]
        
        # Reset per-turn counters
        if hasattr(strategy, 'rolls_this_turn'):
            strategy.rolls_this_turn = 0
        if hasattr(strategy, 'has_rolled'):
            strategy.has_rolled = False
        if hasattr(strategy, 'columns_started_this_turn'):
            strategy.columns_started_this_turn = set()
        
        if verbose:
            print(f"\n=== Player {player}'s turn ===")
        
        turn_active = True
        while turn_active:

            should_roll = strategy.decide_to_roll(game)
            if verbose:
                if hasattr(strategy, 'columns_started_this_turn'):
                    rule28_points = RuleOf28.calulate_points(game, strategy.columns_started_this_turn)
                    print(f"Rule of 28 Points: {rule28_points}")    

            if not should_roll:
                if verbose:
                    print("Player Stops")
                    print(f"Temp markers: {dict(game.board.temp_markers)}")
                    print(f"Complete Cols: {game.board.completed}")

                    if hasattr(strategy, 'columns_started_this_turn'):
                        rule28_points = RuleOf28.calulate_points(game, strategy.columns_started_this_turn)
                        print(f"Rule of 28 Points: {rule28_points}")

                game.stop()
                turn_active = False
                continue

            dice = game.roll_dice()
            valid_moves = game.get_valid_moves(dice)
            
            if verbose:
                print(f"Rolled: {dice}, Valid moves: {valid_moves}")
            
            if not valid_moves:
                if verbose:
                    print("BUST!")
                    print(game.board.completed)
                game.bust()
                turn_active=False
                continue
            
            # Choose move and make it
            move = strategy.choose_move(game, valid_moves)

            if hasattr(strategy, 'columns_started_this_turn'):
                for col in move:
                    if col not in game.board.temp_markers:
                        strategy.columns_started_this_turn.add(col)

            game.make_move(move)

            #if move is None:
            #    if verbose:
            #        print("Player Stops")
            #        print(f"Temp markers: {dict(game.board.temp_markers)}")
            #        print(game.board.completed)
            #    game.stop()
            #    turn_active=False
            #    continue

            #game.make_move(move)

            if verbose:
                print(f"Chose: {move}, Temp markers: {dict(game.board.temp_markers)}")
    
    if verbose:
        winner_name = strategies[game.winner].__class__.__name__
        print(f"\n*** {winner_name} (Player {game.winner}) wins! ***")

    return game.winner

def run_simulations(num_games: int = 1000):
    start = time.time()
    strategies = [
        #BasicCautiousPlayer(),
        #BasicAggressivePlayer(),
        #DecentCautiousPlayer(),
        DecentAggressivePlayer(),
        #AdvancedCautiousPlayer(),
        AdvancedAggressivePlayer(),
        #RandomPlayer(),
        #RandomPlayer(),
        #RuleOf28Player(),
        #SmartRuleOf28Player(),
        ]
    
    wins = [0] * len(strategies)
    
    for i in range(num_games):
        winner = simulate_game(strategies, verbose=False)
        wins[winner] += 1
        
        if (i + 1) % 500 == 0:
            print(f"Completed {i + 1} games...")
    
    print(f"\n=== Results after {num_games} games ===")
    for i, w in enumerate(wins):
        print(f"{strategies[i].__class__.__name__}: {w} wins ({w/num_games*100:.1f}%)")
    end = time.time()
    print(f"{end-start} Seconds")


if __name__ == "__main__":
    # Run a single verbose game
    print("Running single game:\n")

    #strategies = [BasicAggressivePlayer(), DecentAggressivePlayer()]
    #strategies = [DecentCautiousPlayer(), DecentAggressivePlayer()]
    #strategies = [BasicCautiousPlayer(), DecentCautiousPlayer()]
    #strategies = [BasicCautiousPlayer(),BasicAggressivePlayer()]
    #strategies = [RandomPlayer(),BasicCautiousPlayer()]
    #strategies = [RuleOf28Player(),DecentCautiousPlayer()]
    #strategies = [RuleOf28Player(),SmartRuleOf28Player()]
    #strategies = [AdvancedCautiousPlayer(),AdvancedAggressivePlayer()]
    #strategies = [DecentCautiousPlayer(),AdvancedCautiousPlayer()]
    strategies = [DecentAggressivePlayer(),AdvancedAggressivePlayer()]


    winner = simulate_game(strategies, verbose=True)
    
    # Run simulations
    print("\n" + "="*50)
    print("Running 10000 game simulation...")
    print("="*50)
    run_simulations(10000)
