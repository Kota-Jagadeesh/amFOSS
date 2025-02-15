document.getElementById("getWeather").addEventListener("click", async () => {
    const location = document.getElementById("location").value;
    const weatherInfoDiv = document.getElementById("weatherInfo");
    
    if (!location) {
      weatherInfoDiv.textContent = "Please enter a location.";
      return;
    }
  
    weatherInfoDiv.textContent = "Fetching weather data...";
  
    try {
      const apiKey = "82e5ae004a72c3ebd47df74e5a8c24f2";
      const response = await fetch(`https://api.openweathermap.org/data/2.5/weather?q=${location}&units=metric&appid=${apiKey}`);
      const data = await response.json();
  
      if (data.cod === 200) {
        weatherInfoDiv.innerHTML = `
          <p><strong>Location:</strong> ${data.name}, ${data.sys.country}</p>
          <p><strong>Temperature:</strong> ${data.main.temp}°C</p>
          <p><strong>Weather:</strong> ${data.weather[0].description}</p>
          <p><strong>Humidity:</strong> ${data.main.humidity}%</p>
        `;
      } else {
        weatherInfoDiv.textContent = "Location not found. Please try again.";
      }
    } catch (error) {
      weatherInfoDiv.textContent = "Error fetching weather data. Try again later.";
    }
});

