import os
import tempfile
import subprocess
from typing import Dict, List, Optional, Tuple, Union
from .data import *

class Bitrans:
    """
    Bi-directional translation/substitution tool.
    Python implementation of the original C code (bitrans.c).
    
    This class provides functionality for translating text using substitution rules.
    It can translate in both directions (forward and reverse) and can handle
    complex rule sets with multiple characters.
    
    Attributes:
        rules_dict: Dictionary containing translation rules
        bitdir: Translation direction (1=forward, 2=reverse)
        csep: Character used as placeholder for spaces
        camp: Ampersand character
        ndef: Number of rules
        input_patterns: List of input patterns
        output_patterns: List of output patterns
        pattern_lengths: List of pattern lengths
        ix: Sorting index for patterns
    
    Example:
        >>> from pyvoynich.bitrans import Bitrans
        >>> bitrans = Bitrans({'hello': 'world'})
        >>> bitrans.translate('hello')
        'world'
    """
    
    def __init__(self, rules_dict: Optional[Dict] = None, direction: int = 1):
        """
        Initialize the Bitrans object.
        
        Args:
            rules_dict: Dictionary containing translation rules. If None, uses STA_Eva_def by default.
            direction: Translation direction, must be 1 or 2. 
                       1 = left to right (key -> value)
                       2 = right to left (value -> key)
                       
        Raises:
            ValueError: If direction is not 1 or 2
        """
        self.rules_dict = rules_dict if rules_dict is not None else STA_Eva_def
        self.bitdir = direction  # Translation direction, must be 1 or 2
        if self.bitdir not in [1, 2]:
            raise ValueError("Direction must be 1 or 2")
            
        self.debr = 0    # Debugging output levels
        self.debs = 0
        self.strict = 0  # Be strict about matching transliteration alphabets
        self.csep = '#'  # The placeholder for spaces when matching
        self.camp = '&'  # The ampersand character
        self.poly = 0    # Rules file has homophonic records?
        
        # Initialize rules structures
        self.ndef = 0    # Number of definitions in the rules file
        self.ncom = 0    # Number of comment definitions in the rules file
        self.lcom = []   # Comment definitions
        
        # Process rules dictionary into internal format
        self.process_rules()
    
    @classmethod
    def from_file(cls, rules_file_path: str, direction: int = 1):
        """
        Create a Bitrans instance from a rules file.
        
        Args:
            rules_file_path: Path to the rules file
            direction: Translation direction (1 or 2)
            
        Returns:
            Bitrans instance
            
        Raises:
            FileNotFoundError: If the rules file doesn't exist
            ValueError: If the rules file has an invalid format
        """
        if not os.path.exists(rules_file_path):
            raise FileNotFoundError(f"Rules file not found: {rules_file_path}")
            
        rules_dict = cls.load_rules_from_file(rules_file_path)
        return cls(rules_dict, direction)
    
    @staticmethod
    def load_rules_from_file(rules_file_path: str) -> Dict[str, str]:
        """
        Load rules from a file.
        
        Args:
            rules_file_path: Path to the rules file
            
        Returns:
            Dictionary of rules
            
        Raises:
            ValueError: If the rules file has an invalid format
        """
        rules_dict = {}
        
        try:
            with open(rules_file_path, 'r', encoding='utf-8') as f:
                # Skip header line
                header = f.readline().strip()
                if not header.startswith('#=BIT'):
                    raise ValueError(f"Invalid rules file header: {header}")
                    
                # Process rules
                line_num = 1
                for line in f:
                    line_num += 1
                    line = line.strip()
                    if not line or line.startswith('#=') or line.startswith('------'):
                        continue
                        
                    parts = line.split()
                    if len(parts) >= 2:
                        # First part is the input, rest are outputs
                        input_token = parts[0]
                        output_token = parts[1]
                        rules_dict[input_token] = output_token
                    else:
                        # Skip lines that don't have enough parts
                        continue
        except Exception as e:
            raise ValueError(f"Error reading rules file: {e}")
        
        if not rules_dict:
            raise ValueError("No valid rules found in the rules file")
            
        return rules_dict
        
    def process_rules(self):
        """
        Process the rules dictionary into the internal format used by bitrans.
        
        This method converts the rules dictionary into lists of input and output patterns,
        and sorts them by length for efficient matching.
        """
        # Initialize structures
        self.input_patterns = []
        self.output_patterns = []
        self.pattern_lengths = []
        
        # Process each rule
        if self.bitdir == 1:
            # Normal direction: key -> value
            for key, value in self.rules_dict.items():
                self.input_patterns.append(key)
                self.output_patterns.append(value)
                self.pattern_lengths.append(len(key))
                self.ndef += 1
        else:
            # Reverse direction: value -> key
            for key, value in self.rules_dict.items():
                self.input_patterns.append(value)
                self.output_patterns.append(key)
                self.pattern_lengths.append(len(value))
                self.ndef += 1
            
        # Create sorting index based on pattern length (longest first)
        self.ix = list(range(self.ndef))
        self.ix.sort(key=lambda i: self.pattern_lengths[i], reverse=True)
    
    def prepare_line(self, text: str) -> Tuple[str, List[str], List[str]]:
        """
        Prepare the line for processing.
        
        Args:
            text: Input text to prepare
            
        Returns:
            Tuple of (text, modt, spcs) where:
                text: The text with spaces replaced by csep
                modt: Marks which characters are in comments
                spcs: Original spacing characters
        """
        # Add a space at the start and end
        text = ' ' + text + ' '
        
        # Initialize modt (modification tracking) and spcs (spaces)
        modt = [' '] * len(text)
        spcs = [' '] * len(text)
        
        # Convert text to list for easier manipulation
        text_list = list(text)
        
        # Process the text
        for jj in range(len(text_list)):
            ch = text_list[jj]
            
            # Handle spaces and separators
            if ch == ' ' or ch == '.' or ch == ',':
                spcs[jj] = ch
                text_list[jj] = self.csep
            else:
                spcs[jj] = '+'
                
            # Handle original instances of the separator
            if ch == self.csep:
                spcs[jj] = self.csep
                modt[jj] = '-'
                
        return ''.join(text_list), modt, spcs
    
    def process_line(self, text: str, modt: List[str], spcs: List[str]) -> Tuple[str, List[str], List[str]]:
        """
        Perform all substitutions on the line.
        
        Args:
            text: The text to process
            modt: Modification tracking list
            spcs: Spaces tracking list
            
        Returns:
            Tuple of (text, modt, spcs) after processing
        """
        text_list = list(text)
        
        # For each rule in sorted order
        for idx in self.ix:
            input_pattern = self.input_patterns[idx]
            output_pattern = self.output_patterns[idx]
            input_len = len(input_pattern)
            output_len = len(output_pattern)
            
            # Search for the pattern in the text
            pos = 0
            while pos <= len(text_list) - input_len:
                # Check if the pattern matches at this position
                if ''.join(text_list[pos:pos+input_len]) == input_pattern:
                    # Check if this part is free to modify
                    isfree = True
                    sepkeep = ' '  # Default separator
                    
                    for jj in range(input_len):
                        if modt[pos + jj] != ' ':
                            isfree = False
                            break
                        if text_list[pos + jj] == self.csep:
                            sepkeep = spcs[pos + jj]
                    
                    if isfree:
                        # Calculate length difference
                        dlen = output_len - input_len
                        
                        if dlen > 0:
                            # Insert space if output is longer
                            text_list[pos+input_len:pos+input_len] = [''] * dlen
                            modt[pos+input_len:pos+input_len] = [' '] * dlen
                            spcs[pos+input_len:pos+input_len] = [' '] * dlen
                        elif dlen < 0:
                            # Remove characters if output is shorter
                            del text_list[pos+output_len:pos+input_len]
                            del modt[pos+output_len:pos+input_len]
                            del spcs[pos+output_len:pos+input_len]
                        
                        # Replace with output pattern
                        for jj in range(output_len):
                            text_list[pos + jj] = output_pattern[jj]
                            if output_pattern[jj] == self.csep:
                                spcs[pos + jj] = sepkeep
                            else:
                                spcs[pos + jj] = ' '
                                modt[pos + jj] = '-'
                        
                        # Skip ahead past this replacement
                        pos += output_len
                    else:
                        pos += 1
                else:
                    pos += 1
        
        return ''.join(text_list), modt, spcs
    
    def output_line(self, text: str, modt: List[str], spcs: List[str]) -> str:
        """
        Format the processed line for output.
        
        Args:
            text: Processed text
            modt: Modification tracking list
            spcs: Spaces tracking list
            
        Returns:
            Formatted output string
        """
        result = []
        text_list = list(text)
        
        # Skip the first and last space that we added
        for jj in range(1, len(text_list) - 1):
            ch = text_list[jj]
            if modt[jj] == ' ' and ch == self.csep:
                ch = spcs[jj]
            result.append(ch)
            
        return ''.join(result)
    
    def translate(self, input_text: str) -> str:
        """
        Translate the input text using the rules.
        
        Args:
            input_text: The text to translate
            
        Returns:
            Translated text
        """
        if not input_text:
            return ""
            
        lines = input_text.splitlines()
        result_lines = []
        
        for line in lines:
            # Skip empty lines
            if not line.strip():
                result_lines.append('')
                continue
                
            # Process the line
            text, modt, spcs = self.prepare_line(line)
            text, modt, spcs = self.process_line(text, modt, spcs)
            result = self.output_line(text, modt, spcs)
            result_lines.append(result)
            
        return '\n'.join(result_lines)
    
    def create_rules_file(self, output_path: str):
        """
        Create a rules file from the current rules dictionary.
        
        Args:
            output_path: Path to save the rules file
            
        Raises:
            IOError: If the file cannot be written
        """
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                # Write header
                f.write("#=BIT  \n")
                
                # Write rules
                for i in range(self.ndef):
                    input_pattern = self.input_patterns[i]
                    output_pattern = self.output_patterns[i]
                    f.write(f"{input_pattern} {output_pattern}\n")
        except Exception as e:
            raise IOError(f"Error writing rules file: {e}")
    
    def reverse_direction(self):
        """
        Reverse the translation direction.
        
        This method swaps the input and output patterns, effectively reversing
        the translation direction.
        """
        self.bitdir = 3 - self.bitdir  # Toggle between 1 and 2
        
        # Swap input and output patterns
        self.input_patterns, self.output_patterns = self.output_patterns, self.input_patterns
        
        # Recalculate pattern lengths and sorting
        for i in range(self.ndef):
            self.pattern_lengths[i] = len(self.input_patterns[i])
        
        # Re-sort
        self.ix = list(range(self.ndef))
        self.ix.sort(key=lambda i: self.pattern_lengths[i], reverse=True)
        
    def __str__(self):
        """Return a string representation of the Bitrans object."""
        direction = "forward" if self.bitdir == 1 else "reverse"
        return f"Bitrans(rules={len(self.rules_dict)}, direction={direction})"
        
    def __repr__(self):
        """Return a string representation of the Bitrans object."""
        return self.__str__()
