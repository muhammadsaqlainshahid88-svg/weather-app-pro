# ============================================================
# 🌤️ WEATHER APP PRO (WeatherAPI Version)
# Full Professional Tkinter UI
# ============================================================

import tkinter as tk
from tkinter import messagebox
import requests
import threading
from datetime import datetime

# ============================================================
# 🔑 CONFIG
# ============================================================
API_KEY = "your_api_key_here"
BASE_URL = "http://api.weatherapi.com/v1"

# ============================================================
# 🌈 WEATHER ICONS
# ============================================================
def get_emoji(condition):
    condition = condition.lower()
    if "sun" in condition or "clear" in condition:
        return "☀️"
    elif "cloud" in condition:
        return "☁️"
    elif "rain" in condition:
        return "🌧️"
    elif "storm" in condition or "thunder" in condition:
        return "⛈️"
    elif "snow" in condition:
        return "❄️"
    else:
        return "🌡️"

# ============================================================
# 🌐 API CALL
# ============================================================
def fetch_weather(city, country):
    url = f"{BASE_URL}/forecast.json"
    params = {
        "key": API_KEY,
        "q": f"{city},{country}",
        "days": 7
    }
    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    return response.json()

# ============================================================
# 🖼️ APP CLASS
# ============================================================
class WeatherApp:

    def __init__(self, root):
        self.root = root
        self.root.title("🌤️ Weather App Pro")
        self.root.geometry("750x650")
        self.root.config(bg="#0f172a")

        self.build_ui()

    # ================= UI =================
    def build_ui(self):

        # Title
        tk.Label(
            self.root,
            text="🌤️ Weather App Pro",
            font=("Segoe UI", 22, "bold"),
            bg="#0f172a",
            fg="#38bdf8"
        ).pack(pady=15)

        # Input Card
        card = tk.Frame(self.root, bg="#1e293b", padx=20, pady=20)
        card.pack(padx=20, pady=10, fill="x")

        # Country
        tk.Label(card, text="Country", bg="#1e293b", fg="white").pack(anchor="w")
        self.country_entry = tk.Entry(card, font=("Segoe UI", 12))
        self.country_entry.pack(fill="x", pady=5)

        # City
        tk.Label(card, text="City", bg="#1e293b", fg="white").pack(anchor="w")
        self.city_entry = tk.Entry(card, font=("Segoe UI", 12))
        self.city_entry.pack(fill="x", pady=5)

        # Button
        tk.Button(
            card,
            text="Get Weather",
            bg="#38bdf8",
            fg="black",
            font=("Segoe UI", 11, "bold"),
            command=self.start_thread
        ).pack(pady=10)

        # Status
        self.status = tk.Label(
            self.root,
            text="Enter city and country",
            bg="#0f172a",
            fg="#94a3b8"
        )
        self.status.pack()

        # Result Box
        self.result = tk.Text(
            self.root,
            height=20,
            bg="#020617",
            fg="white",
            font=("Consolas", 11)
        )
        self.result.pack(padx=20, pady=15, fill="both", expand=True)

    # ================= THREAD =================
    def start_thread(self):
        threading.Thread(target=self.get_weather, daemon=True).start()

    # ================= MAIN LOGIC =================
    def get_weather(self):
        city = self.city_entry.get().strip()
        country = self.country_entry.get().strip()

        if not city or not country:
            messagebox.showwarning("Input Error", "Enter both city and country")
            return

        self.status.config(text="Fetching data...")

        try:
            data = fetch_weather(city, country)

            current = data["current"]
            forecast = data["forecast"]["forecastday"]

            emoji = get_emoji(current["condition"]["text"])

            # Clear old result
            self.result.delete(1.0, tk.END)

            # Current Weather
            self.result.insert(tk.END, f"{emoji} {city}, {country}\n\n")
            self.result.insert(tk.END, f"Temperature: {current['temp_c']}°C\n")
            self.result.insert(tk.END, f"Feels Like: {current['feelslike_c']}°C\n")
            self.result.insert(tk.END, f"Humidity: {current['humidity']}%\n")
            self.result.insert(tk.END, f"Wind: {current['wind_kph']} km/h\n")
            self.result.insert(tk.END, f"Condition: {current['condition']['text']}\n\n")

            # Forecast
            self.result.insert(tk.END, "7-Day Forecast:\n\n")

            for day in forecast:
                date = datetime.strptime(day["date"], "%Y-%m-%d").strftime("%A")
                min_temp = day["day"]["mintemp_c"]
                max_temp = day["day"]["maxtemp_c"]
                cond = day["day"]["condition"]["text"]
                emoji = get_emoji(cond)

                self.result.insert(
                    tk.END,
                    f"{date}: {emoji} {min_temp}°C / {max_temp}°C ({cond})\n"
                )

            self.status.config(text="✅ Done")

        except Exception as e:
            self.status.config(text="❌ Error")
            messagebox.showerror("Error", str(e))


# ============================================================
# 🚀 RUN APP
# ============================================================
if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop()
