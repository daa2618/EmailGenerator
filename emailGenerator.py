import re


def _splitName(name:str)->tuple:
    """
    Splits a person's name into first, middle, and last names.

    Args:
        name (str): The full name of the person.

    Returns:
        tuple: A tuple containing the first, middle, and last names.
            If the name has fewer than three parts, the missing parts will be None.

    Example:
        ```python
        name = "John Doe"
        first, middle, last = splitName(name)
        print(first, middle, last)  # Output: John None Doe
        ```
    """
    split = name.split()
    first, middle, last = None, None, None
    try:
        first, last = split
    except:
        try:
            first, middle, last = split
        except Exception as e:
            print(f"{len(split)=}\n{e}")

    return first, middle, last

def _getFormatListAndSeperator(emailFormat):
    """Extracts format list and separators from an email format string.

    Args:
        emailFormat (str): A string representing the email format, 
                           where format elements are enclosed in square brackets 
                           `[]`, and separators are between them.

    Returns:
        tuple: A tuple containing two lists:
            - The first list contains the format elements (strings within `[]`).
            - The second list contains the separators (strings between `[]`).

    Example:
        >>> getFormatListAndSeperator("[first]_[last]") 
        >>> returns (["first", "last"], ["_"])
        >>>  getFormatListAndSeperator("[first_initial]_[last]") 
        >>> returns (["first_initial", "last"], ["_"])

    Note:  This function uses regular expressions.  It assumes that format elements are 
           enclosed in square brackets and that separators are the text between them.  
           It might not handle all possible edge cases or malformed input strings.
    """
    formatList, separator = re.findall("\\[(.*?)\\]", emailFormat), re.findall("\\](.*?)\\[", emailFormat)
    if separator:
        separator = separator[0]
    else:
        separator = ""

    return formatList, separator

def _getSequencingWords(formatList):
    """Extracts sequencing words from a list of strings.

      This function iterates through a list of strings and extracts the substring 
      following an underscore "_" character, up to a backspace character ('\b').  
      Only strings containing an underscore followed by a backspace are considered.
    
      Args:
        formatList: A list of strings.  Each string is expected to be in the format 
                    "word_sequencingWord\b", where "word" is any alphanumeric word 
                    and "sequencingWord" is the desired extracted part.
    
      Returns:
        A list of strings. Each string is the extracted "sequencingWord" from the 
        input strings that matched the pattern. Returns an empty list if no strings 
        match the pattern or if the input list is empty.
    
      Raises:
        None.  The function handles potential errors (no match) gracefully by returning 
        an empty list.
    
      Example:
        getSequencingWords(["first_three\b", "last_two\b", "other_stuff"]) 
        == ["three", "two", "stuff]
    
        getSequencingWords(["no_match"]) == ["match"]
    
        getSequencingWords([]) == []
      """
    return [re.findall(r"\w+_(.*?)\b", x)[0] for x in formatList if re.findall(r"\w+_(.*?)\b", x)]

def _getNewEmailFormat(word, formatList, emailFormat, newFormatOptions = ["first", "last", "middle"]):
    """Generates a new email format based on a given word and a list of existing formats.

    This function searches for a format in `formatList` containing the given `word` (case-insensitive). 
    If found, it extracts parts of the format specified by `newFormatOptions` (e.g., "first", "last", "middle" name components) 
    using regular expressions.  It then substitutes the found format with the extracted component in the original `emailFormat` (assumed to be a global variable).


    Args:
        word (str): The word to search for in the format list.
        formatList (list): A list of strings representing existing email formats.
        newFormatOptions (list, optional): A list of strings specifying the parts to extract from the found format (e.g., ["first", "last"]). Defaults to ["first", "last", "middle"].

    Returns:
        tuple: A tuple containing:
            - The found format string (str) from `formatList` or None if no matching format is found.
            - The new email format string (str) after substitution, or None if extraction fails or no matching format is found.

    Notes:
        The function uses regular expressions to extract parts of the format string.  The effectiveness depends heavily on the format of strings in `formatList` and the correctness of regular expressions implicitly assumed within `newFormatOptions`.


    Example:
        (Assuming a global variable `emailFormat = "John.Doe@example.com"`)

        getNewEmailFormat("two", ['first_two', 'last'], "[first_two][last]") 
        would return ('first_two', '[first][last]')

    """
    sequencing = [x for x in formatList if word.lower() in x.lower()]
    if sequencing:
        sequencingVar = sequencing[0]
        newWord = [re.findall(x, sequencingVar)[0] for x in newFormatOptions if re.findall(x, sequencingVar)]
        if newWord:
            newEmailFormat = re.sub(sequencingVar, newWord[0], emailFormat)
            return sequencingVar, newEmailFormat
        else:
            return sequencingVar, None
    
    else:
        return None, None
        
    
def generateEmailString(name:str, emailFormat:str, domain:str) -> (str|None):
    """
    constructs an email address based on a specified format using 
    parts of a person's name. It allows for flexibility in how the 
    name is represented (initials or first three letters) and 
    handles separators between name parts. 
    The final output is a well-formed email address that combines the 
    generated name parts with the provided domain.

    
    Generates an email address based on a specified format and a person's name.

    Args:
        name (str): The full name of the person.
        emailFormat (str): A string specifying the desired email format. 
            Use square brackets to denote placeholders for name parts, 
            and specify the desired format within the brackets:
            - `[first]`: Use the first name.
            - `[last]`: Use the last name.
            - `[first_initial]`: Use the first initial of the first name.
            - `[last_initial]`: Use the first initial of the last name.
            - `[first_three]`: Use the first three letters of the first name.
            - `[last_three]`: Use the first three letters of the last name.
            Use any non-bracket characters within the format string as separators.
        domain (str): The domain name for the email address.

    Returns:
        str or None: The generated email string if successful, otherwise None.  
                     Error messages are printed to the console if the name cannot be 
                     split or if there's an error during email string construction.
    
    Raises:
        NameError: If the email format specifies a middle name but one doesn't exist.

    Example:
        ```python
        name = "John Doe"
        emailFormat = "[first_initial][last]"
        domain = "@example.com"
        email = generateEmailString(name, emailFormat, domain)
        print(email)  # Output: JDoe@example.com
        ```
    
    """
    formatList, separator = _getFormatListAndSeperator(emailFormat)
    
    words = _getSequencingWords(formatList)
    
    first, middle, last = _splitName(name)

    
        
    if (first and last) or middle:
        wordList = ["initial", "two", "three", "four", "five"]
        wordOptions = dict(zip(wordList, [1, 2, 3, 4, 5]))
        
        newFirst, newLast, newMiddle = {}, {}, {}
        for word in words:
            for x in formatList:
                if word in x.lower():
                    if "first" in x.lower():
                        first = first[:wordOptions.get(word)]
                    elif "last" in x.lower():
                        last = last[:wordOptions.get(word)]
                    elif "middle" in x.lower():
                        if middle:
                            middle = middle[:wordOptions.get(word)]
                        else:
                            raise NameError("Middle name does not exist")

        #print(words)
        #print(formatList)
        
        pattern=re.compile("_"+"|_".join(words))
        
        newEmailFormat = pattern.sub("", emailFormat)
        #print(newEmailFormat)
        newFormatList = re.findall("\\[(.*?)\\]", newEmailFormat)
        #print(first, middle, last)
        if not middle and "middle" in formatList:
            raise NameError("Middle name does not exist")
        try:
            string = separator.join([eval(x).lower() for x in newFormatList if eval(x)])
        
            return f"{string}{domain}"
        except Exception as e:
            print(f"Error: {e}\nResults not found for: \n\t{words=}\n\t{formatList=}\n\t{newEmailFormat=}")
            return None
    else:
        print("Name cannot be split into first, last and middle names")
        return None
    
        
if __name__ == "__main__":
    name = input("Enter Name: ")
    emailFormat = input("Enter Email Format: ")
    domain = input("Enter required domain: ")
    try:
        print("Resulting Email Address: ", generateEmailString(name, emailFormat, domain))
    except Exception as e:
        print(f"Error: {e}")

