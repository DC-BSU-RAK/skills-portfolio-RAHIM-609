import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import random
import time
import sys
import os

# For sound effects (Windows only; fallback to beep on others)
try:
    import winsound
    HAS_WINSOUND = True
except ImportError:
    HAS_WINSOUND = False

# --------------------------
# Load jokes from text file
# --------------------------
def load_or_create_jokes(filename="randomJokes.txt"):
    # If file DOES NOT exist → create it with default jokes
    if not os.path.exists(filename):
        with open(filename, "w") as f:
            f.write(DEFAULT_JOKES)
        print(f"{filename} not found — created new file with default jokes!")

    # Load jokes into list of (setup, punchline)
    jokes = []
    with open(filename, "r") as file:
        for line in file:
            line = line.strip()
            if not line:
                continue
            if "?" in line:
                setup, punchline = line.split("?", 1)
                jokes.append((setup + "?", punchline))

    return jokes


DEFAULT_JOKES = """Why did the chicken cross the road?To get to the other side.
What happens if you boil a clown?You get a laughing stock.
Why did the car get a flat tire?Because there was a fork in the road!
How did the hipster burn his mouth?He ate his pizza before it was cool.
What did the janitor say when he jumped out of the closet?SUPPLIES!!!!
Have you heard about the band 1023MB?It's probably because they haven't got a gig yet…
Why does the golfer wear two pants?Because he's afraid he might get a "Hole-in-one."
Why should you wear glasses to maths class?Because it helps with division.
Why does it take pirates so long to learn the alphabet?Because they could spend years at C.
Why did the woman go on the date with the mushroom?Because he was a fun-ghi.
Why do bananas never get lonely?Because they hang out in bunches.
What did the buffalo say when his kid went to college?Bison.
Why shouldn't you tell secrets in a cornfield?Too many ears.
What do you call someone who doesn't like carbs?Lack-Toast Intolerant.
Why did the can crusher quit his job?Because it was soda pressing.
Why did the birthday boy wrap himself in paper?He wanted to live in the present.
What does a house wear?A dress.
Why couldn't the toilet paper cross the road?Because it got stuck in a crack.
Why didn't the bike want to go anywhere?Because it was two-tired!
Want to hear a pizza joke?Nahhh, it's too cheesy!
Why are chemists great at solving problems?Because they have all of the solutions!
Why is it impossible to starve in the desert?Because of all the sand which is there!
What did the cheese say when it looked in the mirror?Halloumi!
Why did the developer go broke?Because he used up all his cache.
Did you know that ants are the only animals that don't get sick?It's true! It's because they have little antibodies.
Why did the donut go to the dentist?To get a filling.
What do you call a bear with no teeth?A gummy bear!
What does a vegan zombie like to eat?Graaains.
What do you call a dinosaur with only one eye?A Do-you-think-he-saw-us!
Why should you never fall in love with a tennis player?Because to them... love means NOTHING!
What did the full glass say to the empty glass?You look drunk.
What's a potato's favorite form of transportation?The gravy train
What did one ocean say to the other?Nothing, they just waved.
What did the right eye say to the left eye?Honestly, between you and me something smells.
What do you call a dog that's been run over by a steamroller?Spot!
What's the difference between a hippo and a zippo?One's pretty heavy and the other's a little lighter
Why don't scientists trust Atoms?They make up everything.
"""

class JokeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("😂 Joke Teller - Laugh Out Loud! 😂")
        self.root.geometry("500x600")
        self.root.resizable(True, True)

        # Load jokes
        self.jokes = load_or_create_jokes("randomJokes.txt")
        if not self.jokes:
            self.root.quit()
            return
        self.current_joke = None
        self.joke_count = 0

        # Create a canvas for gradient background
        self.canvas = tk.Canvas(root, width=500, height=600)
        self.canvas.pack(fill="both", expand=True)
        self.create_gradient()

        # Title label
        self.title_label = tk.Label(self.canvas, text="🤡 Welcome to the Joke Machine! 🤡", font=("Comic Sans MS", 18, "bold italic"), bg="#FFD700", fg="#FF4500")
        self.title_label.place(relx=0.5, rely=0.05, anchor="center")

        # Joke counter
        self.counter_label = tk.Label(self.canvas, text=f"Jokes Told: {self.joke_count} 😂", font=("Comic Sans MS", 12), bg="#FFD700", fg="#000000")
        self.counter_label.place(relx=0.5, rely=0.12, anchor="center")

        # Funny meter (progress bar)
        self.funny_meter = ttk.Progressbar(self.canvas, orient="horizontal", length=300, mode="determinate", maximum=10)
        self.funny_meter.place(relx=0.5, rely=0.18, anchor="center")
        self.funny_meter_label = tk.Label(self.canvas, text="Funny Meter: 0/10 😆", font=("Comic Sans MS", 10), bg="#FFD700", fg="#000000")
        self.funny_meter_label.place(relx=0.5, rely=0.22, anchor="center")

        # Setup label
        self.setup_label = tk.Label(self.canvas, text="", font=("Comic Sans MS", 14, "bold"), bg="#FFD700", fg="#000080", wraplength=400, justify="center")
        self.setup_label.place(relx=0.5, rely=0.35, anchor="center")

        # Punchline label (initially hidden)
        self.punchline_label = tk.Label(self.canvas, text="", font=("Comic Sans MS", 12, "italic"), bg="#FFD700", fg="#FF0000", wraplength=400, justify="center")
        self.punchline_label.place(relx=0.5, rely=0.5, anchor="center")

        # Buttons with styles
        style = ttk.Style()
        style.configure("Funny.TButton", font=("Comic Sans MS", 12, "bold"), padding=10, relief="raised", borderwidth=3)
        style.map("Funny.TButton", background=[("active", "#00FF00")], foreground=[("active", "#FFFFFF")])

        self.joke_button = ttk.Button(self.canvas, text="Hit me with a Joke! 😂", command=self.show_joke, style="Funny.TButton")
        self.joke_button.place(relx=0.5, rely=0.65, anchor="center")

        self.punchline_button = ttk.Button(self.canvas, text="Reveal the Punchline! 🤔", command=self.show_punchline, style="Funny.TButton")
        self.punchline_button.place(relx=0.5, rely=0.75, anchor="center")

        self.next_button = ttk.Button(self.canvas, text="Next Zany Joke! 😜", command=self.show_joke, style="Funny.TButton")
        self.next_button.place(relx=0.5, rely=0.85, anchor="center")

        self.quit_button = ttk.Button(self.canvas, text="Exit the Fun! 😢", command=root.quit, style="Funny.TButton")
        self.quit_button.place(relx=0.5, rely=0.95, anchor="center")

    def create_gradient(self):
        # Simple gradient background
        for i in range(600):
            color = "#%02x%02x%02x" % (255 - i//3, 215 - i//4, 0 + i//6)  # Yellow to orange gradient
            self.canvas.create_line(0, i, 500, i, fill=color)

    def show_joke(self):
        if not self.jokes:
            return
        self.current_joke = random.choice(self.jokes)
        setup, _ = self.current_joke
        self.setup_label.config(text=f"🤔 {setup}")
        self.punchline_label.config(text="")
        self.joke_count += 1
        self.counter_label.config(text=f"Jokes Told: {self.joke_count} 😂")
        # Update funny meter randomly
        funny_level = random.randint(1, 10)
        self.funny_meter["value"] = funny_level
        self.funny_meter_label.config(text=f"Funny Meter: {funny_level}/10 😆")

    def show_punchline(self):
        if self.current_joke:
            _, punchline = self.current_joke
            # Animated fade-in for punchline
            self.punchline_label.config(text="")
            self.root.after(500, lambda: self.fade_in_punchline(f"😄 {punchline}", 0))
            # Play laugh sound
            self.play_laugh_sound()

    def fade_in_punchline(self, text, alpha):
        if alpha <= 100:
            # Simulate fade by changing text color intensity (simple approximation)
            intensity = int(255 * (alpha / 100))
            color = f"#{intensity:02x}0000"  # Red fade-in
            self.punchline_label.config(text=text, fg=color)
            self.root.after(50, lambda: self.fade_in_punchline(text, alpha + 10))

    def play_laugh_sound(self):
        if HAS_WINSOUND:
            winsound.Beep(800, 300)  # Short beep
        else:
            print("\a")  # Fallback beep

# ----------------------------
# Run Application
# ----------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = JokeApp(root)
    root.mainloop()