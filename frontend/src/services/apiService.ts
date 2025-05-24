import axios from 'axios';
import { Hand, HandData } from '@/types';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

interface AxiosLikeError {
  isAxiosError?: boolean;
  response?: {
    data?: {
      detail?: string;
    };
  };
}

const isAxiosError = (error: unknown): error is AxiosLikeError => {
  return (error as AxiosLikeError).isAxiosError === true;
};

export const createHand = async (handData: HandData): Promise<string> => {
  try {
    const response = await axios.post<{ id: string }>(`${API_URL}/hands/create`, handData, {
      headers: {
        'Content-Type': 'application/json',
      },
    });
    return response.data.id;
  } catch (error) {
    console.error('Error creating hand:', error);
    if (isAxiosError(error)) {
      throw new Error(error.response?.data?.detail || 'Failed to create hand');
    }
    throw new Error('Failed to create hand');
  }
};

export const getHands = async (limit: number = 100, offset: number = 0): Promise<Hand[]> => {
  try {
    const response = await axios.get<Hand[]>(`${API_URL}/hands/`, {
      params: { limit, offset },
    });
    // Parse JSON strings in the response
    return response.data.map(hand => ({
      ...hand,
      stacks: typeof hand.stacks === 'string' ? JSON.parse(hand.stacks) : hand.stacks,
      player_cards: typeof hand.player_cards === 'string' ? JSON.parse(hand.player_cards) : hand.player_cards,
      action_sequence: typeof hand.action_sequence === 'string' ? JSON.parse(hand.action_sequence) : hand.action_sequence,
      winnings: typeof hand.winnings === 'string' ? JSON.parse(hand.winnings) : hand.winnings,
    }));
  } catch (error) {
    console.error('Error fetching hands:', error);
    if (isAxiosError(error)) {
      throw new Error(error.response?.data?.detail || 'Failed to fetch hands');
    }
    throw new Error('Failed to fetch hands');
  }
};