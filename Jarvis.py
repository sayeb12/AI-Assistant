import logging
import warnings
import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import requests
from transformers import pipeline, AutoTokenizer
from collections import defaultdict

# Suppress logging and warnings from Hugging Face Transformers

logging.getLogger("transformers.tokenization_utils_base").setLevel(logging.ERROR)
warnings.filterwarnings("ignore", category=UserWarning)

# OpenWeatherMap API Key (Replace with your own API key)
weather_api_key = 'YOUR_OPENWEATHERMAP_API_KEY'

listener = sr.Recognizer()
machine = pyttsx3.init()

def talk(text):
 machine.say(text)
 machine.runAndWait()

def input_instruction():
 global instruction
 try:
 with sr.Microphone() as origin:
 print('Listening...')
 speech = listener.listen(origin)
 instruction = listener.recognize_google(speech)
 instruction = instruction.lower()
 if 'jarvis' in instruction:
 instruction = instruction.replace('jarvis', "")
 print(instruction)
 except:
 pass
 return instruction

def get_weather(city):
 base_url = "http://api.openweathermap.org/data/2.5/weather?"
 complete_url = f"{base_url}q={city}&appid={weather_api_key}&units=metric"
 response = requests.get(complete_url)
 data = response.json()

 if data["cod"] == "404":
 return "City not found. Please try again with a different city name."

 # Check if 'weather' key is present and has data
 if 'weather' in data and len(data['weather']) > 0:
 weather_desc = data['weather'][0]['description']
 temp = data['main']['temp']
 humidity = data['main']['humidity']
 wind_speed = data['wind']['speed']
 report = f"The weather in {city} is {weather_desc}. " \
 f"The temperature is {temp}°C, humidity is {humidity}%, " \
 f"and wind speed is {wind_speed} m/s."
 return report
 else:
 return "Weather information not available for this city."

def speak_to_jarvis():
 talk("How can I help you?")
 instruction = input_instruction()
 print(instruction)
 if 'play' in instruction:
 song = instruction.replace('play', "")
 talk("Playing " + song)
 pywhatkit.playonyt(song)

 elif 'time' in instruction:
 time = datetime.datetime.now().strftime('%I:%M %p')
 talk('Current time is ' + time)

 elif 'date' in instruction:
 date = datetime.datetime.now().strftime('%d/%m/%Y')
 talk("Today's date is " + date)

 elif 'how are you' in instruction:
 talk('I am fine, how about you?')

 elif 'what is your name' in instruction:
 talk('I am Jarvis, What can I do for you?')

 elif 'who is' in instruction:
 human = instruction.replace('who is', "")
 info = wikipedia.summary(human, 1)
 print(info)
 talk(info)

 elif 'weather' in instruction:
 talk("Sure, please tell me the city name.")
 city = input_instruction() # Use speech recognition to get city name
 weather_report = get_weather(city)
 print(weather_report)
 talk(weather_report)

 else:
 talk('Please Repeat')

def graph_coloring(tasks, constraints):
 graph = defaultdict(list)
 for task, neighbors in constraints.items():
 for neighbor in neighbors:
 graph[task].append(neighbor)
 graph[neighbor].append(task)

 result = {}
 colors = {}
 for task in tasks:
 available_colors = set(range(len(tasks)))
 for neighbor in graph[task]:
 if neighbor in colors:
 available_colors.discard(colors[neighbor])
 if available_colors:
 chosen_color = min(available_colors)
 colors[task] = chosen_color
 result[task] = f"Time Slot {chosen_color + 1}"
 else:
 result[task] = "No available time slot"

 return result

def write_to_AI():
 while True:
 print("Choose an option:")
 print("1. Word Count")
 print("2. Auto Correct")
 print("3. Paraphrasing")
 print("4. Routine Maker")
 print("5. Exit")

 option = int(input("Enter your choice (1/2/3/4/5): "))

 if option == 1:
 text = input("Enter text: ")
 word_count = len(text.split())
 print("Word count:", word_count)

 elif option == 2:
 auto_correct_words = {
 'helo': 'hello',
 'aple': 'apple',
 'tomatoe': 'tomato',
 'bannana': 'banana',
 'writting': 'writing',
 'recieve': 'receive',
 'seperate': 'separate',
 'accomodate': 'accommodate',
 'neccessary': 'necessary',
 'definately': 'definitely',
 'experiance': 'experience',
 'occured': 'occurred',
 'embarass': 'embarrass',
 'arguement': 'argument',
 'priviledge': 'privilege',
 'truely': 'truly',
 'adress': 'address',
 'occurence': 'occurrence',
 'enviroment': 'environment',
 'independant': 'independent',
 'persue': 'pursue',
 'wierd': 'weird',
 'grammer': 'grammar',
 'enviorment': 'environment',
 'agressive': 'aggressive',
 'dissappear': 'disappear',
 'disapoint': 'disappoint',
 'calender': 'calendar',
 'collegue': 'colleague',
 'speach': 'speech',
 'millenium': 'millennium',
 'appologies': 'apologies',
 # Add more words as needed
 }

 text = input("Enter text: ")
 corrected_text = ' '.join(auto_correct_words.get(word, word) for word in 
text.split())
 print("Corrected text:", corrected_text)

 elif option == 3:
 text = input("Enter text: ")
 paraphraser = pipeline("text2text-generation", 
model="Vamsi/T5_Paraphrase_Paws")
 paraphrases = paraphraser(text, num_return_sequences=1)
 print("Paraphrased text:", paraphrases[0]['generated_text'])

 elif option == 4:
 num_tasks = int(input("Enter the number of tasks: "))
 tasks = []
 constraints = defaultdict(list)

 for i in range(num_tasks):
 task_name = input(f"Enter name of task {i + 1}: ")
 tasks.append(task_name)
 num_constraints = int(input(f"Enter the number of constraints for 
{task_name}: "))
 for j in range(num_constraints):
 constraint = input(f"Enter constraint {j + 1} for {task_name}: ")
 constraints[task_name].append(constraint)

 schedule = graph_coloring(tasks, constraints)
 for task, time_slot in schedule.items():
 print(f"Task '{task}' is scheduled at {time_slot}")

 elif option == 5:
 print("Exiting...")
 break

 else:
 print("Invalid option. Please choose 1, 2, 3, 4, or 5.")

def main():
 while True:
 print("Choose an option:")
 print("1. Speak to Jarvis")
 print("2. Write to your AI Assistant")
 print("3. Exit")

 choice = int(input("Enter your choice (1/2/3): "))

 if choice == 1:
 speak_to_jarvis()

 elif choice == 2:
 write_to_AI()

 elif choice == 3:
 print("Exiting...")
 break

 else:
 print("Invalid option. Please choose 1, 2, or 3.")

if __name__ == "__main__":
 main()
