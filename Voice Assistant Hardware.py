import time
import subprocess
import RPi.GPIO as GPIO
import speech_recognition as sr
import pyttsx3


# ============================================================
# GPIO
# ============================================================

LED_PIN = 18

GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)

GPIO.output(LED_PIN, GPIO.LOW)


# ============================================================
# Voice Engine
# ============================================================

engine = pyttsx3.init()

engine.setProperty("rate", 150)
engine.setProperty("volume", 1.0)


def speak(text):
    print("Assistant:", text)

    engine.say(text)
    engine.runAndWait()


# ============================================================
# Speech Recognition
# ============================================================

recognizer = sr.Recognizer()


def listen():

    with sr.Microphone() as source:

        print("\nListening...")

        recognizer.adjust_for_ambient_noise(
            source,
            duration=0.5
        )

        try:

            audio = recognizer.listen(
                source,
                timeout=5,
                phrase_time_limit=5
            )

            print("Recognizing...")

            command = recognizer.recognize_google(
                audio
            )

            command = command.lower()

            print("You:", command)

            return command

        except sr.WaitTimeoutError:

            return ""

        except sr.UnknownValueError:

            speak("Sorry, I did not understand.")

            return ""

        except sr.RequestError:

            speak("Speech recognition service is unavailable.")

            return ""


# ============================================================
# Hardware Commands
# ============================================================

def process_command(command):

    # Turn LED ON
    if "turn on" in command and "light" in command:

        GPIO.output(LED_PIN, GPIO.HIGH)

        speak("Light turned on.")

        return True


    # Turn LED OFF
    elif "turn off" in command and "light" in command:

        GPIO.output(LED_PIN, GPIO.LOW)

        speak("Light turned off.")

        return True


    # LED ON
    elif "led on" in command:

        GPIO.output(LED_PIN, GPIO.HIGH)

        speak("LED turned on.")

        return True


    # LED OFF
    elif "led off" in command:

        GPIO.output(LED_PIN, GPIO.LOW)

        speak("LED turned off.")

        return True


    # Time
    elif "time" in command:

        current_time = time.strftime("%I:%M %p")

        speak(
            "The current time is "
            + current_time
        )

        return True


    # Exit
    elif (
        "exit" in command
        or "quit" in command
        or "stop assistant" in command
    ):

        speak("Goodbye.")

        return False


    # Unknown command
    else:

        speak("I don't know that command.")

        return True


# ============================================================
# Main Program
# ============================================================

try:

    speak("Voice assistant started.")

    speak(
        "You can say turn on light, "
        "turn off light, or what is the time."
    )

    running = True

    while running:

        command = listen()

        if command:

            running = process_command(
                command
            )


except KeyboardInterrupt:

    print("\nAssistant stopped.")


finally:

    GPIO.output(LED_PIN, GPIO.LOW)

    GPIO.cleanup()

    engine.stop()
