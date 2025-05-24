export interface Player {
  id: string; // Changed to string to match "P1", "P2", etc.
  stack: number;
  cards: string[];
}

export interface Action {
  type: 'fold' | 'check' | 'call' | 'bet' | 'raise' | 'allin';
  player: string;
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

export interface Hand {
  id: string;
  stacks: number[] | string; // Allow JSON string or parsed array
  player_cards: string[][] | string; // Allow JSON string or parsed array of arrays
  action_sequence: Action[] | string; // Renamed "actions" to "action_sequence" to match backend
  winnings: { [key: string]: number } | string; // Allow JSON string or parsed object
  dealer_position: number;
  small_blind_position: number;
  big_blind_position: number;
  created_at?: string; // Added to match backend response
}