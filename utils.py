def prompt_list(prompt_text: str) -> list[str]:
    user_input = input(prompt_text).replace(" ", "")
    return user_input.split(",") if user_input else []

def prompt_int(prompt_text: str, default_value: int | None = None) -> int | None:
    while True:
        user_input = input(prompt_text).strip()
        if not user_input:
            return default_value
        try:
            value = int(user_input)
            if value >= 0:
                return value
            else:
                print("Please enter a non-negative number for depth.")
        except ValueError:
            print("Invalid input. Please enter a number or leave empty.")
