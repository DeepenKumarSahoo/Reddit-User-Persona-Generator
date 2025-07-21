# Reddit User Persona Generator

A Python script that scrapes Reddit user profiles and generates comprehensive user personas based on their posts and comments. This tool analyzes user behavior, interests, communication patterns, and other characteristics to create detailed personality profiles.

## 🎯 Features

- **Comprehensive Analysis**: Analyzes demographics, interests, personality traits, communication style, lifestyle preferences, values, online behavior, and technical proficiency
- **Citation System**: Provides evidence and citations for each persona characteristic
- **Flexible Input**: Accepts various Reddit URL formats
- **Detailed Output**: Generates structured text files with complete persona analysis
- **Rate Limiting**: Respects Reddit's rate limits to avoid blocking
- **Error Handling**: Robust error handling for network issues and malformed data

## 📋 Requirements

### Python Version
- Python 3.7 or higher

### Required Libraries
```bash
pip install requests
```

### Standard Library Dependencies
The following standard library modules are used (no installation required):
- `json`
- `time`
- `re`
- `os`
- `datetime`
- `typing`
- `dataclasses`
- `argparse`

## 🚀 Installation

1. **Clone or download the repository**
```bash
git clone <your-repository-url>
cd reddit-persona-generator
```

2. **Install required dependencies**
```bash
pip install requests
```

3. **Verify Python version**
```bash
python --version  # Should be 3.7+
```

## 💻 Usage

### Basic Usage

```bash
python reddit_persona_generator.py <reddit_profile_url>
```

### Examples with Sample URLs

```bash
# Analyze the first sample user
python reddit_persona_generator.py https://www.reddit.com/user/kojied/

# Analyze the second sample user  
python reddit_persona_generator.py https://www.reddit.com/user/Hungry-Move-6603/

# Specify custom output filename
python reddit_persona_generator.py https://www.reddit.com/user/kojied/ -o my_analysis.txt

# Limit analysis to 50 posts/comments
python reddit_persona_generator.py https://www.reddit.com/user/kojied/ -l 50
```

### Command Line Options

- `profile_url` (required): Reddit user profile URL
- `-o, --output`: Custom output filename (default: username_persona.txt)  
- `-l, --limit`: Limit number of posts/comments to analyze (default: 100)
- `-h, --help`: Show help message

### Supported URL Formats

The script accepts various Reddit URL formats:
```
https://www.reddit.com/user/username/
https://reddit.com/user/username
https://www.reddit.com/u/username/
https://reddit.com/u/username
```

## 📊 Output Format

The script generates a comprehensive text file containing:

1. **User Overview** - Basic statistics and most active subreddits
2. **Demographics** - Age, location, occupation indicators  
3. **Interests & Hobbies** - Technology, gaming, fitness, entertainment, etc.
4. **Personality Traits** - Communication style, sentiment analysis
5. **Communication Style** - Tone, formality, engagement patterns
6. **Lifestyle Preferences** - Health, food, travel, home preferences
7. **Values & Beliefs** - Privacy, environment, community orientation
8. **Online Behavior** - Posting patterns, content reception
9. **Technical Proficiency** - Programming languages, tools, concepts
10. **Citations & Evidence** - Source links and evidence for all claims

## 🔧 Technical Details

### How It Works

1. **URL Parsing**: Extracts username from various Reddit URL formats
2. **Data Scraping**: Uses Reddit's JSON API to fetch user posts and comments
3. **Content Analysis**: Applies pattern matching and keyword analysis
4. **Persona Generation**: Categorizes findings into persona dimensions
5. **Citation Tracking**: Records evidence sources for all characteristics
6. **Output Formatting**: Generates structured, readable text reports

### API Usage

- Uses Reddit's public JSON endpoints (no authentication required)
- Respects rate limits with built-in delays
- Handles various error conditions gracefully
- Works with publicly available data only

### Data Analysis Methods

- **Keyword Pattern Matching**: Identifies interests and technical skills
- **Sentiment Analysis**: Analyzes positive/negative language patterns  
- **Activity Pattern Analysis**: Studies posting frequency and engagement
- **Subreddit Participation**: Maps activity to interest categories
- **Communication Style Analysis**: Evaluates formality and tone

## 🛠️ Troubleshooting

### Common Issues

**1. "No data found for user"**
- User may have deleted their account
- User may have no public posts/comments
- User profile may be private or suspended

**2. "Could not extract username from URL"**
- Check URL format is correct
- Ensure URL contains valid Reddit username
- Try different URL format variations

**3. "Error fetching data"**  
- Check internet connection
- Reddit may be temporarily unavailable
- Rate limiting may be in effect (wait and retry)

**4. "Permission denied" when saving file**
- Check write permissions in current directory
- Specify different output location with -o flag

### Rate Limiting

- Script includes automatic delays between requests
- If you hit rate limits, wait a few minutes and retry
- For multiple analyses, add delays between executions

### Debug Mode

Add print statements or modify the script to enable debug output:
```python
# Add after line imports
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 📁 Sample Output Files

This repository includes sample output files:

- `kojied_persona.txt` - Analysis of https://www.reddit.com/user/kojied/
- `Hungry-Move-6603_persona.txt` - Analysis of https://www.reddit.com/user/Hungry-Move-6603/

These demonstrate the expected output format and analysis depth.

## ⚖️ Legal & Ethical Considerations

- **Public Data Only**: Only analyzes publicly available Reddit posts/comments
- **No Authentication**: Does not require login or access private data
- **Respectful Usage**: Includes rate limiting to avoid overloading Reddit's servers
- **Educational Purpose**: Designed for learning and analysis, not harassment
- **No Data Storage**: Does not store user data beyond the generated report

## 📝 Code Quality

- **PEP-8 Compliant**: Follows Python style guidelines
- **Type Hints**: Uses Python type hints for better code documentation
- **Error Handling**: Comprehensive error handling and user feedback
- **Modular Design**: Clean separation of concerns across classes
- **Documentation**: Well-documented with docstrings and comments

## 🚀 Future Enhancements

Potential improvements for future versions:

- **Advanced NLP**: Integration with NLTK or spaCy for better text analysis
- **Machine Learning**: Use trained models for personality prediction
- **Visualization**: Generate charts and graphs for persona data
- **Multiple Users**: Batch processing of multiple users
- **Export Formats**: Support for JSON, CSV, PDF outputs
- **Web Interface**: Create web-based version of the tool

## 📞 Support

For issues or questions:

1. Check the troubleshooting section above
2. Review sample output files for expected format
3. Ensure all requirements are properly installed
4. Verify Reddit URLs are accessible and valid

## 🏆 Assignment Compliance

This project meets all assignment requirements:

- ✅ Takes Reddit user profile URL as input
- ✅ Scrapes comments and posts from the user
- ✅ Builds comprehensive user persona  
- ✅ Outputs persona to text file
- ✅ Provides citations for each characteristic
- ✅ Includes executable Python script
- ✅ Contains sample output files for both test users
- ✅ Follows PEP-8 guidelines
- ✅ Includes detailed README with setup instructions

## 📄 License

This project is created for educational purposes as part of an internship assignment. The code is provided as-is for evaluation purposes.