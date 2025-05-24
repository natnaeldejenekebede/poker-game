// // frontend/src/tests/pokerGame.test.tsx
// import { render, screen, fireEvent } from '@testing-library/react';
// import PokerGameApp from '../app/page';
// import { PokerGame } from '../domain/pokerGame';

// jest.mock('../services/apiService', () => ({
//   createHand: jest.fn(),
//   getHands: jest.fn(() => Promise.resolve([])),
// }));

// describe('PokerGameApp', () => {
//   test('renders and handles reset', () => {
//     render(<PokerGameApp />);
//     const startButton = screen.getByText('Start');
//     fireEvent.click(startButton);
//     expect(screen.getByText('Reset')).toBeInTheDocument();
//     expect(screen.getByText('Player 1 is dealt')).toBeInTheDocument();
//   });

//   test('disables invalid actions', () => {
//     render(<PokerGameApp />);
//     const checkButton = screen.getByText('Check');
//     expect(checkButton).toBeDisabled();

//     const callButton = screen.getByText('Call');
//     expect(callButton).toBeDisabled();
//   });
// });