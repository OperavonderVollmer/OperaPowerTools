"""
    OperaPowerTools
    Yippie
"""


def opt_info() -> str:
    """
    Provide a brief description of the OperaPowerTools utility.

    Returns
    -------
    str
        A message describing the purpose and design philosophy of the OperaPowerTool.
        The toolkit is designed for lightweight, cross-project utility functions with 
        minimal load times due to on-demand imports.
    """

    message = (
        "OperaPowerTool is a lightweight utility toolkit for functions that aren't worth defining "
        "in a single script but are useful across multiple projects. Imports are handled within "
        "each function to keep load times minimal."
    )
    return message

def find_best_match(target: str, options: list) -> str | None :
    from rapidfuzz import process
    """
    Find the best match for a target string in a list of options.

    Parameters
    ----------
    target : str
        The target string to find a match for.
    options : list
        A list of strings to search for a match.

    Returns
    -------
    str or None
        The best match, or None if no match is found.

    Notes
    -----
    The best match is determined by finding the string in options with the highest
    Levenshtein similarity to the target string. The similarity is calculated using
    the jellyfish library. If the similarity is below 90, no match is returned.
    """
    bestMatch = process.extractOne(target, options, score_cutoff=90)
    return bestMatch[0] if bestMatch else None

def get_phonetic_representation(word: str) -> str:
    """
    Return a phonetic representation of the given word.

    Parameters
    ----------
    word : str
        The word to get a phonetic representation of.

    Returns
    -------
    str
        A phonetic representation of the word. This is computed using the
        double metaphone algorithm, and if the result is empty, the soundex
        algorithm is used instead.
    """

    from metaphone import doublemetaphone
    import jellyfish  
    
    metaphone_primary, metaphone_secondary = doublemetaphone(word)
    return metaphone_primary or metaphone_secondary or jellyfish.soundex(word)

def find_best_phonetic_match(target: str, options: list) -> str | None:    


    """
    Find the best match in options by computing the Levenshtein similarity between
    the phonetic representation of the target and the phonetic representation of
    each option.

    Parameters
    ----------
    target : str
        The target string to find a match for.
    options : list[str]
        The list of strings to search for the best match.

    Returns
    -------
    str | None
        The best match found in options, or None if no match was found with a
        similarity of at least 70.
    """


    from rapidfuzz import process
    
    target_phonetic = get_phonetic_representation(target)
    phonetic_map = {option: get_phonetic_representation(option) for option in options}
    best_match = process.extractOne(target_phonetic, phonetic_map.values(), score_cutoff=70)

    if best_match:
        for option, phonetic in phonetic_map.items():
            if phonetic == best_match[0]:
                return option

    return None

def normalize_number(input: int | str) -> int:
    
    """
    Normalize a given input into an integer.

    Parameters
    ----------
    input : int | str
        The input to normalize. If it is an integer, it will be returned as is.
        If it is a string, it will be stripped of its whitespace and converted to
        lowercase. If the string is a number, it will be returned as an integer.
        If the string is a word representation of a number, it will be converted
        to an integer.

    Returns
    -------
    int
        The normalized integer.

    Raises
    ------
    ValueError
        If the input is not a valid number or word representation of a number.
    """
    from word2number import w2n
    import re
    import inflect

    if isinstance(input, int): return input

    input = input.strip().lower()

    if input.isdigit():  
        return int(input)
    
    p = inflect.engine()
    input = re.sub(r'\b\d+\b', lambda x: p.number_to_words(x.group(0)), input)

    try:
        return w2n.word_to_num(input)
    except ValueError as e:
        raise ValueError(f"Invalid number input: {input}") from e

def bubble_sort(arr: list[int]) -> list[int]:
    """
    Sorts the given list of integers in ascending order using the bubble sort algorithm.

    The bubble sort algorithm works by repeatedly swapping adjacent elements if they are in the wrong order.
    The algorithm stops when no more swaps occur, indicating that the list is sorted.

    Parameters
    ----------
    arr : list[int]
        The list of integers to be sorted.

    Returns
    -------
    list[int]
        The sorted list of integers.

    Notes
    -----
    Bubble sort has a time complexity of O(n^2) in the worst case, which is less efficient than other sorting algorithms like insertion sort and selection sort.
    However, bubble sort has the advantage of being simple to implement and being relatively efficient when the input is already partially sorted.
    """
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(n - i - 1):
            if arr[j] > arr[j + 1]:  
                arr[j], arr[j + 1] = arr[j + 1], arr[j]  # Swap
                swapped = True
        if not swapped:  # Optimization: Stop if no swaps occurred
            break
    return arr

def selection_sort(arr: list[int]) -> list[int]:
    """
    Sorts the given list of integers in ascending order using the selection sort algorithm.

    The selection sort algorithm works by repeatedly selecting the minimum element from the unsorted subarray and swapping it with the first element of the unsorted subarray.
    The algorithm stops when all elements have been sorted.

    Parameters
    ----------
    arr : list[int]
        The list of integers to be sorted.

    Returns
    -------
    list[int]
        The sorted list of integers.

    Notes
    -----
    Selection sort has a time complexity of O(n^2) in the worst case, which is less efficient than other sorting algorithms like insertion sort and bubble sort.
    However, selection sort has the advantage of being simple to implement and being relatively efficient when the input is already partially sorted.
    """

    n = len(arr)
    for i in range(n):
        min_index = i  
        for j in range(i + 1, n):
            if arr[j] < arr[min_index]:  
                min_index = j
        arr[i], arr[min_index] = arr[min_index], arr[i]
    return arr

def insertion_sort(arr: list[int]) -> list[int]:
    """
    Sorts the given list of integers in ascending order using the insertion sort algorithm.

    The insertion sort algorithm works by iterating through the list and inserting each element into its correct position in the sorted subarray.
    The algorithm has a time complexity of O(n^2) in the worst case.
    However, insertion sort has the advantage of being simple to implement and being relatively efficient when the input is already partially sorted.

    Parameters
    ----------
    arr : list[int]
        The list of integers to be sorted.

    Returns
    -------
    list[int]
        The sorted list of integers.

    Notes
    -----
    Insertion sort has a time complexity of O(n^2) in the worst case, which is less efficient than other sorting algorithms like merge sort and quick sort.
    However, insertion sort has the advantage of being simple to implement and being relatively efficient when the input is already partially sorted.
    """
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:  
            arr[j + 1] = arr[j]  
            j -= 1
        arr[j + 1] = key  
    return arr


def sanitize_text(text: str, more_keywords: list[str] = []) -> tuple[str, str]:
    """
    Sanitizes the given text by blocking any strings that contain potentially
    dangerous keywords. The function takes an optional list of additional keywords
    to block. The function returns a tuple containing the sanitized text and an
    optional log message if any potentially dangerous keywords were found.

    Parameters
    ----------
    text : str
        The string to be sanitized.
    more_keywords : list[str], optional
        A list of additional keywords to block.

    Returns
    -------
    tuple[str, str]
        A tuple containing the sanitized text and an optional log message if any
        potentially dangerous keywords were found.

    Raises
    ------
    TypeError
        If more_keywords is not a list or if any of its elements are not strings.
    """
    import re
    log_message = ""

    if not isinstance(more_keywords, list) or not all(isinstance(k, str) for k in more_keywords):
        raise TypeError("more_keywords must be a list of strings")

    BLACKLISTED_KEYWORDS = [
        r"\bimport\b", r"\bexec\b", r"\beval\b", r"\bsystem\(", r"\bos\.", 
        r"\bsubprocess\.", r"\brm\s+-rf\b", r"\brmdir\b", r"\bdel\b", 
        r"\bopen\(", r"\bwrite\(", r"\bread\(", r"\bchmod\b", r"\bchown\b",  
    ]

    # Escape user-defined keywords to prevent regex injection
    escaped_keywords = [re.escape(k) for k in more_keywords]

    # Merge all keywords into a single regex pattern
    combined_pattern = "|".join(BLACKLISTED_KEYWORDS + escaped_keywords)

    # Find matches
    match = re.search(combined_pattern, text, re.IGNORECASE)
    
    if match:
        log_message = f"Blocked potentially dangerous input: '{text}' matches keyword '{match.group()}'"
        return "", log_message

    return text, ""


def enumerate_directory(path: str, levels: int = 1) -> dict[str, list[str | dict[str, list]]]:
    """
    Enumerates the contents of the given directory, optionally recursing into
    subdirectories up to the given number of levels.

    Parameters
    ----------
    path : str
        The path to the directory to enumerate.
    levels : int, optional
        The number of levels to recurse into subdirectories. Defaults to 1.

    Returns
    -------
    dict[str, list[str | dict[str, list]]]
        A dictionary with the given path as the key and a list of its contents as
        the value. If `levels` is greater than 1, each subdirectory will be
        represented as a nested dictionary. If any errors occur while enumerating
        the directory, the "error" key will contain a list of error messages.
    """
    
    def _scan_directory(directory: str, depth: int) -> list[str | dict[str, list]]:
        from os import scandir
        from os.path import isdir

        contents = []

        try:
            for entry in scandir(directory):
                if entry.is_file():
                    contents.append(entry.name)
                elif entry.is_dir() and depth > 0:
                    subdir_contents = _scan_directory(entry.path, depth - 1)
                    if subdir_contents:
                        contents.append({entry.name: subdir_contents})
        except PermissionError:
            pass  

        return contents

    from os.path import exists, isdir

    if not exists(path):
        return {"error": [f"Directory does not exist: {path}"]}

    if not isdir(path):
        return {"error": [f"Path is not a directory: {path}"]}

    return {path: _scan_directory(path, levels)}


def clipboard_get() -> str:
    """Retrieves the current contents of the system clipboard as a string.

    Returns
    -------
    str
        The contents of the clipboard.
    """
    import pyperclip
    return pyperclip.paste()

def clipboard_set(text: str) -> None:

    """Sets the contents of the system clipboard to the given text.

    Parameters
    ----------
    text : str
        The text to be copied to the clipboard.
    """
    import pyperclip
    pyperclip.copy(text)


def timed_delay(wait_time: float, variant_time_x: float = 0, variant_time_y: float = 0) -> None:
    """
    Blocks the current thread for a specified amount of time, with optional variability.

    Parameters
    ----------
    wait_time : float
        The base time in seconds to wait.
    variant_time_x : float, optional
        The minimum additional random time to add to the wait_time, defaults to 0.
    variant_time_y : float, optional
        The maximum additional random time to add to the wait_time, defaults to 0.

    Returns
    -------
    None
    """

    import time, random

    wait_time = max(0, wait_time)
    variant_time_x, variant_time_y = sorted([max(0, variant_time_x), max(0, variant_time_y)])

    total_delay = wait_time + random.uniform(variant_time_x, variant_time_y)
    print_from("OperaPowerTools", f"Waiting for {total_delay:.2f} seconds...")
    time.sleep(total_delay)


def random_within_boundary_box(x: float, y: float, h: float, w: float, centered: bool = False) -> tuple[int, int]:
    """
    Generates a random integer coordinate within a specified boundary box.

    If `centered` is True, the (x, y) coordinates represent the center of the boundary box,
    and the function adjusts the min/max values accordingly.

    Parameters
    ----------
    x : float
        The x-coordinate of the top-left corner (or center if centered=True) of the boundary box.
    y : float
        The y-coordinate of the top-left corner (or center if centered=True) of the boundary box.
    h : float
        The height of the boundary box.
    w : float
        The width of the boundary box.
    centered : bool, optional
        If True, the given (x, y) is treated as the center of the box instead of the top-left corner.

    Returns
    -------
    tuple[int, int]
        A tuple containing random x and y coordinates within the boundary box.

    Raises
    ------
    ValueError
        If the calculated min coordinates are greater than the max coordinates due to
        non-positive dimensions, indicating an invalid boundary box.
    """

    import random

    if centered:
        x_min, x_max = int(x - w / 2), int(x + w / 2)
        y_min, y_max = int(y - h / 2), int(y + h / 2)
    else:
        x_min, x_max = int(x), int(x + w)
        y_min, y_max = int(y), int(y + h)

    if x_min > x_max or y_min > y_max:
        raise ValueError(f"Invalid boundary box: ({x}, {y}, {h}, {w}). Ensure width and height are positive.")

    return random.randint(x_min, x_max), random.randint(y_min, y_max)


def file_move(source: str, destination: str) -> tuple[bool, str]:
    """
    Moves a file from one location to another.

    Parameters
    ----------
    source : str
        The source path of the file to be moved.
    destination : str
        The destination path where the file should be moved.

    Returns
    -------
    tuple[bool, str]
        A tuple where the first value indicates success (True/False), 
        and the second value contains an error message if failed.
    """
    import shutil, os

    # Ensure the source file exists
    if not os.path.exists(source):
        return False, f"Source file not found: {source}"

    # Ensure destination directory exists
    destination_dir = os.path.dirname(destination)
    if destination_dir and not os.path.exists(destination_dir):
        os.makedirs(destination_dir)

    try:
        shutil.move(source, destination)
        return True, "File moved successfully"
    except Exception as e:
        return False, f"Failed to move file: {e}"

    

def file_copy(source: str, destination: str) -> tuple[bool, str]:
    """
    Copies a file from one location to another.

    Parameters
    ----------
    source : str
        The source path of the file to be copied.
    destination : str
        The destination path where the file should be copied.

    Returns
    -------
    tuple[bool, str]
        A tuple where the first value indicates success (True/False),
        and the second value contains an error message if failed.
    """
    import shutil, os

    # Ensure the source file exists
    if not os.path.exists(source):
        return False, f"Source file not found: {source}"

    # Ensure destination directory exists
    destination_dir = os.path.dirname(destination)
    if destination_dir and not os.path.exists(destination_dir):
        os.makedirs(destination_dir)

    try:
        shutil.copy2(source, destination)  # copy2 preserves metadata
        return True, "File copied successfully"
    except Exception as e:
        return False, f"Failed to copy file: {e}"


def get_processes() -> list[str]:
    """
    Returns a list of currently running process names.

    Returns
    -------
    list[str]
        A list of process names (lowercased).
    """
    import psutil  # Lazy import

    return [p.info['name'].lower() for p in psutil.process_iter(['name']) if p.info['name']]


def kill_process(process_name: str, process_list: list[str] = None) -> bool:
    """
    Finds and kills the closest matching process.

    Parameters
    ----------
    process_name : str
        The name of the process to kill.
    process_list : list[str], optional
        A pre-fetched list of running process names for optimization.

    Returns
    -------
    bool
        True if a process was successfully killed, False otherwise.
    """
    import psutil

    # Fetch running processes if not provided
    process_list = process_list or get_processes()

    if not process_list:
        print("No running processes found.")
        return False

    best_match = find_best_match(process_name.lower(), process_list)

    if not best_match:
        print(f"No suitable match found for process: {process_name}")
        return False

    success = False
    for process in psutil.process_iter(['name']):
        if process.info['name'].lower() == best_match:
            try:
                process.kill()
                print(f"Killed process: {best_match}")
                success = True
            except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
                print(f"Could not terminate {best_match}: {e}")

    return success



def get_main_idea(passage: str, sentences: int = 1, summarizer: str = 'lsa') -> str:
    """
    Gets the main idea of a given passage of text.

    Parameters
    ----------
    passage : str
        The text passage to summarize.
    sentences : int, optional
        The number of sentences to return in the summary. Defaults to 1.
    summarizer : str, optional
        The summarizer to use. Choose from 'lsa', 'lex_rank', 'luhn', or 'text_rank'. Defaults to 'lsa'.

    Returns
    -------
    str
        The main idea of the passage, summarized in the number of sentences specified.

    Raises
    ------
    ValueError
        If the specified summarizer is not valid.
    """
    from sumy.parsers.plaintext import PlaintextParser
    from sumy.nlp.tokenizers import Tokenizer
    from sumy.summarizers.luhn import LuhnSummarizer
    from sumy.summarizers.lex_rank import LexRankSummarizer
    from sumy.summarizers.lsa import LsaSummarizer
    from sumy.summarizers.text_rank import TextRankSummarizer
    import nltk
    nltk.download('punkt_tab')


    summarizers = {
        'luhn': LuhnSummarizer,
        'lex_rank': LexRankSummarizer,
        'lsa': LsaSummarizer,
        'text_rank': TextRankSummarizer,
    }

    if summarizer not in summarizers:
        raise ValueError(f"Invalid summarizer '{summarizer}'. Choose from: {', '.join(summarizers.keys())}")
    
    parser = PlaintextParser.from_string(passage, Tokenizer("english"))
    summarizer_instance = summarizers[summarizer]()
    summary = summarizer_instance(parser.document, sentences)
    
    return " ".join(str(sentence) for sentence in summary)


def print_from(name: str, message: str) -> None:
    """
    Prints a message with the given name, prefixed in square brackets.

    Parameters
    ----------
    name : str
        The name to print in square brackets.
    message : str
        The message to print after the name.
    """
    
    print(f"[{name}] {message}")

def print_pretty(message: str, flourish: str, num: int) -> None:

    """
    Prints a message with a flourish around it.

    Parameters
    ----------
    message : str
        The message to print.
    flourish : str
        The character to use for the flourish.
    num : int
        The number of times to repeat the flourish on each side of the message.
    """
    print(f"{flourish * num} {message} {flourish * num}")