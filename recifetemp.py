def get_recife_weather_status():
    """Simulates getting current weather status for Recife."""
    temperatures = [25, 26, 27, 28, 29, 30]
    humidity = [70, 75, 80, 85, 90]
    conditions = ["Ensolarado", "Parcialmente Nublado", "Nublado com Pancadas de Chuva"]

    current_temp = random.choice(temperatures) + random.uniform(0, 1)
    current_humidity = random.choice(humidity)
    current_condition = random.choice(conditions)

    return current_temp, current_humidity, current_condition

def display_weather_info():
    """Displays current weather information for Recife."""
    current_date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    temp, humidity, condition = get_recife_weather_status()

    print(f"--- Clima em Recife - {current_date} ---")
    print(f"Temperatura: {temp:.1f}°C")
    print(f"Umidade: {humidity}%")
    print(f"Condição: {condition}")
    print("---------------------------------------")

if _name_ == "_main_":
    display_weather_info()