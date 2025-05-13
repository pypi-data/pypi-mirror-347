# Lorem Ipsum Generator

A simple, lightweight, and flexible Lorem Ipsum text generator for python. Generate placeholder text in various formats including words, sentences, paragraphs, and lists.

Visit our website: [lorem ipsum generator](https://www.loremipsums.org)

## Features

- 🚀 Zero dependencies
- 📦 Lightweight (~2KB)
- 🎯 Multiple output formats
- 🌐 Online generator available at [www.loremipsums.org](https://www.loremipsums.org)

## Installation

```bash
pip install loremipsum
```

## Usage

This package provides two APIs:
1. The static `Lorem` class (original API)
2. The object-oriented `LoremIpsum` class with a pre-created `loremIpsum` instance (new API)

### Original API - Static Lorem Class

```python
from loremipsum import Lorem

# Generate a single random word
word = Lorem.word()
print(word)

# Generate multiple words
words = Lorem.words(5)
print(words)

# Generate a sentence (random word count between 3-15 if not specified)
sentence = Lorem.sentence()
print(sentence)
# Or with specific word count
sentence = Lorem.sentence(10)
print(sentence)

# Generate multiple sentences
sentences = Lorem.sentences(3)
print(sentences)

# Generate a paragraph (random sentence count between 3-7 if not specified)
paragraph = Lorem.paragraph()
print(paragraph)
# Or with specific sentence count
paragraph = Lorem.paragraph(5)
print(paragraph)

# Generate multiple paragraphs
paragraphs = Lorem.paragraphs(3)
print(paragraphs)
# Customize paragraph separator (default is "\n\n")
paragraphs = Lorem.paragraphs(3, separator="\n---\n")
print(paragraphs)
```

### New API - LoremIpsum Class

```python
from loremipsum import loremIpsum, LoremIpsum

# Use the pre-created singleton instance
# Generate words (default: 10 words)
text = loremIpsum.generateWords()
print(text)

# Generate words with capitalization
text = loremIpsum.generateWords(5, capitalize=True)
print(text)

# Generate text with specific byte size
text = loremIpsum.generateBytes(100)
print(f"{text} ({len(text.encode('utf-8'))} bytes)")

# Generate sentences (default: 3 sentences)
text = loremIpsum.generateSentences(3)
print(text)

# Generate paragraphs (default: 1 paragraph)
text = loremIpsum.generateParagraphs(2)
print(text)

# Generate paragraphs without line breaks
text = loremIpsum.generateParagraphs(2, withLineBreaks=False)
print(text)

# Generate a bullet list
text = loremIpsum.generateList(5, style="bullet")
print(text)

# Generate a numbered list
text = loremIpsum.generateList(5, style="number")
print(text)

# Generate a list with no formatting
text = loremIpsum.generateList(5, style="none")
print(text)

# Create a custom instance with your own words
custom_lorem = LoremIpsum(words=["hello", "world", "python", "programming"])
text = custom_lorem.generateSentences(2)
print(text)
```

## License

MIT

## Acknowledgements

This project was inspired by various Lorem Ipsum generators. 