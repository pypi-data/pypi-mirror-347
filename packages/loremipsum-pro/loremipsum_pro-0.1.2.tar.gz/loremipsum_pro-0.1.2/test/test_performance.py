import unittest
import time
from loremipsum import Lorem, loremIpsum


class TestPerformance(unittest.TestCase):
    """Performance tests for the loremipsum package"""
    
    def measure_execution_time(self, func, *args, **kwargs):
        """Measure execution time of a function"""
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        return result, (end_time - start_time)
    
    def test_word_generation_performance(self):
        """Compare performance of word generation between APIs"""
        num_words = 1000
        
        # Measure time for Lorem.words
        _, lorem_time = self.measure_execution_time(Lorem.words, num_words)
        
        # Measure time for loremIpsum.generateWords
        _, loremipsum_time = self.measure_execution_time(loremIpsum.generateWords, num_words)
        
        print(f"\nPerformance - Generate {num_words} words:")
        print(f"Lorem.words: {lorem_time:.6f} seconds")
        print(f"loremIpsum.generateWords: {loremipsum_time:.6f} seconds")
        
        # We don't assert on exact times, just that both complete in reasonable time
        self.assertLess(lorem_time, 1.0, "Lorem.words took too long")
        self.assertLess(loremipsum_time, 1.0, "loremIpsum.generateWords took too long")
    
    def test_paragraph_generation_performance(self):
        """Compare performance of paragraph generation between APIs"""
        num_paragraphs = 100
        
        # Measure time for Lorem.paragraphs
        _, lorem_time = self.measure_execution_time(Lorem.paragraphs, num_paragraphs)
        
        # Measure time for loremIpsum.generateParagraphs
        _, loremipsum_time = self.measure_execution_time(loremIpsum.generateParagraphs, num_paragraphs)
        
        print(f"\nPerformance - Generate {num_paragraphs} paragraphs:")
        print(f"Lorem.paragraphs: {lorem_time:.6f} seconds")
        print(f"loremIpsum.generateParagraphs: {loremipsum_time:.6f} seconds")
        
        # We don't assert on exact times, just that both complete in reasonable time
        self.assertLess(lorem_time, 2.0, "Lorem.paragraphs took too long")
        self.assertLess(loremipsum_time, 2.0, "loremIpsum.generateParagraphs took too long")
    
    def test_large_text_generation(self):
        """Test performance of generating large amounts of text"""
        # Generate 1MB of text with Lorem
        num_paragraphs = 100
        
        print("\nGenerating large text with Lorem.paragraphs...")
        start_time = time.time()
        text = Lorem.paragraphs(num_paragraphs)
        end_time = time.time()
        text_size = len(text.encode('utf-8')) / 1024  # Size in KB
        
        print(f"Generated {text_size:.2f} KB in {end_time - start_time:.6f} seconds")
        
        # Generate approximately same amount with loremIpsum
        print("\nGenerating large text with loremIpsum.generateParagraphs...")
        start_time = time.time()
        text = loremIpsum.generateParagraphs(num_paragraphs)
        end_time = time.time()
        text_size = len(text.encode('utf-8')) / 1024  # Size in KB
        
        print(f"Generated {text_size:.2f} KB in {end_time - start_time:.6f} seconds")
    
    def test_bytes_generation_performance(self):
        """Test performance of generateBytes method"""
        bytes_size = 10240  # 10KB
        
        print(f"\nGenerating exactly {bytes_size} bytes with loremIpsum.generateBytes...")
        start_time = time.time()
        text = loremIpsum.generateBytes(bytes_size)
        end_time = time.time()
        actual_size = len(text.encode('utf-8'))
        
        print(f"Generated {actual_size} bytes in {end_time - start_time:.6f} seconds")
        self.assertLessEqual(actual_size, bytes_size)


if __name__ == "__main__":
    unittest.main() 