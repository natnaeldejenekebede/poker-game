'use client';

import { useState, useEffect, useCallback } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from './components/ui/card';
import { Input } from './components/ui/input';
import { Button } from './components/ui/button';
import { ScrollArea } from './components/ui/scroll-area';
import { PokerActionPanel } from './components/poker-action-panel';
import { PokerGame } from '../domain/pokerGame';
import { createHand, getHands } from '../services/apiService';
import { Player, Hand, Action, HandData } from '@/types';

export default function PokerGameApp() {
  const [game] = useState(() => new PokerGame());
  const [players, setPlayers] = useState<Player[]>(game.players);
  const [actionLog, setActionLog] = useState<string[]>([]);
  const [handHistory, setHandHistory] = useState<Hand[]>([]);
  const [betAmount, setBetAmount] = useState(20);
  const [currentPlayer, setCurrentPlayer] = useState(2);
  const [isStarted, setIsStarted] = useState(false);
  const [loading, setLoading] = useState(true); // Added loading state
  const [error, setError] = useState<string | null>(null); // Added error state

  const resetGame = useCallback(() => {
    game.reset();
    const initialLog = [
      `Player 1 is dealt ${game.players[0].cards.join('')}`,
      `Player 2 is dealt ${game.players[1].cards.join('')}`,
      `Player 3 is dealt ${game.players[2].cards.join('')}`,
      `Player 4 is dealt ${game.players[3].cards.join('')}`,
      `Player 5 is dealt ${game.players[4].cards.join('')}`,
      `Player 6 is dealt ${game.players[5].cards.join('')}`,
      `---`,
      `Player 3 is the dealer`,
      `Player 4 posts small blind - 20 chips`,
      `Player 5 posts big blind - 40 chips`,
    ];
    setPlayers([...game.players]);
    setActionLog(initialLog);
    setCurrentPlayer(2);
    setIsStarted(true);
  }, [game]);

  const handleAction = useCallback(
    async (actionType: Action['type']) => {
      try {
        const action: Action = {
          type: actionType,
          player: `P${currentPlayer + 1}`,
          amount: ['bet', 'raise'].includes(actionType) ? betAmount : undefined,
        };

        if (game.validateAction(action)) {
          game.applyAction(action);
          const logMessage = `Player ${currentPlayer + 1} ${
            action.type
          }${action.amount ? ` to ${action.amount} chips` : ''}`;
          setActionLog((prev) => [...prev, logMessage]);
          setPlayers([...game.players]);
          setCurrentPlayer(game.currentPlayerIndex);

          if (game.currentRound === 'complete' || game.players.filter(p => p.cards.length > 0).length <= 1) {
            const handId = Math.random().toString(36).substring(2, 15);
            const finalLog = `Hand #${handId} ended\nFinal pot was ${game.pot}`;
            setActionLog((prev) => [...prev, logMessage, finalLog]);
            await saveHand();
          }
        }
      } catch (err) {
        console.error('Error handling action:', err);
        setError('Failed to process action. Please try again.');
      }
    },
    [game, currentPlayer, betAmount]
  );

  const saveHand = async () => {
    try {
      const handData: HandData = {
        stacks: players.map(p => p.stack),
        player_cards: players.map(p => p.cards),
        actions: actionLog
          .slice(6)
          .map(log => {
            const parts = log.split(' ');
            if (parts.length >= 2 && parts[1].match(/fold|check|call|bet|raise|allin/)) {
              return {
                type: parts[1] as Action['type'],
                player: parts[0],
                amount: parts[3] ? parseInt(parts[3]) : undefined,
              } as Action;
            }
            return null;
          })
          .filter((a): a is Action => a !== null),
        dealer_position: 2, // Player 3
        small_blind_position: 3, // Player 4
        big_blind_position: 4, // Player 5
      };
      await createHand(handData);
      await fetchHandHistory();
    } catch (err) {
      console.error('Error saving hand:', err);
      setError('Failed to save hand. Please try again.');
    }
  };

  const fetchHandHistory = async () => {
    try {
      setLoading(true);
      const hands = await getHands();
      setHandHistory(hands);
    } catch (err) {
      console.error('Error fetching hand history:', err);
      setError('Failed to load hand history. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const runTestGame = () => {
    resetGame();
    handleAction('bet');
    handleAction('call');
    handleAction('fold');
    handleAction('check');
    console.log('E2E Test: Game state updated successfully');
  };

  useEffect(() => {
    fetchHandHistory();
  }, []);

  if (loading) {
    return (
      <div className="container min-h-screen bg-gradient-to-br from-green-800 to-green-900 text-white font-sans flex items-center justify-center">
        <p className="text-2xl">Loading...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="container min-h-screen bg-gradient-to-br from-green-800 to-green-900 text-white font-sans flex items-center justify-center">
        <p className="text-2xl text-red-400">{error}</p>
      </div>
    );
  }

  return (
    <div className="container min-h-screen bg-gradient-to-br from-green-800 to-green-900 text-white font-sans">
      <header className="py-4 bg-green-700/80 shadow-lg">
        <h1 className="text-4xl font-extrabold text-center text-yellow-300 drop-shadow-lg animate-pulse">Texas Hold&apos;em Poker</h1>
      </header>
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 p-6">
        {/* Playing Field Log (Left Column) */}
        <div className="space-y-8">
          {/* Setup */}
          <Card className="bg-gray-800/90 border-green-600 shadow-xl hover:shadow-2xl transition-shadow">
            <CardHeader className="bg-green-600/50">
              <CardTitle className="text-2xl font-bold text-yellow-200">Setup</CardTitle>
            </CardHeader>
            <CardContent className="p-6">
              <div className="flex items-center gap-4 mb-4">
                <span className="text-lg text-gray-300">Stacks</span>
                <Input
                  type="number"
                  value={players[0].stack}
                  onChange={(e) => {
                    const newPlayers = [...players];
                    const stack = parseInt(e.target.value) || 10000;
                    newPlayers.forEach(p => (p.stack = stack));
                    setPlayers(newPlayers);
                  }}
                  className="w-32 bg-gray-700 border-green-500 text-white placeholder-gray-400 focus:ring-2 focus:ring-green-400"
                  placeholder="10000"
                />
                <Button
                  variant="outline"
                  className="btn-fold border-green-500 hover:bg-gray-600"
                  onClick={() => setPlayers(players.map(p => ({ ...p, stack: 10000 })))}
                >
                  Apply
                </Button>
                <Button
                  variant={isStarted ? 'destructive' : 'default'}
                  className={isStarted ? 'btn-allin hover:bg-red-700' : 'bg-green-600 hover:bg-green-700 transition-all duration-200'}
                  onClick={resetGame}
                >
                  {isStarted ? 'Reset' : 'Start'}
                </Button>
                {/* Added button for manual test */}
                <Button
                  variant="secondary"
                  className="bg-blue-600 hover:bg-blue-700"
                  onClick={runTestGame}
                >
                  Run Test Game
                </Button>
              </div>
            </CardContent>
          </Card>

          {/* Actions */}
          <Card className="bg-gray-800/90 border-green-600 shadow-xl hover:shadow-2xl transition-shadow">
            <CardContent className="p-6">
              <PokerActionPanel
                betAmount={betAmount}
                currentPlayer={currentPlayer}
                onAction={handleAction}
                onBetChange={setBetAmount}
                game={game}
              />
            </CardContent>
          </Card>

          {/* Play Log */}
          <Card className="bg-gray-800/90 border-green-600 shadow-xl hover:shadow-2xl transition-shadow">
            <CardHeader className="bg-green-600/50">
              <CardTitle className="text-2xl font-bold text-yellow-200">Play Log</CardTitle>
            </CardHeader>
            <CardContent className="p-4">
              <ScrollArea className="h-72 rounded-lg border-green-600 bg-gray-900/70">
                {actionLog.map((log, index) => (
                  <p
                    key={index}
                    className={`text-base ${log.includes('Hand #') ? 'font-bold text-yellow-400' : 'text-gray-200'} py-1`}
                  >
                    {log}
                  </p>
                ))}
              </ScrollArea>
            </CardContent>
          </Card>
        </div>

        {/* Hand History (Right Column) */}
        <Card className="bg-gray-800/90 border-green-600 shadow-xl hover:shadow-2xl transition-shadow">
          <CardHeader className="bg-green-600/50">
            <CardTitle className="text-2xl font-bold text-yellow-200">Hand History</CardTitle>
          </CardHeader>
          <CardContent className="p-4">
         <ScrollArea className="h-[calc(100vh-400px)] rounded-lg border-green-600 bg-gray-900/70">
              {handHistory.length > 0 ? (
                handHistory.map(hand => {
                  const actions = hand.action_sequence || []; // Use action_sequence
                  const actionSeq = Array.isArray(actions)
                    ? actions
                        .map((a: Action) =>
                          a && a.type
                            ? a.amount
                             ? `${a.type[0]}${a.amount}`
                              : a.type === 'fold'
                              ? 'f'
                              : a.type === 'check'
                              ? 'x'
                              : a.type === 'call'
                              ? 'c'
                              : 'allin'
                            : ''
                        )
                        .filter(Boolean)
                        .join(':')
                    : '';
                  const board = game.board.join(' ');
                  const fullActionSeq = `fff:${actionSeq}:${board}`;
                  const playerCards = hand.player_cards || [];
                  const winnings = hand.winnings || {};

                  return (
                    <div key={hand.id} className="mb-6 p-4 bg-green-800/50 rounded-lg hover:bg-green-700/50 transition-colors">
                      <p className="text-xl font-semibold text-yellow-400">Hand #{hand.id}</p>
                      <p className="text-gray-200 mt-2">
                        Stack 10000; Dealer: P{hand.dealer_position + 1}; P{hand.small_blind_position + 1} Small Blind; P{hand.big_blind_position + 1} Big Blind
                      </p>
                      <p className="text-gray-200 mt-2">
                        Hands: {Array.isArray(playerCards)
                          ? playerCards.map((cards: string[], i: number) => `P${i + 1}: ${Array.isArray(cards) ? cards.join(' ') : cards}`).join(', ')
                          : String(playerCards)}
                      </p>
                      <p className="text-gray-200 mt-2">Actions: {fullActionSeq}</p>
                      <p className="text-gray-200 mt-2">
                        Winnings: {Object.entries(winnings).map(([player, amount]) => `${player}: ${Number(amount) > 0 ? '+' : ''}${amount}`).join(', ')}
                      </p>
                    </div>
                  );
                })
              ) : (
                <p className="text-gray-400 p-4">No hands in history yet.</p>
              )}
            </ScrollArea>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}