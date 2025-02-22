module cryptonian_games::game_rewards {
    use std::string;
    use std::string::String;
    use std::vector;
    use aptos_framework::signer;
    use aptos_framework::coin;
    use aptos_framework::timestamp;
    use aptos_framework::aptos_coin::AptosCoin;

    // Errors
    const ENOT_AUTHORIZED: u64 = 1;
    const EINVALID_GAME: u64 = 2;
    const EINVALID_REWARD: u64 = 3;

    // Game types
    const PUZZLE_GAME: vector<u8> = b"PUZZLE_NFT_GAME";
    const MINESWEEPER_GAME: vector<u8> = b"MINESWEEPER";

    // Reward types
    const TOKEN_REWARD: u64 = 1;
    const NFT_REWARD: u64 = 2;

    struct GameReward has key {
        game_name: String,
        reward_type: u64,
        reward_amount: u64,
        timestamp: u64,
    }

    struct PlayerStats has key {
        total_rewards: u64,
        games_completed: u64,
        nfts_minted: u64,
        last_reward_time: u64,
    }

    struct NFTCollection has key {
        nfts: vector<NFT>,
    }

    struct NFT has store {
        id: u64,
        name: String,
        game: String,
        rarity: u64,
        metadata: String,
    }

    /// Initializes the player's stats and NFT collection
    public fun initialize(account: &signer) {
        let account_addr = signer::address_of(account);
        assert!(account_addr == @cryptonian_games, ENOT_AUTHORIZED);
        
        if (!exists<PlayerStats>(account_addr)) {
            move_to(account, PlayerStats {
                total_rewards: 0,
                games_completed: 0,
                nfts_minted: 0,
                last_reward_time: 0,
            });
        };

        if (!exists<NFTCollection>(account_addr)) {
            move_to(account, NFTCollection {
                nfts: vector::empty<NFT>(),
            });
        };
    }

        /// Rewards a player for completing a game
    public entry fun reward_player(
        account: &signer,
        game_name: String,
        reward_type: u64,
        reward_amount: u64,
    ) acquires PlayerStats {
        let player_address = signer::address_of(account);
        
        // Verify game name
        assert!(
            game_name == string::utf8(PUZZLE_GAME) || 
            game_name == string::utf8(MINESWEEPER_GAME),
            EINVALID_GAME
        );

        // Update player stats
        let stats = borrow_global_mut<PlayerStats>(player_address);
        stats.games_completed = stats.games_completed + 1;
        stats.total_rewards = stats.total_rewards + reward_amount;
        stats.last_reward_time = timestamp::now_seconds();

        // Create reward record
        move_to(account, GameReward {
            game_name,
            reward_type,
            reward_amount,
            timestamp: timestamp::now_seconds(),
        });

        // Distribute rewards
        if (reward_type == TOKEN_REWARD) {
            coin::transfer<AptosCoin>(account, player_address, reward_amount);
        };
    }

    /// Mints an NFT for the player
    public entry fun mint_nft(
        account: &signer,
        name: String,
        game: String,
        rarity: u64,
        metadata: String,
    ) acquires NFTCollection, PlayerStats {
        let player_address = signer::address_of(account);

        let collection = borrow_global_mut<NFTCollection>(player_address);
        let stats = borrow_global_mut<PlayerStats>(player_address);
        
        let nft = NFT {
            id: stats.nfts_minted + 1,
            name,
            game,
            rarity,
            metadata,
        };

        vector::push_back(&mut collection.nfts, nft);
        stats.nfts_minted = stats.nfts_minted + 1;
    }

    /// Retrieves player statistics
    public fun get_player_stats(player: address): (u64, u64, u64) acquires PlayerStats {
        let stats = borrow_global<PlayerStats>(player);
        (stats.total_rewards, stats.games_completed, stats.nfts_minted)
    }
}
