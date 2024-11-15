export const getRandomWord = async () => {
    const response = await fetch('http://localhost:8000/get_random_word');
    return response.json();
};