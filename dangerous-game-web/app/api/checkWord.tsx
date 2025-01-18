export const checkWord = async (tweakedDescription: string) => {
    const response = await fetch('http://localhost:8000/api/v1/check_word', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ description: tweakedDescription }),
    });
    return response.json();
};

export const generateText = async (embedding: number[]) => {
  const response = await fetch('http://localhost:8000/api/v1/generate-text', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json',
      },
      body: JSON.stringify({
          embedding: embedding,
          model: "flan-t5"
      }),
  });
  return response.json();
};

export const findClosestWord = async (embedding: number[]) => {
  const response = await fetch('http://localhost:8000/api/v1/find-closest-word', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json',
      },
      body: JSON.stringify({
          embedding: embedding,
      }),
  });
  return response.json();
};