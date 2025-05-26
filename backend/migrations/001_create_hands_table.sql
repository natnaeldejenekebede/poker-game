DROP TABLE IF EXISTS hands;  -- Use with caution, backs up data first if needed
    CREATE TABLE hands (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        stacks JSONB NOT NULL,
        dealer_position INTEGER NOT NULL,
        small_blind_position INTEGER NOT NULL,
        big_blind_position INTEGER NOT NULL,
        player_cards JSONB NOT NULL,
        action_sequence JSONB NOT NULL,
        winnings JSONB NOT NULL,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
    );