// frontend/src/components/poker-action-panel.tsx
'use client';

import { Button } from '../components/ui/button';
import { Input } from '../components/ui/input';
import { PokerGame } from '@/domain/pokerGame';
import { Action } from '@/types';

interface PokerActionPanelProps {
  betAmount: number;
  currentPlayer: number;
  onAction: (type: Action['type']) => void;
  onBetChange: (amount: number) => void;
  game: PokerGame;
}

export function PokerActionPanel({ betAmount, currentPlayer, onAction, onBetChange, game }: PokerActionPanelProps) {
  const player = `P${currentPlayer + 1}`;
  const bigBlindSize = 40;

  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-bold text-yellow-300 drop-shadow-md">Actions</h2>
      <div className="grid grid-cols-3 gap-4">
        <Button
          className="btn-fold bg-gray-600 hover:bg-gray-500 text-white transition-all duration-200 hover:scale-105"
          onClick={() => onAction('fold')}
          disabled={!game.validateAction({ type: 'fold', player })}
        >
          Fold
        </Button>
        <Button
          className="btn-check bg-blue-600 hover:bg-blue-500 text-white transition-all duration-200 hover:scale-105"
          onClick={() => onAction('check')}
          disabled={!game.validateAction({ type: 'check', player })}
        >
          Check
        </Button>
        <Button
          className="btn-call bg-green-600 hover:bg-green-500 text-white transition-all duration-200 hover:scale-105"
          onClick={() => onAction('call')}
          disabled={!game.validateAction({ type: 'call', player })}
        >
          Call
        </Button>
        <Button
          className="btn-bet bg-yellow-600 hover:bg-yellow-500 text-white transition-all duration-200 hover:scale-105"
          onClick={() => onAction('bet')}
          disabled={!game.validateAction({ type: 'bet', player, amount: betAmount })}
        >
          Bet {betAmount}
        </Button>
        <Button
          className="btn-raise bg-yellow-600 hover:bg-yellow-500 text-white transition-all duration-200 hover:scale-105"
          onClick={() => onAction('raise')}
          disabled={!game.validateAction({ type: 'raise', player, amount: betAmount })}
        >
          Raise {betAmount}
        </Button>
        <Button
          className="btn-allin bg-red-600 hover:bg-red-500 text-white transition-all duration-200 hover:scale-105"
          onClick={() => onAction('allin')}
          disabled={!game.validateAction({ type: 'allin', player })}
        >
          ALL IN
        </Button>
      </div>
      <div className="flex items-center gap-4">
        <Button
          className="btn-adjust bg-gray-600 hover:bg-gray-500 text-white w-12 h-12 flex items-center justify-center transition-all duration-200 hover:scale-110"
          onClick={() => onBetChange(Math.max(20, betAmount - bigBlindSize))}
        >
          -
        </Button>
        <Input
          type="number"
          value={betAmount}
          readOnly
          className="w-24 text-center bg-gray-700 border-green-500 text-white placeholder-gray-400 focus:ring-2 focus:ring-green-400"
        />
        <Button
          className="btn-adjust bg-gray-600 hover:bg-gray-500 text-white w-12 h-12 flex items-center justify-center transition-all duration-200 hover:scale-110"
          onClick={() => onBetChange(betAmount + bigBlindSize)}
        >
          +
        </Button>
      </div>
    </div>
  );
}