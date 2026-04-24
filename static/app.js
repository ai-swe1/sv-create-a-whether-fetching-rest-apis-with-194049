const API = window.location.origin;

window.addEventListener('load', async () => {
    try {
        const response = await fetch(`${API}/weather`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const weatherData = await response.json();
        console.log(weatherData);
        document.getElementById('temperature').innerText = `Temperature: ${weatherData.temperature}°C`;
        document.getElementById('humidity').innerText = `Humidity: ${weatherData.humidity}%`;
        document.getElementById('description').innerText = `Description: ${weatherData.description}`;
    } catch (error) {
        console.error('Error:', error);
        alert('Failed to fetch weather data. Please try again later.');
    }
});
