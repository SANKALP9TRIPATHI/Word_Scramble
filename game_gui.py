import random
import time
import os
import json
from datetime import datetime

# For colorful text in terminal
try:
    import colorama
    from colorama import Fore, Back, Style
    colorama.init(autoreset=True)
    HAS_COLORS = True
except ImportError:
    HAS_COLORS = False
    class DummyColors:
        def __getattr__(self, name):
            return ""
    Fore = Back = Style = DummyColors()

class WordScrambleGame:
    def __init__(self):
        self.score = 0
        self.player_name = ""
        self.leaderboard_file = "word_scramble_leaderboard.json"
        self.difficulty_levels = {
            'easy': {'word_count': 10, 'time_limit': 60, 'points': 10, 'color': Fore.GREEN},
            'medium': {'word_count': 15, 'time_limit': 45, 'points': 20, 'color': Fore.YELLOW},
            'hard': {'word_count': 20, 'time_limit': 30, 'points': 30, 'color': Fore.RED}
        }
        self.selected_difficulty = 'medium'

        self.word_bank = [
            # Easy words (4-5 letters)
            "cake", "game", "blue", "jump", "play", "talk", "walk", "fast", "swim", "read",
            "sing", "time", "road", "hand", "feet", "desk", "book", "file", "door", "city",
            # Medium words (6-8 letters)
            "computer", "language", "internet", "victory", "journey", "student", "practice",
            "mountain", "elephant", "universe", "chocolate", "keyboard", "tropical", "stadium",
            "calendar", "festival", "building", "painting", "exercise", "question",
            # Hard words (9+ letters)
            "intelligence", "development", "conversation", "opportunity", "environment",
            "celebration", "imagination", "technology", "restaurant", "experience",
            "friendship", "challenge", "adventure", "wonderful", "beautiful"
        ]

        # ASCII art for game logo
        self.logo = """
        ██╗    ██╗ ██████╗ ██████╗ ██████╗     ███████╗ ██████╗██████╗  █████╗ ███╗   ███╗██████╗ ██╗     ███████╗
        ██║    ██║██╔═══██╗██╔══██╗██╔══██╗    ██╔════╝██╔════╝██╔══██╗██╔══██╗████╗ ████║██╔══██╗██║     ██╔════╝
        ██║ █╗ ██║██║   ██║██████╔╝██║  ██║    ███████╗██║     ██████╔╝███████║██╔████╔██║██████╔╝██║     █████╗  
        ██║███╗██║██║   ██║██╔══██╗██║  ██║    ╚════██║██║     ██╔══██╗██╔══██║██║╚██╔╝██║██╔══██╗██║     ██╔══╝  
        ╚███╔███╔╝╚██████╔╝██║  ██║██████╔╝    ███████║╚██████╗██║  ██║██║  ██║██║ ╚═╝ ██║██████╔╝███████╗███████╗
         ╚══╝╚══╝  ╚═════╝ ╚═╝  ╚═╝╚═════╝     ╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝╚═════╝ ╚══════╝╚══════╝
        """

        self.trophy = """
              .-=========-.
              \\'-=======-'/
              _|   .=.   |_
             ((|  {{1}}  |))
              \\|   /|\\   |/
               \\__ '`' __/
                 _`) (`_
               _/_______\\_
              /___________\\
        """

    def display_animated_text(self, text, delay=0.03, color=None):
        for char in text:
            if color:
                print(f"{color}{char}", end='', flush=True)
            else:
                print(char, end='', flush=True)
            time.sleep(delay)
        print()

    def load_leaderboard(self):
        if os.path.exists(self.leaderboard_file):
            try:
                with open(self.leaderboard_file, 'r') as file:
                    return json.load(file)
            except:
                return []
        else:
            return []

    def save_leaderboard(self, leaderboard):
        with open(self.leaderboard_file, 'w') as file:
            json.dump(leaderboard, file)

    def update_leaderboard(self):
        leaderboard = self.load_leaderboard()

        entry = {
            'name': self.player_name,
            'score': self.score,
            'difficulty': self.selected_difficulty,
            'date': datetime.now().strftime("%Y-%m-%d %H:%M")
        }

        leaderboard.append(entry)
        leaderboard.sort(key=lambda x: x['score'], reverse=True)
        leaderboard = leaderboard[:10]
        self.save_leaderboard(leaderboard)

        player_rank = next((i for i, item in enumerate(leaderboard)
                            if item['name'] == self.player_name and
                               item['score'] == self.score and
                               item['date'] == entry['date']), -1)

        if player_rank < 3 and player_rank != -1:
            self.display_congratulations(player_rank + 1)

    def display_congratulations(self, rank):
        os.system('cls' if os.name == 'nt' else 'clear')

        medals = {
            1: f"{Fore.YELLOW}🥇 GOLD MEDAL 🥇",
            2: f"{Fore.WHITE}🥈 SILVER MEDAL 🥈",
            3: f"{Fore.RED}🥉 BRONZE MEDAL 🥉"
        }

        medal_display = medals.get(rank, "")

        print(f"{Fore.CYAN}{self.trophy}")
        print(f"\n{Fore.YELLOW}🎉 CONGRATULATIONS {self.player_name.upper()}! 🎉")
        print(f"\n{medal_display}")
        print(f"\n{Fore.CYAN}You've reached RANK #{rank} on the leaderboard!")
        print(f"{Fore.CYAN}Your score: {Fore.YELLOW}{self.score} points")

        input(f"\n{Style.DIM}Press Enter to continue...{Style.RESET_ALL}")

    def display_leaderboard(self):
        leaderboard = self.load_leaderboard()

        print(f"\n{Fore.CYAN}{'=' * 70}")
        print(f"{Fore.YELLOW}🏆 WORD SCRAMBLE CHALLENGE LEADERBOARD 🏆".center(70))
        print(f"{Fore.CYAN}{'=' * 70}")

        if not leaderboard:
            print(f"{Fore.WHITE}No scores recorded yet. Be the first one!".center(70))
        else:
            print(f"{Fore.CYAN}{'Rank':<6}{'Name':<15}{'Score':<10}{'Difficulty':<12}{'Date':<20}")
            print(f"{Fore.CYAN}{'-' * 70}")

            for i, entry in enumerate(leaderboard):
                if i == 0:
                    rank_color = Fore.YELLOW  # Gold
                elif i == 1:
                    rank_color = Fore.WHITE   # Silver
                elif i == 2:
                    rank_color = Fore.RED     # Bronze
                else:
                    rank_color = Fore.CYAN

                diff_color = self.difficulty_levels[entry['difficulty']]['color']

                print(f"{rank_color}{i+1:<6}{Fore.WHITE}{entry['name']:<15}{Fore.GREEN}{entry['score']:<10}{diff_color}{entry['difficulty']:<12}{Fore.CYAN}{entry['date']:<20}")

        print(f"{Fore.CYAN}{'=' * 70}\n")

    def scramble_word(self, word):
        chars = list(word)
        while True:
            random.shuffle(chars)
            scrambled = ''.join(chars)
            if scrambled != word:
                return scrambled
            if len(word) <= 2:
                return scrambled

    def display_difficulty_selection(self):
        difficulty_art = [
            f"""{Fore.GREEN}
            ┌───────────────────────────┐
            │   EASY MODE - BEGINNER    │
            ├───────────────────────────┤
            │ ✓ 10 words                │
            │ ✓ 60 seconds per word     │
            │ ✓ 10 points per word      │
            │ ✓ Shorter words (4-5)     │
            └───────────────────────────┘
            """,

            f"""{Fore.YELLOW}
            ┌───────────────────────────┐
            │   MEDIUM MODE - CASUAL    │
            ├───────────────────────────┤
            │ ✓ 15 words                │
            │ ✓ 45 seconds per word     │
            │ ✓ 20 points per word      │
            │ ✓ Medium words (6-8)      │
            └───────────────────────────┘
            """,

            f"""{Fore.RED}
            ┌───────────────────────────┐
            │    HARD MODE - EXPERT     │
            ├───────────────────────────┤
            │ ✓ 20 words                │
            │ ✓ 30 seconds per word     │
            │ ✓ 30 points per word      │
            │ ✓ Longer words (9+)       │
            └───────────────────────────┘
            """
        ]

        print("\n" + "\n".join(difficulty_art))

    def select_difficulty(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"{Fore.CYAN}{self.logo}")
        print(f"\n{Fore.YELLOW}=== DIFFICULTY SELECTION ==={Style.RESET_ALL}")

        self.display_difficulty_selection()

        print(f"\n{Fore.WHITE}Select your challenge level:")
        print(f"{Fore.GREEN}1. Easy   {Fore.WHITE}- For a relaxed gameplay experience")
        print(f"{Fore.YELLOW}2. Medium {Fore.WHITE}- Balanced challenge (recommended)")
        print(f"{Fore.RED}3. Hard   {Fore.WHITE}- For word masters only!")

        while True:
            choice = input(f"\n{Fore.CYAN}Enter your choice (1-3): {Fore.WHITE}").strip()
            if choice == '1':
                self.selected_difficulty = 'easy'
                break
            elif choice == '2':
                self.selected_difficulty = 'medium'
                break
            elif choice == '3':
                self.selected_difficulty = 'hard'
                break
            else:
                print(f"{Fore.RED}Invalid choice. Please enter 1, 2, or 3.")

    def get_words_for_round(self):
        if self.selected_difficulty == 'easy':
            words = [w for w in self.word_bank if len(w) <= 5]
        elif self.selected_difficulty == 'medium':
            words = [w for w in self.word_bank if 6 <= len(w) <= 8]
        else:  
            words = [w for w in self.word_bank if len(w) >= 9]

        if len(words) < self.difficulty_levels[self.selected_difficulty]['word_count']:
            additional = random.sample(self.word_bank,
                                     self.difficulty_levels[self.selected_difficulty]['word_count'] - len(words))
            words.extend(additional)

        return random.sample(words, self.difficulty_levels[self.selected_difficulty]['word_count'])

    def display_countdown(self, seconds):
        for i in range(seconds, 0, -1):
            if i == 3:
                color = Fore.RED
            elif i == 2:
                color = Fore.YELLOW
            else:
                color = Fore.GREEN

            print(f"{color}{i}...", end='\r')
            time.sleep(0.7)
        print(f"{Fore.CYAN}GO!{' ' * 10}")
        time.sleep(0.3)

    def play_round(self):
        self.score = 0
        words = self.get_words_for_round()
        word_count = self.difficulty_levels[self.selected_difficulty]['word_count']
        time_limit = self.difficulty_levels[self.selected_difficulty]['time_limit']
        points_per_word = self.difficulty_levels[self.selected_difficulty]['points']
        difficulty_color = self.difficulty_levels[self.selected_difficulty]['color']

        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"{Fore.CYAN}{self.logo}")

        print(f"\n{difficulty_color}{'=' * 70}")
        print(
            f"{Fore.YELLOW}WORD SCRAMBLE CHALLENGE - {difficulty_color}{self.selected_difficulty.upper()}{Fore.YELLOW} MODE".center(
                70))
        print(f"{difficulty_color}{'=' * 70}")
        print(f"{Fore.WHITE}Unscramble {word_count} words. {time_limit} seconds per word.")
        print(f"{Fore.WHITE}Each correct answer: {Fore.GREEN}+{points_per_word} points{Fore.WHITE} + time bonus!")
        print(f"{difficulty_color}{'=' * 70}")

        input(f"\n{Fore.CYAN}Press Enter to start the challenge...{Style.RESET_ALL}")
        print(f"\n{Fore.YELLOW}Get ready, {self.player_name}!")
        self.display_countdown(3)

        for i, word in enumerate(words, 1):
            scrambled = self.scramble_word(word)

            print(f"\n{difficulty_color}{'─' * 40}")
            print(f"{difficulty_color}┌{'─' * (len(scrambled) + 18)}┐")
            print(
                f"{difficulty_color}│ {Fore.WHITE}Word {i}/{word_count}: {Fore.YELLOW}{scrambled.upper()} {difficulty_color}│")
            print(f"{difficulty_color}└{'─' * (len(scrambled) + 18)}┘")

            print(f"{Fore.GREEN}⏱️ Time: {time_limit} seconds")

            start_time = time.time()

            print(f"{Fore.CYAN}Your answer: {Fore.WHITE}", end='', flush=True)
            answer = input()

            elapsed = time.time() - start_time
            time_remaining = max(0, time_limit - int(elapsed))

            if elapsed >= time_limit:
                print(f"\n{Fore.RED}⏰ Time's up! {Fore.WHITE}The word was: {Fore.YELLOW}{word.upper()}")
                continue

            if answer.lower() == word.lower():
                time_bonus = max(0, int((time_limit - elapsed) / 5))
                round_score = points_per_word + time_bonus
                self.score += round_score

                self.display_answer_box(answer, True)
                print(
                    f"{Fore.WHITE}+{points_per_word} points + {time_bonus} time bonus = {Fore.YELLOW}+{round_score} points{Fore.WHITE}")
                print(f"{Fore.CYAN}Current Score: {Fore.YELLOW}{self.score}")
            else:
                self.display_answer_box(answer, False, word)

        print(f"\n{Fore.GREEN}{'=' * 70}")
        print(f"{Fore.YELLOW}🎮 GAME COMPLETE! 🎮".center(70))
        print(f"{Fore.GREEN}{'=' * 70}")

        self.display_animated_text(f"Final Score: {self.score} points!", 0.05, Fore.YELLOW)

        print(f"\n{Fore.CYAN}Difficulty: {difficulty_color}{self.selected_difficulty.capitalize()}")
        print(f"{Fore.CYAN}Words attempted: {Fore.WHITE}{word_count}")

        self.update_leaderboard()

    def display_instructions(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"{Fore.CYAN}{self.logo}")

        print(f"\n{Fore.YELLOW}{'=' * 70}")
        print(f"{Fore.YELLOW}HOW TO PLAY WORD SCRAMBLE CHALLENGE".center(70))
        print(f"{Fore.YELLOW}{'=' * 70}")

        instructions = [
            f"{Fore.GREEN}1.{Fore.WHITE} Words will appear with their letters scrambled",
            f"{Fore.GREEN}2.{Fore.WHITE} Type the correct unscrambled word before time runs out",
            f"{Fore.GREEN}3.{Fore.WHITE} You earn points for each correct answer",
            f"{Fore.GREEN}4.{Fore.WHITE} You get bonus points for answering quickly",
            f"{Fore.GREEN}5.{Fore.WHITE} Try to get the highest score and top the leaderboard!"
        ]

        for instruction in instructions:
            time.sleep(0.3)
            print(instruction)

        print(f"{Fore.YELLOW}{'=' * 70}")

        print(f"\n{Fore.CYAN}Example:")
        print(f"{Fore.WHITE}If you see: {Fore.YELLOW}ESDTU")
        print(f"{Fore.WHITE}You should type: {Fore.GREEN}DUETS")

        print(f"\n{Fore.CYAN}Scoring:")
        print(f"{Fore.WHITE}Correct answer: {Fore.GREEN}+10-30 points {Fore.WHITE}(depends on difficulty)")
        print(f"{Fore.WHITE}Speed bonus: {Fore.GREEN}Up to +12 points {Fore.WHITE}for quick answers")

        print(f"\n{Fore.CYAN}Difficulty Levels:")
        print(f"{Fore.GREEN}Easy:{Fore.WHITE} Shorter words, more time")
        print(f"{Fore.YELLOW}Medium:{Fore.WHITE} Medium words, moderate time")
        print(f"{Fore.RED}Hard:{Fore.WHITE} Longer words, less time")

    def display_exit_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

        goodbye_art = f"""
        {Fore.CYAN}
         _______ _                 _           __              ___ _           _             _ 
        |__   __| |               | |         / _|            / (_) |         (_)           | |
           | |  | |__   __ _ _ __ | | _____  | |_ ___  _ __  | |_| |__   __ _ _ _ __   __ _| |
           | |  | '_ \\ / _` | '_ \\| |/ / __| |  _/ _ \\| '__| | | | '_ \\ / _` | | '_ \\ / _` | |
           | |  | | | | (_| | | | |   <\\__ \\ | || (_) | |    | | | |_) | (_| | | | | | (_| |_|
           |_|  |_| |_|\\__,_|_| |_|_|\\_\\___/ |_| \\___/|_|    |_|_|_.__/ \\__, |_|_| |_|\\__, (_)
                                                                        __/ |          __/ |  
                                                                       |___/          |___/   
        """

        print(goodbye_art)
        print(f"\n{Fore.YELLOW}Thanks for playing Word Scramble Challenge, {self.player_name}!")
        print(f"\n{Fore.WHITE}We hope to see you again soon!")
        print(f"\n{Fore.CYAN}Your highest score: {Fore.GREEN}{self.get_player_high_score()}")

        time.sleep(2)

    def get_player_high_score(self):
        leaderboard = self.load_leaderboard()
        player_scores = [entry['score'] for entry in leaderboard if entry['name'] == self.player_name]
        return max(player_scores) if player_scores else 0

    def display_main_menu(self):
        menu_items = [
            f"{Fore.GREEN}1. {Fore.WHITE}Play Game",
            f"{Fore.YELLOW}2. {Fore.WHITE}View Leaderboard",
            f"{Fore.CYAN}3. {Fore.WHITE}Instructions",
            f"{Fore.RED}4. {Fore.WHITE}Exit"
        ]

        for item in menu_items:
            time.sleep(0.1)
            print(item)
    def display_answer_box(self, answer, is_correct, correct_word=None):
        box_width = max(len(answer), len(correct_word) if correct_word else 0) + 10

        if is_correct:
           print(f"\n{Fore.GREEN}┌{'─' * box_width}┐")
           print(f"{Fore.GREEN}│ {Fore.WHITE}Your answer: {Fore.YELLOW}{answer.upper()}{' ' * (box_width - 14 - len(answer))} {Fore.GREEN}│")
           print(f"{Fore.GREEN}│ {Fore.GREEN}✓ CORRECT! {' ' * (box_width - 11)} {Fore.GREEN}│")
           print(f"{Fore.GREEN}└{'─' * box_width}┘")
        else:
           print(f"\n{Fore.RED}┌{'─' * box_width}┐")
           print(f"{Fore.RED}│ {Fore.WHITE}Your answer: {Fore.YELLOW}{answer.upper()}{' ' * (box_width - 14 - len(answer))} {Fore.RED}│")
           print(f"{Fore.RED}│ {Fore.RED}✗ WRONG! {' ' * (box_width - 9)} {Fore.RED}│")
        if correct_word:
            print(f"{Fore.RED}│ {Fore.WHITE}Correct word: {Fore.YELLOW}{correct_word.upper()}{' ' * (box_width - 16 - len(correct_word))} {Fore.RED}│")
        print(f"{Fore.RED}└{'─' * box_width}┘")

    def simple_input_box(self, prompt, width=40):
          box_width = max(width, len(prompt) + 4)

          print(f"{Fore.CYAN}┌{'─' * box_width}┐")
          print(f"{Fore.CYAN}│ {Fore.WHITE}{prompt}{' ' * (box_width - len(prompt) - 2)}{Fore.CYAN}│")
          print(f"{Fore.CYAN}└{'─' * box_width}┘")

          print(f"\033[1A\033[{len(prompt) + 3}C", end="", flush=True)

          answer = input()

          print()

          return answer

    def start_game(self):
        if not HAS_COLORS:
            print("For the best experience, install colorama:")
            print("pip install colorama")
            print("Continuing with limited styling...\n")
            time.sleep(2)

        os.system('cls' if os.name == 'nt' else 'clear')

        for line in self.logo.split('\n'):
            print(f"{Fore.CYAN}{line}")
            time.sleep(0.05)

        print(f"\n{Fore.YELLOW}{'=' * 70}")
        print(f"{Fore.YELLOW}WELCOME TO WORD SCRAMBLE CHALLENGE".center(70))
        print(f"{Fore.YELLOW}{'=' * 70}")

        while True:
            self.player_name = input(f"\n{Fore.CYAN}Enter your name: {Fore.WHITE}").strip()
            if self.player_name:
                break
            print(f"{Fore.RED}Please enter a valid name.")

        while True:
            os.system('cls' if os.name == 'nt' else 'clear')

            print(f"{Fore.CYAN}{self.logo}")

            print(f"\n{Fore.YELLOW}{'=' * 70}")
            print(f"{Fore.YELLOW}WORD SCRAMBLE CHALLENGE - Player: {Fore.WHITE}{self.player_name}".center(70))
            print(f"{Fore.YELLOW}{'=' * 70}")

            self.display_main_menu()

            choice = input(f"\n{Fore.CYAN}Enter your choice (1-4): {Fore.WHITE}").strip()

            if choice == '1':
                self.select_difficulty()
                self.play_round()
                input(f"\n{Fore.CYAN}Press Enter to continue...{Style.RESET_ALL}")
            elif choice == '2':
                self.display_leaderboard()
                input(f"\n{Fore.CYAN}Press Enter to continue...{Style.RESET_ALL}")
            elif choice == '3':
                self.display_instructions()
                input(f"\n{Fore.CYAN}Press Enter to continue...{Style.RESET_ALL}")
            elif choice == '4':
                self.display_exit_screen()
                break
            else:
                print(f"{Fore.RED}Invalid choice. Please enter 1, 2, 3, or 4.")


def input_with_timeout(prompt, timeout):
    import sys
    import select

    if os.name == 'nt':
        import msvcrt
        start_time = time.time()
        sys.stdout.write(prompt)
        sys.stdout.flush()

        input_str = ''
        while True:
            if msvcrt.kbhit():
                char = msvcrt.getche().decode('utf-8')
                if char == '\r':  
                    sys.stdout.write('\n')
                    return input_str
                elif char == '\b':  
                    if input_str:
                        input_str = input_str[:-1]
                        sys.stdout.write(' \b')  
                else:
                    input_str += char

            if time.time() - start_time > timeout:
                continue 
            time.sleep(0.1)
    else:
        print(prompt, end='', flush=True)
        start_time = time.time()
        input_str = ''

        while True:
            rlist, _, _ = select.select([sys.stdin], [], [], 0.1)  
            if rlist:
                char = sys.stdin.read(1)
                if char == '\n':
                    return input_str
                else:
                    input_str += char
                    print(char, end='', flush=True)
            if time.time() - start_time > timeout:
                continue  
            time.sleep(0.1)


if __name__ == "__main__":
    try:
        game = WordScrambleGame()
        game.start_game()
    except KeyboardInterrupt:
        print(f"\n\n{Fore.YELLOW}Game interrupted. Thanks for playing!")
    except Exception as e:
        print(f"\n{Fore.RED}An error occurred: {e}")
        print(f"{Fore.WHITE}Sorry for the inconvenience.")