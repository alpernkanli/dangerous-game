'use client';

import React, { useState, useEffect } from 'react';
import Game from '../components/Game';
import Score from '../components/Score';
import { getRandomWord } from './api/randomWord';
import { checkWord } from './api/checkWord';

interface WordData {
  word: string;
  description: string;
}

const Home: React.FC = () => {
  const [word, setWord] = useState<string>('');
  const [description, setDescription] = useState<string>('');
  const [score, setScore] = useState<number>(0);

  useEffect(() => {
    fetchRandomWord();
  }, []);

  const fetchRandomWord = async () => {
    const data: WordData = await getRandomWord();
    setWord(data.word);
    setDescription(data.description);
  };

  const handleCheckWord = async (tweakedDescription: string) => {
    const isCorrect: boolean = await checkWord(tweakedDescription);
    if (isCorrect) {
      setScore(score + 1);
      fetchRandomWord();
    }
  };

  return (
    <div>
      <Game word={word} description={description} onCheckWord={handleCheckWord} />
      <Score score={score} />
    </div>
  );
};

export default Home;