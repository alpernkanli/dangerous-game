'use client';

import React, { useState, useEffect } from 'react';
import Game from '../components/Game';
import Score from '../components/Score';
import { getRandomWord, getRandomWords } from './api/randomWord';
import { checkWord } from './api/checkWord';

const Home: React.FC = () => {
  const [words, setWords] = useState<string[]>([]);
  const [n, setN] = useState<number>(3); // Default number of words
  
  useEffect(() => {
    fetchRandomWords();
  }, [n]);

  const fetchRandomWords = async () => {
    const data = await getRandomWords(n);
    setWords(data);
  };

  const handlePositionUpdate = (distances: number[]) => {
    console.log('Distances to words:', distances);
  };

  return (
    <div className="container mx-auto p-4">
      <div className="mb-4">
        <label htmlFor="wordCount" className="mr-2">Number of words (2-8):</label>
        <input
          type="number"
          id="wordCount"
          min={2}
          max={8}
          value={n}
          onChange={(e) => setN(Math.min(8, Math.max(2, parseInt(e.target.value) || 2)))}
          className="border p-1"
        />
      </div>
      
      <Game words={words} onPositionUpdate={handlePositionUpdate} />
      <Score score={5} />
    </div>
  );
};

export default Home;