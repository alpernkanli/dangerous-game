'use client';

import React, { useState, useEffect } from 'react';
import Game from '../components/Game';
import Score from '../components/Score';
import { getRandomWord, getRandomWords } from './api/randomWord';
import { checkWord } from './api/checkWord';

interface Word {
  word: string;
  definition: string;
  word_embedding: number[];
  definition_embedding: number[];
}

const Home: React.FC = () => {
  const [words, setWords] = useState<Word[]>([]);
  const [n, setN] = useState<number>(3); // Default number of words
  const [generatedText, setGeneratedText] = useState<string>("");
  const [closestWord, setClosestWord] = useState<{ word: string; definition: string } | null>(null);
  
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
      
      <Game 
        words={words} 
        onPositionUpdate={handlePositionUpdate}
        onTextGenerated={(text) => setGeneratedText(text)}
        onClosestWordFound={(word, definition) => setClosestWord({ word, definition })}
      />
      {generatedText && (
        <div>
          <h3>Generated Text:</h3>
          <p>{generatedText}</p>
        </div>
      )}
      {closestWord && (
        <div>
          <h3>Closest Word:</h3>
          <p>{closestWord.word}</p>
          <p>{closestWord.definition}</p>
        </div>
      )}
    </div>
  );
};

export default Home;