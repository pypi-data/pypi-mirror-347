from itertools import product
from typing import Generator, Any
import re

def generatePermutations(
    templateString : str, 
    dataTypesList : list[str], 
    markerStr : str = "@"
    ) -> Generator[str, Any, None]:
    """
    Generates all permutations of a template string by replacing a marker string with
    elements from a list of data types.
    Args:
        templateString (str): The template string containing the marker.
        dataTypesList (list[str]): A list of data types to replace the marker.
        markerStr (str, optional): The marker string to be replaced. Defaults to "@".
        Yields:
        str: Each permutation of the template string with the marker replaced.
        
    Example:
        >>> template = "int @, float @, double @"
        >>> dataTypes = ["int", "float", "double"]
        >>> for perm in generatePermutations(template, dataTypes):
        ...     print(perm)
        int int float int double int
        int int float int double float
        int int float int double double
        int int float float double int
        int int float float double float
        int int float float double double
        int int float double double int
        int int float double double float
        int int float double double double
        int float float int double int
        int float float int double float
        int float float int double double
        int float float float double int
        int float float float double float
        int float float float double double
        int float float double double int
        int float float double double float
        int float float double double double
        int double float int double int
        int double float int double float
        int double float int double double
        int double float float double int
        int double float float double float
        int double float float double double
        int double float double double int
        int double float double double float
        int double float double double double
    """
    count = templateString.count(markerStr)
    if count == 0:
        raise ValueError("Marker String Not Found")
    for combo in product(dataTypesList, repeat=count):
        replacedString = templateString
        for replacement in combo:
            replacedString = replacedString.replace(markerStr, replacement, 1)
        yield replacedString


def generateGroupedPermutations(
    templateString: str,
    dataTypesList: list[str],
    markerStart: str = "@",
    markerEnd: str = "@"
    ) -> Generator[str, Any, None]:
    """
    Generates permutations by replacing grouped markers like `@placeholder@` where all
    instances of the same placeholder get the same value.
    
    Args:
        templateString: String containing markers (e.g., "int @T@, float @T@")
        dataTypesList: List of replacement values (e.g., ["int", "float"])
        markerStart: Start character for markers (default "@")
        markerEnd: End character for markers (default "@")
        
    Yields:
        All permutations with placeholders replaced
        
    Example:
        >>> template = "int @T@, float @T@, double @U@"
        >>> dataTypes = ["int", "float"]
        >>> for perm in generateGroupedPermutations(template, dataTypes):
        ...     print(perm)
        int int, float int, double int
        int int, float int, double float
        int int, float int, double double
        int float, float float, double int
        int float, float float, double float
        int float, float float, double double
        int double, float double, double int
        int double, float double, double float
        int double, float double, double double
    """
    pattern = re.compile(
        re.escape(markerStart) + r"([^" + re.escape(markerEnd) + r"]+)" + re.escape(markerEnd)
    )
    placeholders = pattern.findall(templateString)
    unique_placeholders = list(set(placeholders))
    if not unique_placeholders:
        raise ValueError("No valid markers found in template")
    for combo in product(dataTypesList, repeat=len(unique_placeholders)):
        mapping = dict(zip(unique_placeholders, combo))
        def replacer(match):
            ph = match.group(1)
            return mapping.get(ph, match.group(0))
        yield pattern.sub(replacer, templateString)