import numpy as np
from rl_player import DQNPlayer
from CantStop import (
    CantStopGame,
    RandomPlayer,
    simulate_game
)


def quick_permutation_importance(model_path, num_games=200):
    #Quick feature importance test - permutes each feature and measures win rate drop
    
    # Feature names matching _encode_state order
    feature_names = []
    
    # My permanent progress (11 features)
    for col in range(2, 13):
        feature_names.append(f'my_progress_col_{col}')
    
    # Opponent permanent progress (11 features)
    for col in range(2, 13):
        feature_names.append(f'opp_progress_col_{col}')
    
    # Current temp markers (11 features)
    for col in range(2, 13):
        feature_names.append(f'temp_marker_col_{col}')
    
    # Completed columns (11 features)
    for col in range(2, 13):
        feature_names.append(f'completed_col_{col}')
    
    # Single-value features
    feature_names.extend([
        'rolls_this_turn',
        'ro28_points',
        'success_probability',
        'num_temp_markers',
        'my_completed_count',
        'opp_completed_count',
        'column_completed_this_turn'
    ])
    
    print(f"Total features: {len(feature_names)}")
    print(f"\nCalculating baseline performance ({num_games} games)")
    
    # 1. Baseline performance
    baseline_win_rate = evaluate_model(model_path, num_games)
    print(f"Baseline win rate: {baseline_win_rate:.1%}\n")
    
    # 2. Test each feature
    print("Testing feature importance")
    print("-" * 70)
    
    importance_scores = []
    
    for feature_idx, feature_name in enumerate(feature_names):
        # Progress indicator
        if (feature_idx + 1) % 10 == 0:
            print(f"Progress: {feature_idx + 1}/{len(feature_names)} features tested")
        
        # Evaluate with this feature permuted
        permuted_win_rate = evaluate_with_permuted_feature(
            model_path, 
            feature_idx, 
            num_games
        )
        
        # Importance = drop in performance
        importance = baseline_win_rate - permuted_win_rate
        
        importance_scores.append({
            'feature': feature_name,
            'importance': importance,
            'baseline': baseline_win_rate,
            'permuted': permuted_win_rate
        })
    
    return importance_scores, baseline_win_rate


def evaluate_model(model_path, num_games):
    #Evaluate model without any permutation
    dqn = DQNPlayer(load_model=model_path, training=False)
    opponent = RandomPlayer()
    
    wins = 0
    for _ in range(num_games):
        strategies = [dqn, opponent]
        winner = simulate_game(strategies, verbose=False)
        if winner == 0:
            wins += 1
    
    return wins / num_games


def evaluate_with_permuted_feature(model_path, feature_idx, num_games):
    #Evaluate with one feature randomly shuffled
    dqn = DQNPlayer(load_model=model_path, training=False)
    opponent = RandomPlayer()
    
    # Store original encode method
    original_encode = dqn._encode_state
    
    # Create permuted version
    def permuted_encode(game):
        state = original_encode(game)
        # Randomly shuffle this feature's value
        state[feature_idx] = np.random.rand()
        return state
    
    # Replace encode method
    dqn._encode_state = permuted_encode
    
    # Evaluate
    wins = 0
    for _ in range(num_games):
        strategies = [dqn, opponent]
        winner = simulate_game(strategies, verbose=False)
        if winner == 0:
            wins += 1
    
    return wins / num_games


def print_results(importance_scores, baseline_win_rate):
    #Print results in ranked order
    
    # Sort by importance
    sorted_scores = sorted(importance_scores, key=lambda x: x['importance'], reverse=True)
    
    print("\n" + "="*70)
    print("FEATURE IMPORTANCE RESULTS")
    print("="*70)
    print(f"Baseline Win Rate: {baseline_win_rate:.1%}\n")
    
    print(f"{'Rank':<6} {'Feature':<35} {'Importance':<12} {'Drop'}")
    print("-" * 70)
    
    for rank, score in enumerate(sorted_scores[:20], 1):  # Top 20
        importance = score['importance']
        drop_pct = importance * 100
        
        # Mark important features
        if importance > 0.05:
            marker = "***"
        elif importance > 0.02:
            marker = "** "
        elif importance > 0.01:
            marker = "*  "
        else:
            marker = "   "
        
        print(f"{rank:<6} {score['feature']:<35} {importance:>10.4f}  {drop_pct:>5.1f}% {marker}")
    
    print("\n*** = Very Important (>5% drop)")
    print("**  = Important (2-5% drop)")
    print("*   = Moderate (1-2% drop)")
    
    # Group analysis
    print("\n" + "="*70)
    print("FEATURE GROUP ANALYSIS")
    print("="*70)
    
    groups = {
        'My Progress': [s for s in sorted_scores if 'my_progress' in s['feature']],
        'Opponent Progress': [s for s in sorted_scores if 'opp_progress' in s['feature']],
        'Temp Markers': [s for s in sorted_scores if 'temp_marker' in s['feature']],
        'Completed Cols': [s for s in sorted_scores if 'completed' in s['feature']],
        'Other Features': [s for s in sorted_scores if not any(
            x in s['feature'] for x in ['my_progress', 'opp_progress', 'temp_marker', 'completed_col']
        )]
    }
    
    for group_name, features in groups.items():
        if features:
            avg_imp = np.mean([f['importance'] for f in features])
            max_imp = max([f['importance'] for f in features])
            max_feature = max(features, key=lambda x: x['importance'])
            
            print(f"\n{group_name.upper()}")
            print(f"  Avg importance: {avg_imp:.4f}")
            print(f"  Max importance: {max_imp:.4f} ({max_feature['feature']})")
            print(f"  Num features:   {len(features)}")


def save_to_csv(importance_scores, filename='feature_importance.csv'):
    #Save results to CSV
    import csv
    
    sorted_scores = sorted(importance_scores, key=lambda x: x['importance'], reverse=True)
    
    with open(filename, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['rank', 'feature', 'importance', 'baseline_winrate', 'permuted_winrate', 'drop_pct'])
        writer.writeheader()
        
        for rank, score in enumerate(sorted_scores, 1):
            writer.writerow({
                'rank': rank,
                'feature': score['feature'],
                'importance': score['importance'],
                'baseline_winrate': score['baseline'],
                'permuted_winrate': score['permuted'],
                'drop_pct': score['importance'] * 100
            })
    
    print(f"\nResults saved to {filename}")


def main():
    import time
    
    model_path = 'models/dqn_multi_opp.keras'
    
    print("="*70)
    print("PERMUTATION FEATURE IMPORTANCE ANALYSIS")
    print("="*70)
    print(f"Model: {model_path}")
    print(f"Method: Permutation (randomize each feature)\n")
    
    start_time = time.time()
    
    # Run analysis
    importance_scores, baseline = quick_permutation_importance(
        model_path,
        num_games=200  # increase for more accuracy
    )
    
    # Display results
    print_results(importance_scores, baseline)
    
    # Save to CSV
    save_to_csv(importance_scores)
    
    elapsed = time.time() - start_time
    print(f"\nAnalysis completed in {elapsed:.1f} seconds")


if __name__ == "__main__":
    main()
