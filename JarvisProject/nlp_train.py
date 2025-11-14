def speak(x):
    print("Jarvis:", x)

# ----------------------------------------------------
# MODE SELECTION
# ----------------------------------------------------
USE_TEXT_MODE = False

print("Select Mode:")
print("1 → Voice Mode (Say 'Jarvis')")
print("2 → Text Mode (Type commands')")
choice = input("Enter 1 or 2: ").strip()

if choice == "2":
    USE_TEXT_MODE = True
    speak("Text mode activated.")
else:
    speak("Voice mode activated.")

print("Mode selection complete.")
