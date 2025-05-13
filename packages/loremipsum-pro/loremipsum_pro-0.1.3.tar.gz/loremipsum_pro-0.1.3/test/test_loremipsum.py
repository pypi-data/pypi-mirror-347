import unittest
import re
from loremipsum import LoremIpsum, loremIpsum


class TestLoremIpsum(unittest.TestCase):
    """Test cases for the LoremIpsum class and its singleton instance"""

    def test_init(self):
        """Test initialization with default and custom words"""
        # Test default initialization
        lorem = LoremIpsum()
        self.assertIsInstance(lorem.words, list)
        self.assertGreater(len(lorem.words), 0)
        
        # Test custom word list
        custom_words = ["test", "custom", "words"]
        lorem_custom = LoremIpsum(words=custom_words)
        self.assertEqual(lorem_custom.words, custom_words)
    
    def test_generate_words(self):
        """Test generating words with the LoremIpsum class"""
        # Test default
        words = loremIpsum.generateWords()
        self.assertIsInstance(words, str)
        self.assertEqual(len(words.split()), 10)  # Default is 10 words
        
        # Test with specific count
        count = 5
        words = loremIpsum.generateWords(count)
        self.assertEqual(len(words.split()), count)
        
        # Test with capitalization
        words = loremIpsum.generateWords(5, capitalize=True)
        for word in words.split():
            self.assertTrue(word[0].isupper())
        
        # Test with zero count
        words = loremIpsum.generateWords(0)
        self.assertEqual(words, "")
        
        # Test with negative count
        words = loremIpsum.generateWords(-1)
        self.assertEqual(words, "")
    
    def test_generate_bytes(self):
        """Test generating text with specific byte size"""
        # Test default
        text = loremIpsum.generateBytes()
        self.assertIsInstance(text, str)
        self.assertLessEqual(len(text.encode('utf-8')), 100)  # Default is 100 bytes
        
        # Test with specific byte count
        bytes_count = 50
        text = loremIpsum.generateBytes(bytes_count)
        self.assertLessEqual(len(text.encode('utf-8')), bytes_count)
        
        # Test with zero bytes
        text = loremIpsum.generateBytes(0)
        self.assertEqual(text, "")
    
    def test_generate_sentences(self):
        """Test generating sentences"""
        # Test default
        sentences = loremIpsum.generateSentences()
        self.assertIsInstance(sentences, str)
        self.assertEqual(len(re.findall(r'\.', sentences)), 3)  # Default is 3 sentences
        
        # Test with specific count
        count = 5
        sentences = loremIpsum.generateSentences(count)
        self.assertEqual(len(re.findall(r'\.', sentences)), count)
        
        # Test first letter capitalization and proper ending
        sentences = loremIpsum.generateSentences(1)
        self.assertTrue(sentences[0].isupper())
        self.assertTrue(sentences.endswith("."))
        
        # Test with zero count
        sentences = loremIpsum.generateSentences(0)
        self.assertEqual(sentences, "")
        
        # Test with negative count
        sentences = loremIpsum.generateSentences(-1)
        self.assertEqual(sentences, "")
    
    def test_generate_paragraphs(self):
        """Test generating paragraphs"""
        # Test default
        paragraphs = loremIpsum.generateParagraphs()
        self.assertIsInstance(paragraphs, str)
        self.assertEqual(len(paragraphs.split("\n\n")), 1)  # Default is 1 paragraph
        
        # Test with specific count
        count = 3
        paragraphs = loremIpsum.generateParagraphs(count)
        self.assertEqual(len(paragraphs.split("\n\n")), count)
        
        # Test with line breaks disabled
        paragraphs = loremIpsum.generateParagraphs(3, withLineBreaks=False)
        self.assertEqual(paragraphs.count("\n"), 0)  # No line breaks
        
        # Test with zero count
        paragraphs = loremIpsum.generateParagraphs(0)
        self.assertEqual(paragraphs, "")
        
        # Test with negative count
        paragraphs = loremIpsum.generateParagraphs(-1)
        self.assertEqual(paragraphs, "")
    
    def test_generate_list(self):
        """Test generating lists with different styles"""
        # Test default (bullet list with 5 items)
        list_text = loremIpsum.generateList()
        self.assertIsInstance(list_text, str)
        self.assertEqual(len(list_text.split("\n")), 5)  # Default is 5 items
        for line in list_text.split("\n"):
            self.assertTrue(line.startswith("• "))  # Default is bullet style
        
        # Test with bullet style explicit
        count = 3
        list_text = loremIpsum.generateList(count, style="bullet")
        self.assertEqual(len(list_text.split("\n")), count)
        for line in list_text.split("\n"):
            self.assertTrue(line.startswith("• "))
        
        # Test with number style
        list_text = loremIpsum.generateList(3, style="number")
        lines = list_text.split("\n")
        self.assertEqual(len(lines), 3)
        for i, line in enumerate(lines):
            self.assertTrue(line.startswith(f"{i+1}. "))
        
        # Test with none style
        list_text = loremIpsum.generateList(3, style="none")
        self.assertEqual(len(list_text.split("\n")), 3)
        for line in list_text.split("\n"):
            self.assertFalse(line.startswith("• "))
            self.assertFalse(re.match(r'^\d+\.', line))
        
        # Test capitalization of first letter in each item
        list_text = loremIpsum.generateList(1, style="none")
        self.assertTrue(list_text[0].isupper())
        
        # Test with zero count
        list_text = loremIpsum.generateList(0)
        self.assertEqual(list_text, "")
        
        # Test with negative count
        list_text = loremIpsum.generateList(-1)
        self.assertEqual(list_text, "")
    
    def test_singleton_instance(self):
        """Test that the singleton instance works properly"""
        from loremipsum import loremIpsum
        self.assertIsInstance(loremIpsum, LoremIpsum)
        
        # Generate some text to ensure it works
        text = loremIpsum.generateWords(5)
        self.assertIsInstance(text, str)
        self.assertEqual(len(text.split()), 5)


if __name__ == "__main__":
    unittest.main() 