// frontend/src/types/index.ts
export interface Player {
  id: string; // e.g., "P1"
  stack: number;
  cards: string[];
}

export interface Hand {
  actions: Action[];
  id: string;
  stacks: Record<string, number>;
  dealer_position: number;
  small_blind_position: number;
  big_blind_position: number;
  player_cards: Record<string, string[]>;
  action_sequence: string;
  winnings: Record<string, number>;
  created_at: string;
}

export interface Action {
  type: 'fold' | 'check' | 'call' | 'bet' | 'raise' | 'allin';
  player: string; // Make player required where action is valid
  amount?: number;
}

export interface HandData {
  stacks: number[];
  player_cards: string[][];
  actions: Action[];
  dealer_position: number;
  small_blind_position: number;
  big_blind_position: number;
}