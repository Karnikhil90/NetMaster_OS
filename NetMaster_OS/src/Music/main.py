from machine import Pin, PWM
import time

# Set up PWM on GPIO 25 or D25 on the ESP32 board
pwm = PWM(Pin(25))
pwm.duty(512)  # Set default duty cycle for volume

# Dictionary of frequencies for basic notes
NOTE_FREQUENCIES = {
    # Octave 3
    'C3': 131, 'C#3': 139, 'D3': 147, 'D#3': 156,
    'E3': 165, 'F3': 175, 'F#3': 185, 'G3': 196,
    'G#3': 208, 'A3': 220, 'A#3': 233, 'B3': 247,

    # Octave 4
    'C4': 262, 'C#4': 277, 'D4': 294, 'D#4': 311,
    'E4': 330, 'F4': 349, 'F#4': 370, 'G4': 392,
    'G#4': 415, 'A4': 440, 'A#4': 466, 'B4': 494,

    # Octave 5
    'C5': 523, 'C#5': 554, 'D5': 587, 'D#5': 622,
    'E5': 659, 'F5': 698, 'F#5': 740, 'G5': 784,
    'G#5': 831, 'A5': 880, 'A#5': 932, 'B5': 988,

    # Octave 6
    'C6': 1047, 'C#6': 1109, 'D6': 1175, 'D#6': 1245,
    'E6': 1319, 'F6': 1397, 'F#6': 1480, 'G6': 1568,
    'G#6': 1661, 'A6': 1760, 'A#6': 1865, 'B6': 1976,

    # Rest (no sound)
    'REST': 0
}


def play_tone(frequency, duration):
    if frequency == 0:
        pwm.duty(0)  # Turn off sound for a rest
    else:
        pwm.freq(frequency)
        pwm.duty(512)  # Set duty cycle to play sound
    time.sleep(duration)
    pwm.duty(0)  # Stop the sound after the duration

def play_melody(melody):
    for note, duration in melody:
        play_tone(NOTE_FREQUENCIES[note], duration)

# Example melody (Twinkle Twinkle Little Star)
song1 = [
    ('C4', 0.5), ('C4', 0.5), ('G4', 0.5), ('G4', 0.5),
    ('A4', 0.5), ('A4', 0.5), ('G4', 1.0),
    ('F4', 0.5), ('F4', 0.5), ('E4', 0.5), ('E4', 0.5),
    ('D4', 0.5), ('D4', 0.5), ('C4', 1.0)
]

song2 = [
    ('E4', 0.5), ('E4', 0.5), ('F4', 0.5), ('G4', 0.5),
    ('G4', 0.5), ('F4', 0.5), ('E4', 0.5), ('D4', 0.5),
    ('C4', 0.5), ('C4', 0.5), ('D4', 0.5), ('E4', 0.5),
    ('E4', 0.75), ('D4', 0.25), ('D4', 1.0),
    ('E4', 0.5), ('E4', 0.5), ('F4', 0.5), ('G4', 0.5),
    ('G4', 0.5), ('F4', 0.5), ('E4', 0.5), ('D4', 0.5),
    ('C4', 0.5), ('C4', 0.5), ('D4', 0.5), ('E4', 0.5),
    ('D4', 0.75), ('C4', 0.25), ('C4', 1.0)
]

happy_birthday = [
    ('C4', 0.5), ('C4', 0.25), ('D4', 0.5), ('C4', 0.5),
    ('F4', 0.5), ('E4', 1.0),
    ('C4', 0.5), ('C4', 0.25), ('D4', 0.5), ('C4', 0.5),
    ('G4', 0.5), ('F4', 1.0),
    ('C4', 0.5), ('C4', 0.25), ('C5', 0.5), ('A4', 0.5),
    ('F4', 0.5), ('E4', 0.5), ('D4', 0.5),
    ('A#4', 0.5), ('A#4', 0.25), ('A4', 0.5), ('F4', 0.5),
    ('G4', 0.5), ('F4', 1.0)
]

jingle_bells = [
    ('E4', 0.5), ('E4', 0.5), ('E4', 1.0),
    ('E4', 0.5), ('E4', 0.5), ('E4', 1.0),
    ('E4', 0.5), ('G4', 0.5), ('C4', 0.5), ('D4', 0.5), ('E4', 1.0),
    ('F4', 0.5), ('F4', 0.5), ('F4', 0.5), ('F4', 0.5),
    ('F4', 0.5), ('E4', 0.5), ('E4', 0.5), ('E4', 0.25), ('E4', 0.25),
    ('E4', 0.5), ('D4', 0.5), ('D4', 0.5), ('E4', 0.5), ('D4', 0.5), ('G4', 1.0)
]

mary_lamb = [
    ('E4', 0.5), ('D4', 0.5), ('C4', 0.5), ('D4', 0.5),
    ('E4', 0.5), ('E4', 0.5), ('E4', 1.0),
    ('D4', 0.5), ('D4', 0.5), ('D4', 1.0),
    ('E4', 0.5), ('G4', 0.5), ('G4', 1.0),
    ('E4', 0.5), ('D4', 0.5), ('C4', 0.5), ('D4', 0.5),
    ('E4', 0.5), ('E4', 0.5), ('E4', 0.5), ('E4', 0.5),
    ('D4', 0.5), ('D4', 0.5), ('E4', 0.5), ('D4', 0.5), ('C4', 1.0)
]


# Main loop
songs = {
    "Twinkle ": song1,
    "Joy": song2,
    "Happy Birthday": happy_birthday,
    "Jingle Bells": jingle_bells,
    "Mary Had a Little Lamb": mary_lamb
}

# Main loop
while True:
    for song_name, melody in songs.items():
        print(f"Playing: {song_name}")
        play_melody(melody)
        print("Next song will play in 2 seconds...")
        time.sleep(2)  # 2-second delay before the next song