// frontend/src/domain/pokerGame.ts
import { Player, Action } from '../types';

export class PokerGame {
  players: Player[] = Array.from({ length: 6 }, (_, i) => ({
    id: i.toString(),  // Changed from i to i.toString() to match Player.id: string
    stack: 10000,
    cards: [] as string[],  // Explicitly typed as string[] to avoid never[]
  }));
  pot: number = 0;
  currentPlayerIndex: number = 2; // Start after big blind
  currentRound: 'preflop' | 'flop' | 'turn' | 'river' | 'complete' = 'preflop';
  board: string[] = [];
  actions: Action[] = [];

  reset() {
    this.players.forEach(p => {
      p.stack = 10000;
      p.cards = [] as string[];
    });
    this.pot = 0;
    this.currentPlayerIndex = 2;
    this.currentRound = 'preflop';
    this.board = [];
    this.actions = [];
    // Simulate dealing cards (random for simplicity)
    const suits = ['c', 'd', 'h', 's'];
    const ranks = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A'];
    this.players.forEach(p => {
      p.cards = Array.from({ length: 2 }, () =>
        ranks[Math.floor(Math.random() * ranks.length)] +
        suits[Math.floor(Math.random() * suits.length)]
      );
    });
  }

  validateAction(action: Action): boolean {
    const { type, amount } = action;
    const player = this.players[this.currentPlayerIndex];
    if (!player) return false;

    switch (type) {
      case 'fold':
      case 'check':
        return true;
      case 'call':
        return this.actions.length > 0 && this.actions.some(a => a.amount);
      case 'bet':
      case 'raise':
        return amount !== undefined && amount >= 40 && player.stack >= amount;
      case 'allin':
        return player.stack > 0;
      default:
        return false;
    }
  }

  applyAction(action: Action) {
    const player = this.players[this.currentPlayerIndex];
    if (this.validateAction(action)) {
      switch (action.type) {
        case 'fold':
          player.cards = [] as string[];
          break;
        case 'check':
        case 'call':
          break;
        case 'bet':
        case 'raise':
        case 'allin':
          if (action.amount) {
            this.pot += action.amount;
            player.stack -= action.amount;
          }
          break;
      }
      this.actions.push(action);
      this.currentPlayerIndex = (this.currentPlayerIndex + 1) % 6;
      if (this.currentPlayerIndex === 2 && this.actions.length > 6) {
        this.nextRound();
      }
    }
  }

  nextRound() {
    if (this.currentRound === 'preflop' && this.actions.length > 6) {
      this.currentRound = 'flop';
      this.board = this.dealBoard(3);
    } else if (this.currentRound === 'flop') {
      this.currentRound = 'turn';
      this.board.push(this.dealBoard(1)[0]);
    } else if (this.currentRound === 'turn') {
      this.currentRound = 'river';
      this.board.push(this.dealBoard(1)[0]);
    } else if (this.currentRound === 'river') {
      this.currentRound = 'complete';
    }
  }

  dealBoard(count: number): string[] {
    const suits = ['c', 'd', 'h', 's'];
    const ranks = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A'];
    return Array.from({ length: count }, () =>
      ranks[Math.floor(Math.random() * ranks.length)] +
      suits[Math.floor(Math.random() * suits.length)]
    );
  }
}