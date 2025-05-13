import unittest
import re
from loremipsum import Lorem

class TestLorem(unittest.TestCase):
    """Test cases for the Lorem static class"""

    def test_word(self):
        """Test generating a single word"""
        word = Lorem.word()
        self.assertIsInstance(word, str)
        self.assertTrue(len(word) > 0)
        # Test that the word is in the predefined list
        self.assertIn(word, Lorem._WORDS)

    def test_words(self):
        """Test generating multiple words"""
        # Test default
        words = Lorem.words()
        self.assertIsInstance(words, str)
        self.assertEqual(len(words.split()), 1)

        # Test with specific count
        count = 5
        words = Lorem.words(count)
        self.assertEqual(len(words.split()), count)

        # Test with zero count
        words = Lorem.words(0)
        self.assertEqual(words, "")

        # Test with negative count
        words = Lorem.words(-1)
        self.assertEqual(words, "")

    def test_sentence(self):
        """Test sentence generation"""
        # Test default random length
        sentence = Lorem.sentence()
        self.assertIsInstance(sentence, str)
        # Check capitalization and period
        self.assertTrue(sentence[0].isupper())
        self.assertTrue(sentence.endswith("."))

        # Test with specific word count
        word_count = 10
        sentence = Lorem.sentence(word_count)
        self.assertEqual(len(sentence.split()), word_count)
        self.assertTrue(sentence[0].isupper())
        self.assertTrue(sentence.endswith("."))

    def test_sentences(self):
        """Test multiple sentences generation"""
        # Test default (1 sentence)
        sentences = Lorem.sentences()
        self.assertIsInstance(sentences, str)
        self.assertEqual(len(re.findall(r'\.', sentences)), 1)

        # Test specific count
        count = 3
        sentences = Lorem.sentences(count)
        self.assertEqual(len(re.findall(r'\.', sentences)), count)

        # Test with zero count
        sentences = Lorem.sentences(0)
        self.assertEqual(sentences, "")

        # Test with negative count
        sentences = Lorem.sentences(-1)
        self.assertEqual(sentences, "")

    def test_paragraph(self):
        """Test paragraph generation"""
        # Default random sentence count
        paragraph = Lorem.paragraph()
        self.assertIsInstance(paragraph, str)
        # Ensure at least one sentence
        self.assertGreaterEqual(len(re.findall(r'\.', paragraph)), 1)

        # Test with specific sentence count
        sentence_count = 5
        paragraph = Lorem.paragraph(sentence_count)
        self.assertEqual(len(re.findall(r'\.', paragraph)), sentence_count)

    def test_paragraphs(self):
        """Test multiple paragraphs generation"""
        # Test default (1 paragraph)
        paragraphs = Lorem.paragraphs()
        self.assertIsInstance(paragraphs, str)
        
        # Test specific count with default separator
        count = 3
        paragraphs = Lorem.paragraphs(count)
        self.assertEqual(len(paragraphs.split("\n\n")), count)
        
        # Test with custom separator
        separator = "\n---\n"
        paragraphs = Lorem.paragraphs(count, separator)
        self.assertEqual(len(paragraphs.split(separator)), count)

        # Test with zero count
        paragraphs = Lorem.paragraphs(0)
        self.assertEqual(paragraphs, "")

        # Test with negative count
        paragraphs = Lorem.paragraphs(-1)
        self.assertEqual(paragraphs, "")


if __name__ == "__main__":
    unittest.main() 