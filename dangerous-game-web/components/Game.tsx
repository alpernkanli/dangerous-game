import React, { useState, useEffect, useRef } from 'react';

interface GameProps {
  words: string[];
  onPositionUpdate: (distances: number[]) => void;
}

const Game: React.FC<GameProps> = ({ words, onPositionUpdate }) => {
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
      ctx.fillText(words[index], pos.x - 30, pos.y);
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

  const handleMouseUp = () => {
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