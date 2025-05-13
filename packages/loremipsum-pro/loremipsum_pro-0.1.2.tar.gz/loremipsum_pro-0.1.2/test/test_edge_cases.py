import unittest
from loremipsum import Lorem, LoremIpsum, loremIpsum


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and error handling"""
    
    def test_zero_inputs(self):
        """Test behavior with zero counts"""
        # Test Lorem API with zero counts
        self.assertEqual(Lorem.words(0), "")
        self.assertEqual(Lorem.sentences(0), "")
        self.assertEqual(Lorem.paragraphs(0), "")
        
        # Test LoremIpsum API with zero counts
        self.assertEqual(loremIpsum.generateWords(0), "")
        self.assertEqual(loremIpsum.generateSentences(0), "")
        self.assertEqual(loremIpsum.generateParagraphs(0), "")
        self.assertEqual(loremIpsum.generateList(0), "")
        self.assertEqual(loremIpsum.generateBytes(0), "")
    
    def test_negative_inputs(self):
        """Test behavior with negative counts"""
        # Test Lorem API with negative counts
        self.assertEqual(Lorem.words(-5), "")
        self.assertEqual(Lorem.sentences(-5), "")
        self.assertEqual(Lorem.paragraphs(-5), "")
        
        # Test LoremIpsum API with negative counts
        self.assertEqual(loremIpsum.generateWords(-5), "")
        self.assertEqual(loremIpsum.generateSentences(-5), "")
        self.assertEqual(loremIpsum.generateParagraphs(-5), "")
        self.assertEqual(loremIpsum.generateList(-5), "")
        self.assertEqual(loremIpsum.generateBytes(-5), "")
    
    def test_large_inputs(self):
        """Test behavior with very large counts"""
        # Test with reasonably large values (not too large to cause memory issues)
        # These tests verify that large inputs don't crash the system
        
        # Lorem API
        words = Lorem.words(1000)
        self.assertEqual(len(words.split()), 1000)
        
        # Just check that these execute without error for large counts
        sentences = Lorem.sentences(100)
        self.assertIsInstance(sentences, str)
        self.assertGreater(len(sentences), 0)
        
        paragraphs = Lorem.paragraphs(50)
        self.assertIsInstance(paragraphs, str)
        self.assertGreater(len(paragraphs), 0)
        
        # LoremIpsum API
        words = loremIpsum.generateWords(1000)
        self.assertEqual(len(words.split()), 1000)
        
        sentences = loremIpsum.generateSentences(100)
        self.assertIsInstance(sentences, str)
        self.assertGreater(len(sentences), 0)
        
        paragraphs = loremIpsum.generateParagraphs(50)
        self.assertIsInstance(paragraphs, str)
        self.assertGreater(len(paragraphs), 0)
    
    def test_empty_custom_words(self):
        """Test behavior with empty custom word list"""
        # Create a custom instance with an empty word list
        custom_lorem = LoremIpsum(words=[])
        
        # Should handle empty word list gracefully
        self.assertEqual(custom_lorem.generateWords(5), "")
        self.assertEqual(custom_lorem.generateSentences(3), "")
        self.assertEqual(custom_lorem.generateParagraphs(2), "")
    
    def test_invalid_list_style(self):
        """Test behavior with invalid list style"""
        # Test with an unsupported style (should default to 'none')
        list_text = loremIpsum.generateList(3, style="invalid_style")
        self.assertEqual(len(list_text.split("\n")), 3)
        
        # Verify no bullet or number prefixes
        for line in list_text.split("\n"):
            self.assertFalse(line.startswith("• "))
            self.assertFalse(line.startswith("1. "))
    
    def test_whitespace_handling(self):
        """Test that generated text has proper whitespace"""
        # Test for no double spaces in words
        words = Lorem.words(100)
        self.assertNotIn("  ", words)
        
        words = loremIpsum.generateWords(100)
        self.assertNotIn("  ", words)
        
        # Test for no leading/trailing whitespace
        lorem_words = Lorem.words(5)
        self.assertEqual(lorem_words.strip(), lorem_words)
        
        loremipsum_words = loremIpsum.generateWords(5)
        self.assertEqual(loremipsum_words.strip(), loremipsum_words)


if __name__ == "__main__":
    unittest.main() 