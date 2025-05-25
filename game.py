import random
import os

# Spy-themed phrases and their riddle hints
phrases_riddles = {
    "steal the code": [
        "I’m the act of taking secrets unnoticed",  # steal
        "I’m the definite article",  # the
        "I’m a system of symbols to crack"  # code
    ],
    "meet at dusk": [
        "I’m where spies rendezvous",  # meet
        "I’m a preposition of place",  # at
        "I’m twilight’s shadowy time"  # dusk
    ],
    "hide the plan": [
        "I’m what spies do to stay unseen",  # hide
        "I’m the definite article",  # the
        "I’m a scheme for success"  # plan
    ],
    "guard the base": [
        "I’m what sentries do to protect",  # guard
        "I’m the definite article",  # the
        "I’m the spy’s secret headquarters"  # base
    ],
    "send the signal": [
        "I’m how spies dispatch messages",  # send
        "I’m the definite article",  # the
        "I’m a covert communication"  # signal
    ],
    "crack the lock": [
        "I’m what spies do to break barriers",  # crack
        "I’m the definite article",  # the
        "I’m a device to secure secrets"  # lock
    ],
    "find the spy": [
        "I’m what agents do to locate enemies",  # find
        "I’m the definite article",  # the
        "I’m a covert operative"  # spy
    ],
    "secure the file": [
        "I’m what spies do to protect intel",  # secure
        "I’m the definite article",  # the
        "I’m a dossier of secrets"  # file
    ],
    "drop the intel": [
        "I’m what spies do to deliver secrets",  # drop
        "I’m the definite article",  # the
        "I’m critical spy information"  # intel
    ],
    "trail the target": [
        "I’m what spies do to follow foes",  # trail
        "I’m the definite article",  # the
        "I’m the one being tracked"  # target
    ],
    "decode the note": [
        "I’m what spies do to unravel messages",  # decode
        "I’m the definite article",  # the
        "I’m a written secret"  # note
    ],
    "watch the gate": [
        "I’m what spies do to observe entries",  # watch
        "I’m the definite article",  # the
        "I’m an entrance to secure"  # gate
    ],
    "plant the bug": [
        "I’m what spies do to eavesdrop",  # plant
        "I’m the definite article",  # the
        "I’m a hidden listening device"  # bug
    ],
    "forge the pass": [
        "I’m what spies do to fake IDs",  # forge
        "I’m the definite article",  # the
        "I’m a ticket to access"  # pass
    ],
    "trace the call": [
        "I’m what spies do to find sources",  # trace
        "I’m the definite article",  # the
        "I’m a phone communication"  # call
    ],
    "break the cipher": [
        "I’m what spies do to crack codes",  # break
        "I’m the definite article",  # the
        "I’m an encrypted puzzle"  # cipher
    ]
}

# Mission prompts for immersion
prompts = [
    "Agent {name}, decode the scrambled intel!",
    "Agent {name}, unscramble the secret plan now!",
    "Agent {name}, reveal the hidden message!",
    "Agent {name}, infiltrate the base, decode now!"
]

# Feedback messages
feedback = [
    "Intel secured, Agent {name}!",
    "Mission success, Agent {name}!",
    "You’re a word-hunting pro, Agent {name}!",
    "Enemy outsmarted, Agent {name}!"
]

# Scramble a word’s letters
def scramble_word(word):
    word_list = list(word)
    random.shuffle(word_list)
    return "".join(word_list)

# Scramble entire phrase
def scramble_phrase(phrase):
    return " ".join(scramble_word(word) for word in phrase.split())

# Load high score, agent name, session results, and past phrases
def load_progress():
    if os.path.exists("word_hunt_progress.txt"):
        with open("word_hunt_progress.txt", "r") as f:
            lines = f.readlines()
            high_score = int(lines[0].strip()) if lines else 0
            agent_name = lines[1].strip() if len(lines) > 1 else "Unknown"
            session_results = []
            past_phrases = []
            current_session = None
            for line in lines[2:]:
                line = line.strip()
                if line.startswith("Session:"):
                    if current_session:
                        session_results.append(current_session)
                    current_session = {"phrase": line.split(": ")[1], "score": 0, "riddles": []}
                elif line.startswith("Score:"):
                    if current_session:
                        current_session["score"] = int(line.split(": ")[1])
                elif line.startswith("Riddle:"):
                    if current_session:
                        current_session["riddles"].append(line.split(": ", 1)[1])
                elif line:
                    past_phrases.append(line)
            if current_session:
                session_results.append(current_session)
            return high_score, agent_name, session_results, past_phrases
    return 0, "Unknown", [], []

# Save high score, agent name, session results, and past phrases
def save_progress(high_score, agent_name, session_results, past_phrases):
    with open("word_hunt_progress.txt", "w") as f:
        f.write(str(high_score) + "\n")
        f.write(agent_name + "\n")
        for session in session_results:
            f.write(f"Session: {session['phrase']}\n")
            f.write(f"Score: {session['score']}\n")
            for riddle in session["riddles"]:
                f.write(f"Riddle: {riddle}\n")
        for phrase in past_phrases:
            f.write(phrase + "\n")

def main():
    # Get player name
    name = input("Enter your codename, Agent: ").strip()
    if not name:
        name = "Unknown"
    high_score, saved_name, session_results, past_phrases = load_progress()
    # Use saved name if it exists and matches, else update
    agent_name = name if saved_name == "Unknown" or saved_name == name else saved_name
    session_phrases = []  # Track phrases used in this session
    points = 15  # Starting points for hints
    max_hints = 3

    while True:
        # Select a phrase not used in this session
        available_phrases = [p for p in phrases_riddles.keys() if p not in session_phrases]
        if not available_phrases:
            print(f"All missions completed in this session, Agent {agent_name}!")
            break
        phrase = random.choice(available_phrases)
        session_phrases.append(phrase)
        riddles = phrases_riddles[phrase]
        scrambled = scramble_phrase(phrase)
        words = phrase.split()
        scrambled_words = scrambled.split()
        hints_used = 0
        used_riddles = []  # Track riddles used in this round

        print("\n" + random.choice(prompts).format(name=agent_name))
        print(f"Scrambled intel: {scrambled}")

        while True:
            print(f"\nAgent {agent_name} Status | Points: {points} | Hints used: {hints_used}/{max_hints}")
            action = input("Enter a word, 'hint N' (e.g., 'hint 1' for word 1), or 'quit': ").lower()

            if action == "quit":
                print(f"Agency thanks you for your service, Agent {agent_name}!")
                # Save progress before exiting
                save_progress(high_score, agent_name, session_results, past_phrases)
                return
            elif action.startswith("hint ") and hints_used < max_hints and points >= 5:
                try:
                    word_idx = int(action.split()[1]) - 1
                    if 0 <= word_idx < len(words):
                        riddle = riddles[word_idx]
                        print(f"Intel: {riddle}. (-5 points)")
                        points -= 5
                        hints_used += 1
                        if riddle not in used_riddles:
                            used_riddles.append(f"{words[word_idx]}: {riddle}")
                    else:
                        print(f"Invalid word number, Agent {agent_name}! Choose 1 to {len(words)}.")
                except (IndexError, ValueError):
                    print(f"Invalid hint format, Agent {agent_name}! Use 'hint N' (e.g., 'hint 1').")
            elif action in words:
                word_idx = words.index(action)
                if scrambled_words[word_idx] != "CORRECT":
                    print(f"Correct word: '{action}'! (+30 points)")
                    points += 30
                    for _ in action:
                        points += 10  # +10 per correct letter
                    scrambled_words[word_idx] = "CORRECT"
                    print(f"Current intel: {' '.join(scrambled_words)}")
                    if all(w == "CORRECT" for w in scrambled_words):
                        print(f"Fully decoded: {phrase} (+50 points)")
                        points += 50
                        if phrase not in past_phrases:
                            past_phrases.append(phrase)
                        # Save session results
                        session_results.append({"phrase": phrase, "score": points, "riddles": used_riddles})
                        break
                else:
                    print(f"That word was already decoded, Agent {agent_name}!")
            else:
                print(f"Incorrect word or invalid input, Agent {agent_name}!")

        # Save progress after each round
        high_score = max(high_score, points)
        save_progress(high_score, agent_name, session_results, past_phrases)
        print(f"\nMission Report | Current points: {points}")
        print(f"High score: {high_score}")
        print("Decoded intel:", ", ".join(past_phrases) or "None")
        print(random.choice(feedback).format(name=agent_name))

        # Ask to continue
        cont = input(f"\nNew mission, Agent {agent_name}? (yes/no): ").lower()
        if cont != "yes":
            print(f"Agency thanks you for your service, Agent {agent_name}!")
            break

if __name__ == "__main__":
    main()