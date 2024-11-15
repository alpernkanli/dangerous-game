import React, { useState } from 'react';

interface GameProps {
  word: string;
  description: string;
  onCheckWord: (tweakedDescription: string) => void;
}

const Game: React.FC<GameProps> = ({ word, description, onCheckWord }) => {
  const [tweakedDescription, setTweakedDescription] = useState<string>('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onCheckWord(tweakedDescription);
  };

  return (
    <div>
      <h1>Word: {word}</h1>
      <p>Description: {description}</p>
      <form onSubmit={handleSubmit}>
        <input
          title="Description"
          placeholder='Description'
          type="text"
          value={tweakedDescription}
          onChange={(e) => setTweakedDescription(e.target.value)}
        />
        <button type="submit">Submit</button>
      </form>
    </div>
  );
};

export default Game;