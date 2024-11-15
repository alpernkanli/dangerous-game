export const checkWord = async (tweakedDescription: string) => {
    const response = await fetch('http://localhost:8000/check_word', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ description: tweakedDescription }),
    });
    return response.json();
};