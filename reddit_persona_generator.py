#!/usr/bin/env python3
"""
Reddit User Persona Generator
A script that scrapes Reddit user profiles and generates comprehensive user personas
based on their posts and comments.

Author: AI Assistant
Date: July 2025
"""

import requests
import json
import time
import re
import os
from datetime import datetime
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
import argparse


@dataclass
class RedditPost:
    """Data structure to hold Reddit post information"""
    title: str
    content: str
    subreddit: str
    score: int
    created_utc: float
    url: str
    post_type: str  # 'post' or 'comment'


class RedditScraper:
    """Handles scraping of Reddit user data"""
    
    def __init__(self, user_agent: str = "UserPersonaBot/1.0"):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': user_agent
        })
        self.base_url = "https://www.reddit.com"
    
    def extract_username(self, profile_url: str) -> str:
        """Extract username from Reddit profile URL"""
        # Handle various URL formats
        patterns = [
            r'reddit\.com/user/([^/]+)',
            r'reddit\.com/u/([^/]+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, profile_url)
            if match:
                return match.group(1)
        
        raise ValueError(f"Could not extract username from URL: {profile_url}")
    
    def get_user_data(self, username: str, limit: int = 100) -> Tuple[List[RedditPost], Dict]:
        """Fetch user posts and comments"""
        posts = []
        user_info = {}
        
        # Get user overview (posts + comments)
        overview_url = f"{self.base_url}/user/{username}.json?limit={limit}"
        
        try:
            response = self.session.get(overview_url)
            response.raise_for_status()
            data = response.json()
            
            if 'data' not in data or 'children' not in data['data']:
                print(f"Warning: No data found for user {username}")
                return posts, user_info
            
            # Extract user info from first post/comment
            if data['data']['children']:
                first_item = data['data']['children'][0]['data']
                user_info = {
                    'username': username,
                    'account_created': first_item.get('created_utc', 0),
                    'total_karma': first_item.get('total_karma', 0)
                }
            
            # Process each post/comment
            for item in data['data']['children']:
                item_data = item['data']
                
                # Determine if it's a post or comment
                post_type = 'comment' if 'body' in item_data else 'post'
                
                if post_type == 'post':
                    content = f"{item_data.get('title', '')} {item_data.get('selftext', '')}"
                else:
                    content = item_data.get('body', '')
                
                # Skip deleted/removed content
                if content.lower() in ['[deleted]', '[removed]', '']:
                    continue
                
                post = RedditPost(
                    title=item_data.get('title', ''),
                    content=content,
                    subreddit=item_data.get('subreddit', ''),
                    score=item_data.get('score', 0),
                    created_utc=item_data.get('created_utc', 0),
                    url=f"https://reddit.com{item_data.get('permalink', '')}",
                    post_type=post_type
                )
                posts.append(post)
                
            print(f"Successfully scraped {len(posts)} posts/comments for user {username}")
            
        except requests.RequestException as e:
            print(f"Error fetching data for user {username}: {e}")
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON response: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")
        
        return posts, user_info
    
    def rate_limit_delay(self, delay: float = 1.0):
        """Add delay to respect rate limits"""
        time.sleep(delay)


class PersonaGenerator:
    """Generates user persona from scraped Reddit data"""
    
    def __init__(self):
        self.persona_categories = {
            'demographics': [],
            'interests': [],
            'personality_traits': [],
            'communication_style': [],
            'lifestyle': [],
            'values_beliefs': [],
            'online_behavior': [],
            'technical_proficiency': []
        }
    
    def analyze_content(self, posts: List[RedditPost], user_info: Dict) -> Dict:
        """Analyze posts to generate user persona"""
        persona = {
            'user_overview': self._generate_user_overview(posts, user_info),
            'demographics': self._analyze_demographics(posts),
            'interests_hobbies': self._analyze_interests(posts),
            'personality_traits': self._analyze_personality(posts),
            'communication_style': self._analyze_communication_style(posts),
            'lifestyle_preferences': self._analyze_lifestyle(posts),
            'values_beliefs': self._analyze_values(posts),
            'online_behavior': self._analyze_online_behavior(posts),
            'technical_proficiency': self._analyze_technical_skills(posts)
        }
        
        return persona
    
    def _generate_user_overview(self, posts: List[RedditPost], user_info: Dict) -> Dict:
        """Generate basic user overview"""
        if not posts:
            return {"summary": "Limited data available for analysis"}
        
        # Calculate basic stats
        total_posts = len([p for p in posts if p.post_type == 'post'])
        total_comments = len([p for p in posts if p.post_type == 'comment'])
        avg_score = sum(p.score for p in posts) / len(posts) if posts else 0
        
        # Find most active subreddits
        subreddit_activity = {}
        for post in posts:
            subreddit = post.subreddit
            if subreddit:
                subreddit_activity[subreddit] = subreddit_activity.get(subreddit, 0) + 1
        
        top_subreddits = sorted(subreddit_activity.items(), key=lambda x: x[1], reverse=True)[:5]
        
        return {
            "username": user_info.get('username', 'Unknown'),
            "total_posts": total_posts,
            "total_comments": total_comments,
            "average_score": round(avg_score, 2),
            "most_active_subreddits": [sub[0] for sub in top_subreddits],
            "activity_summary": f"Active user with {total_posts} posts and {total_comments} comments"
        }
    
    def _analyze_demographics(self, posts: List[RedditPost]) -> Dict:
        """Analyze demographic indicators from posts"""
        indicators = {
            'age_indicators': [],
            'location_indicators': [],
            'occupation_indicators': [],
            'education_indicators': []
        }
        citations = []
        
        # Age-related keywords
        age_keywords = {
            'young': ['college', 'university', 'student', 'freshman', 'sophomore'],
            'adult': ['job', 'work', 'career', 'mortgage', 'marriage', 'kids'],
            'senior': ['retirement', 'grandkids', 'pension']
        }
        
        # Location keywords (countries, cities, regions)
        location_keywords = ['USA', 'Canada', 'UK', 'Australia', 'Germany', 'France', 
                           'California', 'Texas', 'New York', 'London', 'Toronto']
        
        for post in posts:
            content_lower = post.content.lower()
            
            # Check for age indicators
            for age_group, keywords in age_keywords.items():
                for keyword in keywords:
                    if keyword in content_lower:
                        indicators['age_indicators'].append(f"Likely {age_group} based on '{keyword}' usage")
                        citations.append({
                            'category': 'demographics',
                            'indicator': f"Age group: {age_group}",
                            'evidence': keyword,
                            'source_url': post.url,
                            'source_type': post.post_type
                        })
                        break
            
            # Check for location indicators
            for location in location_keywords:
                if location.lower() in content_lower:
                    indicators['location_indicators'].append(f"Possible location: {location}")
                    citations.append({
                        'category': 'demographics',
                        'indicator': f"Location: {location}",
                        'evidence': f"Mentioned '{location}'",
                        'source_url': post.url,
                        'source_type': post.post_type
                    })
        
        return {
            'analysis': indicators,
            'citations': citations
        }
    
    def _analyze_interests(self, posts: List[RedditPost]) -> Dict:
        """Analyze user interests and hobbies"""
        interests = {}
        citations = []
        
        # Interest categories based on subreddit patterns
        interest_mapping = {
            'technology': ['programming', 'tech', 'software', 'coding', 'python', 'javascript'],
            'gaming': ['gaming', 'games', 'xbox', 'playstation', 'nintendo', 'steam'],
            'fitness': ['fitness', 'gym', 'workout', 'running', 'bodybuilding'],
            'finance': ['investing', 'stocks', 'crypto', 'bitcoin', 'finance', 'money'],
            'entertainment': ['movies', 'tv', 'netflix', 'music', 'books', 'reading'],
            'lifestyle': ['cooking', 'food', 'travel', 'photography', 'art']
        }
        
        # Count subreddit participation
        subreddit_counts = {}
        for post in posts:
            if post.subreddit:
                subreddit = post.subreddit.lower()
                subreddit_counts[subreddit] = subreddit_counts.get(subreddit, 0) + 1
        
        # Map subreddits to interest categories
        for category, keywords in interest_mapping.items():
            category_score = 0
            evidence = []
            
            for subreddit, count in subreddit_counts.items():
                for keyword in keywords:
                    if keyword in subreddit:
                        category_score += count
                        evidence.append(f"r/{subreddit} ({count} posts)")
                        
                        # Add citation
                        relevant_posts = [p for p in posts if p.subreddit.lower() == subreddit][:3]
                        for rp in relevant_posts:
                            citations.append({
                                'category': 'interests',
                                'indicator': f"Interest in {category}",
                                'evidence': f"Active in r/{subreddit}",
                                'source_url': rp.url,
                                'source_type': rp.post_type
                            })
            
            if category_score > 0:
                interests[category] = {
                    'strength': 'High' if category_score > 10 else 'Medium' if category_score > 3 else 'Low',
                    'evidence': evidence[:5]  # Limit evidence
                }
        
        return {
            'analysis': interests,
            'citations': citations
        }
    
    def _analyze_personality(self, posts: List[RedditPost]) -> Dict:
        """Analyze personality traits from communication patterns"""
        traits = {}
        citations = []
        
        if not posts:
            return {'analysis': traits, 'citations': citations}
        
        # Analyze content patterns
        total_words = 0
        question_count = 0
        exclamation_count = 0
        positive_words = ['good', 'great', 'awesome', 'love', 'like', 'amazing', 'excellent']
        negative_words = ['bad', 'hate', 'terrible', 'awful', 'stupid', 'annoying']
        
        positive_count = 0
        negative_count = 0
        
        for post in posts:
            content = post.content
            words = len(content.split())
            total_words += words
            
            question_count += content.count('?')
            exclamation_count += content.count('!')
            
            content_lower = content.lower()
            for word in positive_words:
                positive_count += content_lower.count(word)
            for word in negative_words:
                negative_count += content_lower.count(word)
        
        avg_words_per_post = total_words / len(posts) if posts else 0
        
        # Determine traits based on patterns
        if avg_words_per_post > 50:
            traits['communication_style'] = 'Detailed and expressive'
            citations.append({
                'category': 'personality',
                'indicator': 'Detailed communication style',
                'evidence': f'Average {avg_words_per_post:.1f} words per post',
                'source_url': 'Overall pattern analysis',
                'source_type': 'aggregate'
            })
        
        if positive_count > negative_count * 2:
            traits['sentiment'] = 'Generally positive and optimistic'
        elif negative_count > positive_count:
            traits['sentiment'] = 'More critical or analytical'
        else:
            traits['sentiment'] = 'Balanced emotional expression'
        
        if question_count > len(posts) * 0.3:
            traits['engagement_style'] = 'Inquisitive and engaging'
        
        return {
            'analysis': traits,
            'citations': citations
        }
    
    def _analyze_communication_style(self, posts: List[RedditPost]) -> Dict:
        """Analyze how the user communicates"""
        style_analysis = {}
        citations = []
        
        if not posts:
            return {'analysis': style_analysis, 'citations': citations}
        
        # Analyze formality, tone, etc.
        formal_indicators = ['furthermore', 'however', 'therefore', 'consequently']
        informal_indicators = ['lol', 'omg', 'wtf', 'tbh', 'imo']
        
        formal_count = 0
        informal_count = 0
        
        for post in posts:
            content_lower = post.content.lower()
            
            for indicator in formal_indicators:
                if indicator in content_lower:
                    formal_count += 1
            
            for indicator in informal_indicators:
                if indicator in content_lower:
                    informal_count += 1
        
        if formal_count > informal_count:
            style_analysis['tone'] = 'Formal and professional'
        elif informal_count > formal_count:
            style_analysis['tone'] = 'Casual and informal'
        else:
            style_analysis['tone'] = 'Mixed formal and informal'
        
        return {
            'analysis': style_analysis,
            'citations': citations
        }
    
    def _analyze_lifestyle(self, posts: List[RedditPost]) -> Dict:
        """Analyze lifestyle preferences and patterns"""
        lifestyle = {}
        citations = []
        
        # Look for lifestyle indicators in content
        lifestyle_keywords = {
            'fitness_oriented': ['gym', 'workout', 'exercise', 'running', 'fitness'],
            'food_enthusiast': ['cooking', 'recipe', 'restaurant', 'food', 'cooking'],
            'traveler': ['travel', 'trip', 'vacation', 'country', 'city'],
            'homebody': ['home', 'netflix', 'cozy', 'indoor']
        }
        
        for category, keywords in lifestyle_keywords.items():
            count = 0
            for post in posts:
                content_lower = post.content.lower()
                for keyword in keywords:
                    if keyword in content_lower:
                        count += 1
                        if count <= 3:  # Limit citations
                            citations.append({
                                'category': 'lifestyle',
                                'indicator': category,
                                'evidence': f"Mentioned '{keyword}'",
                                'source_url': post.url,
                                'source_type': post.post_type
                            })
            
            if count > 0:
                lifestyle[category] = f"Interest level: {'High' if count > 5 else 'Medium' if count > 2 else 'Low'}"
        
        return {
            'analysis': lifestyle,
            'citations': citations
        }
    
    def _analyze_values(self, posts: List[RedditPost]) -> Dict:
        """Analyze user values and beliefs"""
        values = {}
        citations = []
        
        # This is a simplified analysis - in a real application,
        # you might use more sophisticated NLP techniques
        value_keywords = {
            'privacy_conscious': ['privacy', 'data', 'surveillance', 'tracking'],
            'environmentally_conscious': ['environment', 'climate', 'sustainability', 'green'],
            'community_oriented': ['community', 'help', 'volunteer', 'support'],
            'technology_enthusiast': ['innovation', 'technology', 'future', 'automation']
        }
        
        for category, keywords in value_keywords.items():
            mentions = 0
            for post in posts:
                content_lower = post.content.lower()
                for keyword in keywords:
                    if keyword in content_lower:
                        mentions += 1
                        if mentions <= 2:  # Limit citations
                            citations.append({
                                'category': 'values',
                                'indicator': category,
                                'evidence': f"Discussion about '{keyword}'",
                                'source_url': post.url,
                                'source_type': post.post_type
                            })
            
            if mentions > 0:
                values[category] = f"Evidence of this value: {mentions} mentions"
        
        return {
            'analysis': values,
            'citations': citations
        }
    
    def _analyze_online_behavior(self, posts: List[RedditPost]) -> Dict:
        """Analyze online behavior patterns"""
        behavior = {}
        citations = []
        
        if not posts:
            return {'analysis': behavior, 'citations': citations}
        
        # Posting frequency analysis
        post_count = len([p for p in posts if p.post_type == 'post'])
        comment_count = len([p for p in posts if p.post_type == 'comment'])
        
        if comment_count > post_count * 3:
            behavior['engagement_style'] = 'More of a commenter than original poster'
        elif post_count > comment_count:
            behavior['engagement_style'] = 'Prefers creating original content'
        else:
            behavior['engagement_style'] = 'Balanced between posting and commenting'
        
        # Karma analysis
        avg_score = sum(p.score for p in posts) / len(posts) if posts else 0
        if avg_score > 10:
            behavior['content_reception'] = 'Generally well-received content'
        elif avg_score > 1:
            behavior['content_reception'] = 'Moderately engaging content'
        else:
            behavior['content_reception'] = 'Niche or less popular content'
        
        return {
            'analysis': behavior,
            'citations': citations
        }
    
    def _analyze_technical_skills(self, posts: List[RedditPost]) -> Dict:
        """Analyze technical proficiency indicators"""
        skills = {}
        citations = []
        
        # Technical keywords and programming languages
        tech_keywords = {
            'programming_languages': ['python', 'javascript', 'java', 'c++', 'php', 'ruby', 'go', 'rust'],
            'web_technologies': ['html', 'css', 'react', 'angular', 'vue', 'node.js', 'django'],
            'tools_platforms': ['git', 'docker', 'aws', 'linux', 'mysql', 'mongodb'],
            'concepts': ['algorithm', 'database', 'api', 'machine learning', 'ai', 'blockchain']
        }
        
        for category, keywords in tech_keywords.items():
            found_skills = []
            for post in posts:
                content_lower = post.content.lower()
                for keyword in keywords:
                    if keyword in content_lower and keyword not in found_skills:
                        found_skills.append(keyword)
                        citations.append({
                            'category': 'technical_skills',
                            'indicator': f'{category}: {keyword}',
                            'evidence': f"Mentioned '{keyword}' in discussion",
                            'source_url': post.url,
                            'source_type': post.post_type
                        })
            
            if found_skills:
                skills[category] = found_skills[:5]  # Limit to top 5
        
        return {
            'analysis': skills,
            'citations': citations
        }
        found_skills = []
        for post in posts:
            content_lower = post.content.lower()
            for keyword in keywords:
                if keyword in content_lower and keyword not in found_skills:
                    found_skills.append(keyword)
                    citations.append({
                            'category': 'technical_skills',
                            'indicator': f'{category}: {keyword}',
                            'evidence': f"Mentioned '{keyword}' in discussion",
                            'source_url': post.url,
                            'source_type': post.post_type
                    })
            
            if found_skills:
                skills[category] = found_skills[:5]  # Limit to top 5
        
        return {
            'analysis': skills,
            'citations': citations
        }


class PersonaOutputGenerator:
    """Generates formatted output for the user persona"""
    
    def __init__(self):
        self.output_template = """
=================================================================
                    REDDIT USER PERSONA ANALYSIS
=================================================================
Generated on: {timestamp}
Profile URL: {profile_url}
Username: {username}

=================================================================
                          USER OVERVIEW
=================================================================
{user_overview}

=================================================================
                         DEMOGRAPHICS
=================================================================
{demographics}

=================================================================
                      INTERESTS & HOBBIES
=================================================================
{interests}

=================================================================
                       PERSONALITY TRAITS
=================================================================
{personality}

=================================================================
                     COMMUNICATION STYLE
=================================================================
{communication}

=================================================================
                    LIFESTYLE PREFERENCES
=================================================================
{lifestyle}

=================================================================
                        VALUES & BELIEFS
=================================================================
{values}

=================================================================
                       ONLINE BEHAVIOR
=================================================================
{online_behavior}

=================================================================
                    TECHNICAL PROFICIENCY
=================================================================
{technical_skills}

=================================================================
                      CITATIONS & EVIDENCE
=================================================================
{citations}

=================================================================
                         DISCLAIMER
=================================================================
This persona is generated based on publicly available Reddit posts 
and comments. It represents patterns and inferences from digital 
behavior and may not fully represent the individual's complete 
personality or circumstances.

Analysis conducted using automated text analysis methods.
=================================================================
"""
    
    def generate_persona_text(self, persona_data: Dict, profile_url: str, 
                            username: str, citations: List[Dict]) -> str:
        """Generate the complete persona text output"""
        
        # Format each section
        user_overview = self._format_user_overview(persona_data.get('user_overview', {}))
        demographics = self._format_section(persona_data.get('demographics', {}))
        interests = self._format_section(persona_data.get('interests_hobbies', {}))
        personality = self._format_section(persona_data.get('personality_traits', {}))
        communication = self._format_section(persona_data.get('communication_style', {}))
        lifestyle = self._format_section(persona_data.get('lifestyle_preferences', {}))
        values = self._format_section(persona_data.get('values_beliefs', {}))
        online_behavior = self._format_section(persona_data.get('online_behavior', {}))
        technical_skills = self._format_section(persona_data.get('technical_proficiency', {}))
        citations_text = self._format_citations(citations)
        
        return self.output_template.format(
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            profile_url=profile_url,
            username=username,
            user_overview=user_overview,
            demographics=demographics,
            interests=interests,
            personality=personality,
            communication=communication,
            lifestyle=lifestyle,
            values=values,
            online_behavior=online_behavior,
            technical_skills=technical_skills,
            citations=citations_text
        )
    
    def _format_user_overview(self, overview_data: Dict) -> str:
        """Format the user overview section"""
        if not overview_data:
            return "No overview data available."
        
        text = ""
        for key, value in overview_data.items():
            if key == 'most_active_subreddits':
                text += f"Most Active Subreddits: {', '.join(value[:5])}\n"
            else:
                text += f"{key.replace('_', ' ').title()}: {value}\n"
        
        return text
    
    def _format_section(self, section_data: Dict) -> str:
        """Format a generic persona section"""
        if not section_data or 'analysis' not in section_data:
            return "No significant patterns detected in this category."
        
        analysis = section_data['analysis']
        if not analysis:
            return "No significant patterns detected in this category."
        
        text = ""
        for category, details in analysis.items():
            category_name = category.replace('_', ' ').title()
            
            if isinstance(details, dict):
                text += f"\n{category_name}:\n"
                for key, value in details.items():
                    text += f"  • {key.replace('_', ' ').title()}: {value}\n"
            elif isinstance(details, list):
                text += f"\n{category_name}:\n"
                for item in details[:5]:  # Limit to 5 items
                    text += f"  • {item}\n"
            else:
                text += f"\n{category_name}: {details}\n"
        
        return text if text else "No significant patterns detected in this category."
    
    def _format_citations(self, all_citations: List[Dict]) -> str:
        """Format all citations grouped by category"""
        if not all_citations:
            return "No citations available."
        
        # Group citations by category
        citations_by_category = {}
        for citation in all_citations:
            category = citation.get('category', 'unknown')
            if category not in citations_by_category:
                citations_by_category[category] = []
            citations_by_category[category].append(citation)
        
        text = ""
        for category, citations in citations_by_category.items():
            text += f"\n{category.upper()} EVIDENCE:\n"
            text += "-" * 50 + "\n"
            
            for i, citation in enumerate(citations[:10], 1):  # Limit to 10 per category
                text += f"{i}. {citation.get('indicator', 'Unknown')}\n"
                text += f"   Evidence: {citation.get('evidence', 'No evidence')}\n"
                text += f"   Source: {citation.get('source_url', 'No URL')}\n"
                text += f"   Type: {citation.get('source_type', 'Unknown')}\n\n"
        
        return text


def main():
    """Main function to run the Reddit User Persona Generator"""
    parser = argparse.ArgumentParser(description='Generate user persona from Reddit profile')
    parser.add_argument('profile_url', help='Reddit user profile URL')
    parser.add_argument('-o', '--output', default=None, 
                       help='Output file name (default: username_persona.txt)')
    parser.add_argument('-l', '--limit', type=int, default=100,
                       help='Limit number of posts/comments to analyze (default: 100)')
    
    args = parser.parse_args()
    
    try:
        # Initialize components
        scraper = RedditScraper()
        generator = PersonaGenerator()
        output_gen = PersonaOutputGenerator()
        
        print(f"Starting analysis for: {args.profile_url}")
        
        # Extract username from URL
        username = scraper.extract_username(args.profile_url)
        print(f"Analyzing user: {username}")
        
        # Scrape user data
        posts, user_info = scraper.get_user_data(username, args.limit)
        
        if not posts:
            print("No posts found for this user. Cannot generate persona.")
            return
        
        print(f"Analyzing {len(posts)} posts and comments...")
        
        # Generate persona
        persona_data = generator.analyze_content(posts, user_info)
        
        # Collect all citations from different sections
        all_citations = []
        for section_name, section_data in persona_data.items():
            if isinstance(section_data, dict) and 'citations' in section_data:
                all_citations.extend(section_data['citations'])
        
        # Generate output text
        persona_text = output_gen.generate_persona_text(
            persona_data, args.profile_url, username, all_citations
        )
        
        # Determine output filename
        if args.output:
            output_filename = args.output
        else:
            output_filename = f"{username}_persona.txt"
        
        # Write to file
        with open(output_filename, 'w', encoding='utf-8') as f:
            f.write(persona_text)
        
        print(f"✅ Persona generated successfully!")
        print(f"📄 Output saved to: {output_filename}")
        print(f"📊 Analyzed {len(posts)} posts/comments")
        print(f"📝 Generated {len(all_citations)} citations")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1


if __name__ == "__main__":
    main()