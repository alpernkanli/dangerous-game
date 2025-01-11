export const getRandomWord = async () => {
    const response = await fetch('http://localhost:8000/api/v1/random-word');
    return response.json();
};

export const getRandomWords = async (n: number) => {
    const response = await fetch(`http://localhost:8000/api/v1/random-words?n=${n}`);
    return response.json();
};
