import React, { useState, useEffect, useRef } from 'react';
import { generateText, findClosestWord } from '../app/api/checkWord';

interface Word {
  word: string;
  definition: string;
  word_embedding: number[];
  definition_embedding: number[];
}


interface GameProps {
  words: Word[];
  onPositionUpdate: (distances: number[]) => void;
  onTextGenerated: (text: string) => void;
  onClosestWordFound: (word: string, definition: string) => void;
}

const Game: React.FC<GameProps> = ({ words, onPositionUpdate, onTextGenerated, onClosestWordFound }) => {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [dragPoint, setDragPoint] = useState({ x: 0, y: 0 });
  const [isDragging, setIsDragging] = useState(false);

  const calculateWordPositions = () => {
    const radius = 150;
    const center = { x: 200, y: 200 };
    return words.map((_, index) => {
      const angle = (index * 2 * Math.PI) / words.length;
      return {
        x: center.x + radius * Math.cos(angle),
        y: center.y + radius * Math.sin(angle)
      };
    });
  };

  const calculateWeightedEmbedding = (distances: number[]) => {
    console.log("Distances:", distances);
    // Convert distances to weights (closer = higher weight)
    const maxDistance = Math.max(...distances);
    const weights = distances.map(d => 1 - (d / maxDistance));
    const totalWeight = weights.reduce((sum, w) => sum + w, 0);
    
    // Normalize weights
    const normalizedWeights = weights.map(w => w / totalWeight);
    
    // Calculate weighted average of embeddings
    const embeddingLength = words[0].word_embedding.length;
    const weightedEmbedding = new Array(embeddingLength).fill(0);
    
    for (let i = 0; i < words.length; i++) {
      const embedding = words[i].word_embedding;
      const weight = normalizedWeights[i];
      
      for (let j = 0; j < embeddingLength; j++) {
        weightedEmbedding[j] += embedding[j] * weight;
      }
    }
    
    console.log("Weighted embedding:", weightedEmbedding);
    return weightedEmbedding;
  };

  useEffect(() => {
    setDragPoint({ x: 200, y: 200 });
  }, [words]);

  // Handle canvas drawing
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    ctx.clearRect(0, 0, canvas.width, canvas.height);

    const wordPositions = calculateWordPositions();
    wordPositions.forEach((pos, index) => {
      ctx.font = '16px Arial';
      ctx.fillStyle = 'black';
      ctx.fillText(words[index].word, pos.x - 30, pos.y);  // Access the word property
    });

    ctx.beginPath();
    ctx.arc(dragPoint.x, dragPoint.y, 8, 0, 2 * Math.PI);
    ctx.fillStyle = 'black';
    ctx.fill();
  }, [words, dragPoint]);

  const handleMouseDown = (e: React.MouseEvent) => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    
    const rect = canvas.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    
    const dx = x - dragPoint.x;
    const dy = y - dragPoint.y;
    if (dx * dx + dy * dy < 64) { // 8^2 radius
      setIsDragging(true);
    }
  };

  const handleMouseMove = (e: React.MouseEvent) => {
    if (!isDragging) return;
    
    const canvas = canvasRef.current;
    if (!canvas) return;
    
    const rect = canvas.getBoundingClientRect();
    const newX = Math.max(0, Math.min(400, e.clientX - rect.left));
    const newY = Math.max(0, Math.min(400, e.clientY - rect.top));
    
    setDragPoint({ x: newX, y: newY });
    
    const wordPositions = calculateWordPositions();
    const distances = wordPositions.map(pos => {
      const dx = pos.x - newX;
      const dy = pos.y - newY;
      return Math.sqrt(dx * dx + dy * dy);
    });
    onPositionUpdate(distances);
  };

  const handleMouseUp = async () => {
    if (isDragging) {
        const wordPositions = calculateWordPositions();
        const distances = wordPositions.map(pos => {
            const dx = pos.x - dragPoint.x;
            const dy = pos.y - dragPoint.y;
            return Math.sqrt(dx * dx + dy * dy);
        });
        
        const weightedEmbedding = calculateWeightedEmbedding(distances);
        
        try {
            const [textResponse, closestWordResponse] = await Promise.all([
                generateText(weightedEmbedding),
                findClosestWord(weightedEmbedding)
            ]);
            
            if (onTextGenerated) {
                onTextGenerated(textResponse.text);
            }
            if (onClosestWordFound) {
                onClosestWordFound(closestWordResponse.word, closestWordResponse.definition);
            }
        } catch (error) {
            console.error('Error:', error);
        }
    }
    setIsDragging(false);
};

  return (
    <div>
      <canvas
        ref={canvasRef}
        width={400}
        height={400}
        onMouseDown={handleMouseDown}
        onMouseMove={handleMouseMove}
        onMouseUp={handleMouseUp}
        onMouseLeave={handleMouseUp}
        style={{ border: '1px solid black' }}
      />
    </div>
  );
};

export default Game;