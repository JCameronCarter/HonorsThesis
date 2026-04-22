#Test the trained DQN player against various opponents
from rl_player import DQNPlayer
from CantStop import (
    simulate_game,
    AdvancedAggressivePlayer,
    AdvancedCautiousPlayer,
    SmartRuleOf28Player,
    RuleOf28Player,
    DecentAggressivePlayer,
    DecentCautiousPlayer
)


def test_against_opponent(model_path, opponent, opponent_name, num_games=100):
    #Test DQN against a specific opponent
    print(f"\nTesting against {opponent_name}...")
    print("-" * 50)
    
    dqn = DQNPlayer(load_model=model_path, training=False)
    
    wins = 0
    for i in range(num_games):
        strategies = [dqn, opponent]
        winner = simulate_game(strategies, verbose=False)
        if winner == 0:
            wins += 1
        
        if (i + 1) % 20 == 0:
            print(f"  Progress: {i + 1}/{num_games} games, "
                  f"Win rate: {wins/(i+1):.1%}")
    
    win_rate = wins / num_games
    print(f"\n  Final: {wins}/{num_games} wins ({win_rate:.1%})")
    
    return win_rate


def main():
    model_path = 'models/dqn_multi_opp.keras'
    
    print("="*60)
    print(f"Testing DQN Model: {model_path}")
    print("="*60)
    
    # Test against multiple opponents
    opponents = [
        (AdvancedAggressivePlayer(), "AdvancedAggressivePlayer"),
        (AdvancedCautiousPlayer(), "AdvancedCautiousPlayer"),
        (SmartRuleOf28Player(), "SmartRuleOf28Player"),
        (RuleOf28Player(), "RuleOf28Player"),
        (DecentAggressivePlayer(), "DecentAggressivePlayer"),
        (DecentCautiousPlayer(), "DecentCautiousPlayer"),
    ]
    
    results = {}
    for opponent, name in opponents:
        win_rate = test_against_opponent(model_path, opponent, name, num_games=100)
        results[name] = win_rate
    
    # Print summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    for name, win_rate in results.items():
        print(f"{name:30s}: {win_rate:.1%}")
    
    avg_win_rate = sum(results.values()) / len(results)
    print(f"\n{'Average Win Rate':30s}: {avg_win_rate:.1%}")


if __name__ == "__main__":
    main()