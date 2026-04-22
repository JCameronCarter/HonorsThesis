#Train the DQN player against multiple opponents
 
import os
import random
import time
import csv
import numpy as np
from rl_player import RLTrainer, DQNPlayer
from CantStop import (
    AdvancedAggressivePlayer, 
    AdvancedCautiousPlayer,
    SmartRuleOf28Player,
    RuleOf28Player,
    DecentAggressivePlayer,
    DecentCautiousPlayer,
    RandomPlayer
)


class MultiOpponentTrainer(RLTrainer):
    #Trainer that rotates through multiple opponents
    
    def __init__(self, opponents_pool):

        super().__init__(opponent=None) #create attributes
        self.opponents_pool = opponents_pool
        self.opponent = None

        # Track performance against each opponent type
        self.opponent_stats = {
            type(opp).__name__: {'wins': 0, 'games': 0} 
            for opp in opponents_pool
        }
    
    def select_opponent(self):
        #Select opponent for this episode
        self.opponent = random.choice(self.opponents_pool)
        return self.opponent
    
    def train_episode(self, verbose=False):
        #Train one episode with a randomly selected opponent
        opponent = self.select_opponent()
        opponent_name = type(opponent).__name__
        
        # Use parent class logic
        result = super().train_episode(verbose=verbose)
        
        # Track stats per opponent
        self.opponent_stats[opponent_name]['games'] += 1
        if result:
            self.opponent_stats[opponent_name]['wins'] += 1
        
        return result
    
    def print_opponent_stats(self):
        #Print win rates against each opponent type
        print("\n" + "="*60)
        print("Performance by Opponent Type")
        print("="*60)
        
        for opp_name, stats in sorted(self.opponent_stats.items()):
            if stats['games'] > 0:
                win_rate = stats['wins'] / stats['games']
                print(f"{opp_name:30s}: {stats['wins']:4d}/{stats['games']:4d} ({win_rate:.1%})")

    def get_stats(self):
        #Get stats for csv
        stats = {'episode': self.episodes,
                'win_rate_overall': self.wins / self.episodes if self.episodes > 0 else 0,
                'epsilon': self.dqn_player.epsilon}
        # pure reward data
        if len(self.cumulative_rewards) > 0:
            stats['reward'] = self.cumulative_rewards[-1]
            stats['q_value'] = self.cumulative_q_values[-1]
            stats['ro28_points'] = self.cumulative_ro28_points[-1]
            stats['loss'] = self.cumulative_losses[-1]
        else:
            stats['reward'] = 0.0
            stats['q_value'] = 0.0
            stats['ro28_points'] = 0.0
            stats['loss'] = 0.0
    
        # smoothed reward data over 500 episodes
        window_size = min(500, len(self.cumulative_rewards))
        if window_size > 0:
            stats['reward_smooth'] = np.mean(self.cumulative_rewards[-window_size:])
            stats['q_value_smooth'] = np.mean(self.cumulative_q_values[-window_size:])
            stats['ro28_points_smooth'] = np.mean(self.cumulative_ro28_points[-window_size:])
            stats['loss_smooth'] = np.mean(self.cumulative_losses[-window_size:])
        else:
            stats['reward_smooth'] = 0.0
            stats['q_value_smooth'] = 0.0
            stats['ro28_points_smooth'] = 0.0
            stats['loss_smooth'] = 0.0
        #Getting Opponent stats
        name_mapping = {
                'AdvancedAggressivePlayer': 'AAP',
                'AdvancedCautiousPlayer': 'ACP',
                'DecentAggressivePlayer': 'DAP',
                'DecentCautiousPlayer': 'DCP',
                'RandomPlayer': 'RP',
                'RuleOf28Player': 'R28P',
                'SmartRuleOf28Player': 'SR28P',
            }
            
        for full_name, abbrev in name_mapping.items():
            if full_name in self.opponent_stats:
                games = self.opponent_stats[full_name]['games']
                wins = self.opponent_stats[full_name]['wins']
                win_rate = wins / games if games > 0 else 0                    
                stats[f'{abbrev}_winrate'] = win_rate
            else:
                stats[f'{abbrev}_winrate'] = 0.0    
        return stats

def setup_csv_logging(log_dir='logs'):
    #Setup csv
    os.makedirs(log_dir, exist_ok=True)
    csv_path = os.path.join(log_dir, 'training_log.csv')
    columns = [
        'episode', 'win_rate_overall', 'epsilon',
        'reward', 'q_value', 'ro28_points', 'loss',
        'reward_smooth', 'q_value_smooth', 'ro28_points_smooth', 'loss_smooth',
        'AAP_winrate',
        'ACP_winrate',
        'DAP_winrate',
        'DCP_winrate',
        'RP_winrate',
        'R28P_winrate',
        'SR28P_winrate'
    ]

        #create csv
    with open(csv_path,'w',newline='') as f:
        writer = csv.DictWriter(f, fieldnames=columns)
        writer.writeheader()
    return csv_path, columns

def log_to_csv(csv_path, columns, stats_dict):
    #Append stats to csv
    with open(csv_path,'a',newline='') as f:
        writer = csv.DictWriter(f, fieldnames=columns)
        writer.writerow(stats_dict)

def main():
    os.makedirs('models', exist_ok=True)
    
    print("="*60)
    print("Training DQN Player - Multi-Opponent Training")
    print("="*60)
    
    # Setup CSV logging
    csv_path, csv_columns = setup_csv_logging(log_dir='logs')

    # Create diverse opponent pool
    opponents_pool = [
        AdvancedAggressivePlayer(),
        AdvancedCautiousPlayer(),
        SmartRuleOf28Player(),
        RuleOf28Player(),
        DecentAggressivePlayer(),
        DecentCautiousPlayer(),
        RandomPlayer(stop_probability=0.5)
    ]
    
    print(f"\nTraining against {len(opponents_pool)} different opponent types:")
    for i, opp in enumerate(opponents_pool, 1):
        print(f"  {i}. {type(opp).__name__}")
    print()
    
    # Create trainer
    trainer = MultiOpponentTrainer(opponents_pool)

    # Train
    num_episodes = 20000
    start = time.time()
    print("="*60)
    print("Starting training")
    print("="*60)
    for episode in range(num_episodes):
        trainer.train_episode(verbose=(episode % 100 == 0))

        stats = trainer.get_stats()
        log_to_csv(csv_path, csv_columns, stats)

        # Update target network
        if episode % 100 == 0:
            trainer.dqn_player.update_target_model()
        
        # Save checkpoints
        if episode % 500 == 0 and episode > 0:
            trainer.dqn_player.model.save(f'models/dqn_multi_opp.h5.ep{episode}.keras')
            print(f"\nCheckpoint saved and logged at episode {episode}")
            trainer.print_opponent_stats()
        
        # Print progress
        if episode % 100 == 0 and episode > 0:
            win_rate = trainer.wins / episode
            print(f"\nEpisode {episode}/{num_episodes}")
            print(f"Overall: {trainer.wins} wins / {episode} games ({win_rate:.1%})")
            print(f"Epsilon: {trainer.dqn_player.epsilon:.3f}")
            print(f"\nTime Elapsed: {time.time() - start:.2f} seconds")
            
    end = time.time()
    # Final save
    trainer.dqn_player.model.save('models/dqn_multi_opp.keras')

    print("\n" + "="*60)
    print("Training Complete!")
    print("="*60)
    print(f"Total Games: {trainer.episodes}") 
    print(f"Overall Win Rate: {trainer.wins/trainer.episodes:.1%}")
    print(f"Epsilon: {trainer.dqn_player.epsilon:.3f}")
    print(f"Total Training Time: {end - start:.2f} seconds")
    
    trainer.print_opponent_stats()


if __name__ == "__main__":
    main()
# Q.E. motherfucking D.