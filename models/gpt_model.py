import numpy as np
import nltk
import string
import re
import random


class SimpleGPTModel:
    def __init__(self):
        self.initialized = False

        # Download ALL required NLTK resources
        self._ensure_nltk_resources()

        # Add specific templates for popular platforms/technologies
        self.specific_topics = {
            'github': {
                'description': "GitHub is a web-based platform for version control and collaboration using Git. It allows developers to store, manage, track changes in code, and collaborate on projects.",
                'templates': [
                    "GitHub serves as a central hub for software development, allowing developers to collaborate on projects, manage code repositories, and track issues.",
                    "Millions of developers use GitHub to host and review code, manage projects, and build software together through features like pull requests and actions.",
                    "As a platform built around Git version control, GitHub provides tools for code review, project management, and continuous integration/continuous deployment (CI/CD).",
                    "GitHub's ecosystem includes features like Actions for automation, Pages for website hosting, and Codespaces for development environments in the browser.",
                    "Many open-source projects rely on GitHub for collaboration, contributions from the community, and transparent development processes.",
                    "GitHub's pull request workflow enables code review and collaboration before changes are merged into the main codebase."
                ]
            },
            'python': {
                'description': "Python is a high-level, interpreted programming language known for its readability and versatility in web development, data science, artificial intelligence, and more.",
                'templates': [
                    "Python's simple syntax and readability make it an excellent language for beginners, while its extensive libraries support advanced applications in data science and AI.",
                    "The Python ecosystem includes powerful libraries like NumPy, Pandas, and TensorFlow that have made it the leading language for data analysis and machine learning.",
                    "Python follows a philosophy of 'there should be one—and preferably only one—obvious way to do it' which promotes code consistency and readability.",
                    "With its large standard library and third-party packages, Python enables developers to perform complex tasks with minimal code.",
                    "Python's flexibility allows it to be used for web development, scientific computing, automation, and even embedded systems programming."
                ]
            },
            'javascript': {
                'description': "JavaScript is a programming language that enables interactive web pages and is an essential part of web applications, running in browsers as well as on servers through Node.js.",
                'templates': [
                    "JavaScript powers the interactive elements of modern websites, allowing developers to create dynamic user experiences without page reloads.",
                    "The evolution of JavaScript from simple client-side scripting to full-stack development through Node.js has transformed web development.",
                    "Modern JavaScript frameworks like React, Angular, and Vue have created powerful paradigms for building complex, responsive web applications.",
                    "JavaScript's event-driven, non-blocking architecture makes it particularly well-suited for handling asynchronous operations in web applications.",
                    "Despite its initial limitations, JavaScript has grown into a versatile language used for everything from front-end development to server-side programming and mobile applications."
                ]
            },
            'docker': {
                'description': "Docker is a platform that uses containerization technology to package applications and their dependencies together, ensuring consistent operation across different computing environments.",
                'templates': [
                    "Docker containers package code and dependencies together, ensuring that applications run consistently regardless of the environment.",
                    "The containerization approach provided by Docker has revolutionized application deployment, making it easier to implement microservices architectures.",
                    "Docker's lightweight containers start quickly and use resources more efficiently than traditional virtual machines, improving scalability.",
                    "DevOps practices have been greatly enhanced by Docker's ability to provide consistent development, testing, and production environments.",
                    "Docker's ecosystem includes Docker Compose for multi-container applications and Docker Swarm for container orchestration across multiple hosts."
                ]
            },
            'artificial intelligence': {
                'description': "Artificial intelligence (AI) is the simulation of human intelligence in machines, encompassing machine learning, natural language processing, computer vision, and other technologies.",
                'templates': [
                    "AI systems can analyze vast amounts of data to identify patterns and make predictions that would be impossible for humans to process manually.",
                    "Machine learning, a subset of AI, enables systems to learn from data and improve performance without explicit programming.",
                    "The ethical implications of AI development include concerns about bias, privacy, automation of jobs, and the potential for autonomous decision-making.",
                    "Deep learning models, inspired by the human brain's neural networks, have achieved breakthrough results in image recognition, natural language processing, and game playing.",
                    "AI applications span industries from healthcare (diagnostic systems) to finance (fraud detection) to transportation (autonomous vehicles)."
                ]
            }
        }

        # Define broader categories and their associated keywords and responses
        self.categories = {
            'technology': {
                'keywords': ['technology', 'computer', 'ai', 'digital', 'internet', 'software', 'hardware',
                             'programming', 'code', 'algorithm', 'data', 'machine', 'learning', 'cyber',
                             'tech', 'robot', 'automation', 'innovation', 'application', 'web', 'mobile',
                             'device', 'cloud', 'network', 'security', 'development', 'system', 'github',
                             'git', 'repository', 'commit', 'python', 'javascript', 'docker', 'container',
                             'devops', 'framework', 'api', 'database', 'frontend', 'backend', 'fullstack'],
                'templates': [
                    "The field of {topic} continues to evolve at a rapid pace. Recent advancements have opened up new possibilities for innovation and growth.",
                    "When discussing {topic}, it's important to consider both the technical aspects and the broader implications for society.",
                    "Experts in {topic} agree that the next decade will bring unprecedented changes to how we interact with technology.",
                    "{topic} represents one of the most dynamic areas in modern technology, with applications ranging from personal devices to enterprise systems.",
                    "The evolution of {topic} has been marked by key breakthroughs that have transformed our understanding of what's possible.",
                    "Many challenges in {topic} require interdisciplinary approaches, combining expertise from various fields of computer science and engineering."
                ]
            },
            'nature': {
                'keywords': ['nature', 'environment', 'climate', 'animal', 'plant', 'forest', 'ecology',
                             'wildlife', 'conservation', 'biodiversity', 'ecosystem', 'sustainable', 'green',
                             'earth', 'ocean', 'river', 'mountain', 'weather', 'natural', 'species', 'habitat',
                             'organic', 'biology', 'ecological', 'environmental', 'renewable'],
                'templates': [
                    "The beauty of {topic} lies in its complexity and interconnectedness. Each element plays a crucial role in maintaining balance.",
                    "Scientists studying {topic} have documented significant changes in recent years, raising important questions about conservation.",
                    "{topic} represents one of our most precious resources, requiring careful management and protection for future generations.",
                    "Understanding {topic} requires a holistic perspective that takes into account various ecological relationships and environmental factors.",
                    "The preservation of {topic} depends on sustainable practices and increased awareness of human impact on natural systems.",
                    "Research in {topic} has revealed fascinating adaptations and behaviors that help species survive in changing environments."
                ]
            },
            'education': {
                'keywords': ['education', 'learning', 'school', 'student', 'teacher', 'knowledge', 'teaching',
                             'academic', 'classroom', 'curriculum', 'university', 'college', 'study', 'degree',
                             'research', 'literacy', 'pedagogy', 'instruction', 'educational', 'scholar',
                             'training', 'skill', 'development', 'course', 'lecture', 'exam', 'assessment'],
                'templates': [
                    "The approach to {topic} has evolved significantly with the integration of new technologies and teaching methodologies.",
                    "Successful {topic} strategies focus on engaging students and developing critical thinking skills rather than rote memorization.",
                    "Research in {topic} suggests that personalized learning paths yield better outcomes for students across different ability levels.",
                    "The future of {topic} will likely emphasize adaptability and lifelong learning to prepare individuals for changing workforce demands.",
                    "Experts in {topic} recognize the importance of addressing diverse learning needs and creating inclusive educational environments.",
                    "Modern {topic} incorporates collaborative learning opportunities that reflect real-world problem-solving scenarios."
                ]
            },
            'health': {
                'keywords': ['health', 'medical', 'medicine', 'doctor', 'patient', 'hospital', 'disease',
                             'treatment', 'wellness', 'fitness', 'nutrition', 'diet', 'mental', 'physical',
                             'healthcare', 'prevention', 'therapy', 'diagnosis', 'clinical', 'pharmaceutical',
                             'surgery', 'recovery', 'immune', 'virus', 'bacteria', 'infection', 'condition'],
                'templates': [
                    "Advancements in {topic} have led to improved treatment options and better patient outcomes for many conditions.",
                    "Modern approaches to {topic} emphasize preventive care and lifestyle modifications alongside traditional medical interventions.",
                    "Research in {topic} continues to uncover the complex relationships between genetics, environment, and personal choices.",
                    "The field of {topic} has been transformed by technological innovations that allow for more precise diagnostics and treatments.",
                    "Experts in {topic} advocate for patient-centered care that considers individual needs and preferences in treatment decisions.",
                    "Understanding {topic} requires a holistic perspective that addresses physical, mental, and social aspects of wellbeing."
                ]
            },
            'business': {
                'keywords': ['business', 'economy', 'market', 'company', 'industry', 'finance', 'management',
                             'entrepreneur', 'corporate', 'startup', 'innovation', 'strategy', 'leadership',
                             'investment', 'commerce', 'trade', 'retail', 'service', 'product', 'consumer',
                             'customer', 'profit', 'revenue', 'growth', 'marketing', 'sales', 'brand'],
                'templates': [
                    "Successful {topic} strategies adapt to changing market conditions while maintaining a clear vision and purpose.",
                    "The landscape of {topic} has been transformed by digital technologies, creating new opportunities and challenges.",
                    "Modern {topic} approaches emphasize sustainability and social responsibility alongside traditional profit metrics.",
                    "Research in {topic} suggests that diverse teams and inclusive practices contribute to innovation and organizational success.",
                    "Effective {topic} leadership balances short-term objectives with long-term vision to ensure sustained growth.",
                    "The evolution of {topic} reflects broader social and economic trends, with increasing emphasis on agility and resilience."
                ]
            },
            'arts': {
                'keywords': ['art', 'music', 'literature', 'film', 'culture', 'creative', 'artist', 'design',
                             'painting', 'sculpture', 'photography', 'theater', 'dance', 'performance', 'poetry',
                             'novel', 'author', 'musician', 'composer', 'gallery', 'exhibition', 'aesthetic',
                             'artistic', 'cultural', 'entertainment', 'media', 'expression'],
                'templates': [
                    "The evolution of {topic} reflects changing social values and technological developments throughout history.",
                    "{topic} provides a powerful medium for cultural expression and social commentary across different societies.",
                    "Contemporary {topic} often blurs traditional boundaries, incorporating diverse influences and experimental approaches.",
                    "The study of {topic} offers insights into human creativity and the ways we process and respond to aesthetic experiences.",
                    "Throughout history, {topic} has served as both a mirror reflecting society and a force for cultural transformation.",
                    "Digital technologies have transformed how {topic} is created, distributed, and experienced in the modern world."
                ]
            }
        }

        # General templates for when no specific category is matched
        self.general_templates = [
            "The topic of {topic} encompasses various perspectives and approaches worth exploring in detail.",
            "When examining {topic}, it's valuable to consider both historical context and contemporary developments.",
            "Discussions about {topic} often reveal interesting connections to related fields and broader societal trends.",
            "Understanding {topic} requires careful analysis of available evidence and consideration of different viewpoints.",
            "Recent developments in {topic} have sparked renewed interest among experts and the general public alike.",
            "The significance of {topic} extends beyond immediate applications to influence long-term trends and practices.",
            "Exploring {topic} reveals complex relationships between theory and practice that continue to evolve over time.",
            "Researchers studying {topic} have identified key patterns and principles that help explain observed phenomena.",
            "The field of {topic} continues to develop as new information and methodologies become available.",
            "Critical thinking about {topic} involves questioning assumptions and evaluating evidence from multiple sources."
        ]

        self.initialized = True

    def _ensure_nltk_resources(self):
        """Make sure all required NLTK resources are downloaded"""
        resources = ['punkt']
        for resource in resources:
            try:
                nltk.data.find(f'tokenizers/{resource}')
                print(f"NLTK resource '{resource}' is already downloaded")
            except LookupError:
                print(f"Downloading NLTK resource '{resource}'")
                nltk.download(resource, quiet=False)

    def generate_with_web_search(self, prompt, length=500):
        """Generate text with web search augmentation"""
        # First check if we have pre-defined information
        specific_topic = self._identify_specific_topic(prompt)

        if specific_topic:
            return self._create_specific_topic_text(specific_topic, length)

        # If not, try to search the web
        try:
            search_results = self._search_web(prompt)
            if search_results:
                # Extract relevant information from search results
                relevant_info = self._extract_info_from_search(search_results)

                # Generate text using the gathered information
                return self._create_informed_text(prompt, relevant_info, length)
        except Exception as e:
            print(f"Web search failed: {str(e)}")

        # Fall back to template-based generation if search fails
        return self.generate(prompt, length)

    def _process_text(self, text):
        """Process text for model input"""
        # Simple preprocessing that doesn't rely on NLTK
        text = text.lower()
        text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation but keep spaces

        try:
            # Try to use NLTK tokenization
            from nltk.tokenize import word_tokenize
            tokens = word_tokenize(text)
        except Exception as e:
            # Fall back to simple splitting if NLTK fails
            print(f"NLTK tokenization failed: {str(e)}. Using simple split.")
            tokens = text.split()

        return tokens

    def _extract_key_topics(self, prompt):
        """Extract key topics from the prompt"""
        try:
            words = self._process_text(prompt)
            # Remove common stopwords
            stopwords = ['the', 'a', 'an', 'and', 'or', 'but', 'is', 'are', 'was', 'were',
                         'has', 'have', 'had', 'be', 'been', 'being', 'in', 'on', 'at', 'to',
                         'for', 'with', 'about', 'against', 'between', 'into', 'through',
                         'during', 'before', 'after', 'above', 'below', 'from', 'up', 'down',
                         'of', 'off', 'over', 'under', 'again', 'further', 'then', 'once',
                         'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both',
                         'each', 'few', 'more', 'most', 'some', 'such', 'no', 'not', 'only',
                         'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will',
                         'just', 'should', 'now']

            # Filter out stopwords
            key_words = [word for word in words if word not in stopwords and len(word) > 2]

            # If no key words are found after filtering, use the original prompt
            if not key_words:
                # Use the original prompt if no key words
                key_words = [prompt.lower()]

            return key_words
        except Exception as e:
            print(f"Error extracting key topics: {str(e)}")
            # Return a simple processed version of the prompt if extraction fails
            return [prompt.lower()]

    def _identify_specific_topic(self, prompt):
        """Check if the prompt contains a specific topic we have detailed information about"""
        prompt_lower = prompt.lower()

        for topic, data in self.specific_topics.items():
            if topic in prompt_lower:
                return topic

        # Check for partial matches or related terms
        for topic in self.specific_topics.keys():
            if any(term in prompt_lower for term in topic.split()):
                return topic

        return None

    def _identify_category(self, prompt):
        """Identify which category the prompt belongs to"""
        try:
            prompt_lower = prompt.lower()

            # Check each category for keyword matches
            for category, data in self.categories.items():
                if any(keyword in prompt_lower for keyword in data['keywords']):
                    return category

            return "general"
        except Exception as e:
            print(f"Error identifying category: {str(e)}")
            return "general"

    def _create_specific_topic_text(self, topic, length=500):
        """Create text for a specific topic using its description and templates"""
        topic_data = self.specific_topics[topic]

        # Start with the description
        text = topic_data['description'] + " "

        # Add 3-4 template sentences
        templates_to_use = random.sample(topic_data['templates'], min(4, len(topic_data['templates'])))
        for template in templates_to_use:
            text += template + " "

        # Create a second paragraph with additional information
        second_para = f"\n\nFurthermore, {topic} continues to evolve and adapt to changing needs. "
        remaining_templates = [t for t in topic_data['templates'] if t not in templates_to_use]

        if remaining_templates:
            for template in random.sample(remaining_templates, min(2, len(remaining_templates))):
                second_para += template + " "

        text += second_para

        # Ensure we don't exceed the requested length
        return text[:length]

    def _create_paragraph(self, topic_words, category, num_sentences=5):
        """Create a coherent paragraph about the topic"""
        try:
            if category == "general":
                templates = self.general_templates
            else:
                templates = self.categories[category]['templates']

            # Always use the original prompt as the primary topic
            primary_topic = topic_words[0]

            # Start with a sentence that explicitly mentions the topic
            first_sentence = f"{primary_topic} is a fascinating subject that warrants careful consideration."

            # Then add a template sentence
            try:
                template_sentence = random.choice(templates).format(topic=primary_topic)
                paragraph = f"{first_sentence} {template_sentence}"
            except Exception as e:
                print(f"Error applying template: {str(e)}")
                paragraph = first_sentence + f" There are many interesting aspects of {primary_topic} to explore."

            # Add additional sentences based on the category
            sentences_to_add = min(num_sentences - 2, len(templates) - 1)

            if sentences_to_add > 0:
                try:
                    # Get a sample of templates for additional sentences
                    additional_templates = random.sample([t for t in templates if t != template_sentence],
                                                         sentences_to_add)
                    for template in additional_templates:
                        paragraph += " " + template.format(topic=primary_topic)
                except Exception as e:
                    print(f"Error adding additional sentences: {str(e)}")
                    # Fallback generic sentences
                    paragraph += f" It offers valuable insights that continue to evolve. The implications of {primary_topic} are far-reaching and significant."

            return paragraph
        except Exception as e:
            print(f"Error creating paragraph: {str(e)}")
            # Fallback if anything goes wrong
            return f"{topic_words[0]} is an interesting topic with many different aspects to explore."

    def generate(self, prompt, length=500):
        """
        Generate text based on the prompt
        """
        if not prompt or prompt.strip() == "":
            return "Please provide a prompt to generate text."

        if not self.initialized:
            return "The model is not properly initialized. Please check the server logs."

        try:
            # Use the complete prompt as the main topic
            original_prompt = prompt.strip()

            # Check if this is a specific topic we have detailed information about
            specific_topic = self._identify_specific_topic(original_prompt)

            if specific_topic:
                # Use the specific topic generation
                return self._create_specific_topic_text(specific_topic, length)

            # If not a specific topic, continue with the regular approach
            # Extract key topics from the prompt for additional content
            key_topics = self._extract_key_topics(prompt)
            if original_prompt.lower() not in [t.lower() for t in key_topics]:
                key_topics.insert(0, original_prompt)

            # Identify the category of the prompt
            category = self._identify_category(prompt)

            # Create an initial paragraph that directly addresses the prompt
            paragraph1 = self._create_paragraph([original_prompt], category, num_sentences=3)

            # Create a second paragraph that continues to focus on the prompt
            paragraph2 = f"Furthermore, {original_prompt} has significant implications that deserve attention. "
            paragraph2 += self._create_paragraph([original_prompt], category, num_sentences=2)

            # Combine paragraphs
            full_text = paragraph1 + "\n\n" + paragraph2

            # Ensure we don't exceed the requested length
            return full_text[:length]

        except Exception as e:
            # If anything goes wrong, return a simple response that references the prompt
            import traceback
            print(f"Error in GPT text generation: {str(e)}")
            print(traceback.format_exc())
            return f"The topic of {prompt} is interesting and has many aspects worth exploring. It continues to evolve and offers valuable insights across different contexts."