import requests
import string # Keep this import, even if not directly used for the custom CHARSET
import time
import json 

URL = "http://challenge.nahamcon.com:31054/guess"

# IMPORTANT: This CHARSET assumes the flag only contains lowercase hex characters and digits.
# If the flag contains ANY other character (uppercase, underscore, hyphen, etc.),
# this script WILL NOT find it and will output warnings.
CHARSET = "abcdef0123456789" 

FLAG_LENGTH_INSIDE_BRACES = 32

EMOJI_YELLOW = "\ud83d\udfe8" # 🟨
EMOJI_GREEN = "\ud83d\udfe9"  # 🟩
EMOJI_BLACK = "\u2b1b"   # ⬛

def make_guess(guess_str):
    """Sends a POST request to /guess and returns the emoji feedback string."""
    if not guess_str.startswith("flag{") or not guess_str.endswith("}"):
        raise ValueError("Guess must be in flag{} format.")
    if len(guess_str) != FLAG_LENGTH_INSIDE_BRACES + 6: # 7 for "flag{}"
        raise ValueError(f"Guess must be {FLAG_LENGTH_INSIDE_BRACES} chars inside braces.")

    payload = {"guess": guess_str}
    
    try:
        response = requests.post(URL, json=payload)
        response.raise_for_status() # Raise an exception for HTTP errors (4xx or 5xx)
        
        response_json = response.json()
        feedback = response_json.get("result")
        
        if feedback:
            print(f"Guess: {guess_str} -> Feedback: {feedback}")
        else:
            print(f"Guess: {guess_str} -> No 'result' field in response: {response.text}")
            return None
        
        return feedback
    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON response: {e}. Response: {response.text}")
        return None

def solve_flagdle():
    current_flag_chars = ['_'] * FLAG_LENGTH_INSIDE_BRACES 
    
    print("Starting Flagdle solver...")
    print(f"Target length: {FLAG_LENGTH_INSIDE_BRACES} characters inside braces.")
    print(f"Character set: {CHARSET}")

    for pos in range(FLAG_LENGTH_INSIDE_BRACES):
        print(f"\nAttempting to find character for position {pos}...")
        found_char_for_position = False
        
        for char_to_try in CHARSET:
            temp_guess_chars = list(current_flag_chars)
            temp_guess_chars[pos] = char_to_try
            
            guess_str = "flag{" + "".join(temp_guess_chars) + "}"
            feedback = make_guess(guess_str)
            if feedback is None:
                print("Exiting due to request error or malformed response.")
                return None
            
            if feedback[pos] == "🟩":
                current_flag_chars[pos] = char_to_try
                print(f"🟩 Found char '{char_to_try}' at position {pos}. Current flag: {''.join(current_flag_chars)}")
                found_char_for_position = True
                break
            
            time.sleep(0.01)

        if not found_char_for_position:
            print(f"⚠️ Warning: Could not find a correct character for position {pos} using the provided CHARSET. "
                  f"The correct character for this position is NOT in: {CHARSET}")
            # If a position cannot be resolved, the current flag cannot be completed with this CHARSET.
            # You might choose to break here, or let it continue to see other warnings.
            # For this strict CHARSET, if a char isn't found, the flag is likely not entirely hex/digit.
            # You might want to return None here to indicate failure.
            # return None 
            
    final_flag = "flag{" + "".join(current_flag_chars) + "}"
    print(f"\n--- Flagdle Solver Complete ---")
    print(f"Attempting final verification for: {final_flag}")
    
    final_feedback = make_guess(final_flag)
    if final_feedback and all(f == EMOJI_GREEN for f in final_feedback):
        print("🎉 Congratulations! The flag is all green!")
        return final_flag
    else:
        print("❌ Final guess was not all green. Review the logic or CHARSET.")
        return None

if __name__ == "__main__":
    found_flag = solve_flagdle()
    if found_flag:
        print(f"Final Flag: {found_flag}")
    else:
        print("Flag could not be determined with the given CHARSET.")