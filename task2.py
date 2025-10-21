import re
from typing import Generator, Callable

def generator_numbers(text: str) -> Generator[float, None, None]:
    """
    Analyzes the text and recognizes all real nums, separated by spaces,
    returns nums as a generator.
    """
    pattern = r'\b\d+(?:\.\d+)?\b' #regex pattern for real numbers
    
    #finds all matches in text
    for match in re.finditer(pattern, text):
        #converts the matched str to float and yield it
        yield float(match.group(0))

def sum_profit(text: str, func: Callable[[str], Generator[float, None, None]]) -> float:
    """
    Calcs total profit by summing all real numbers generated 
    by the provided gen func from the text
    """
    #uses gen func to get the nums and then sums them up
    return sum(func(text))

#usage example
text = """Загальний дохід працівника складається з декількох частин: 
1000.01 як основний дохід, доповнений додатковими надходженнями 27.45 і 324.00 доларів."""
total_income = sum_profit(text, generator_numbers)

print(f"Total profit: {total_income}")