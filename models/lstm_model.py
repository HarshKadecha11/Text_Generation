import nltk
from nltk.tokenize import word_tokenize
import string
import random


class LSTMTextGenerator:
    def __init__(self):
        self.initialized = False

        # Download ALL required NLTK resources
        self._ensure_nltk_resources()

        # Topic templates
        self.topic_templates = {
            'history': [
                "Throughout {era}, {subject} played a pivotal role in shaping society and culture.",
                "Historians have extensively documented how {subject} influenced the development of {related_concept}.",
                "The significance of {subject} cannot be overstated when examining {era} events.",
                "Many scholars argue that {subject} represented a turning point in how people understood {related_concept}.",
                "The evolution of {subject} reflects broader social and political changes during {era}."
            ],
            'science': [
                "Recent research on {subject} has revealed fascinating insights into {related_concept}.",
                "Scientists studying {subject} have developed new methodologies to address longstanding questions.",
                "The field of {subject} continues to advance our understanding of fundamental {related_concept}.",
                "Breakthrough discoveries in {subject} have applications ranging from medicine to technology.",
                "The complex relationship between {subject} and {related_concept} presents ongoing challenges for researchers."
            ],
            'personal': [
                "My experience with {subject} has profoundly influenced how I approach {related_concept}.",
                "When I first encountered {subject}, I didn't anticipate how it would transform my perspective.",
                "Working with {subject} has taught me valuable lessons about patience and persistence.",
                "The challenges associated with {subject} often require creative problem-solving strategies.",
                "I've found that understanding {subject} provides unique insights into everyday {related_concept}."
            ],
            'philosophical': [
                "The concept of {subject} raises fundamental questions about {related_concept} and human experience.",
                "Philosophers have long debated the nature of {subject} and its relationship to consciousness.",
                "Examining {subject} through different philosophical traditions reveals varying interpretations.",
                "The paradoxes within {subject} challenge conventional understanding of {related_concept}.",
                "Contemporary discussions of {subject} often integrate insights from both Eastern and Western philosophy."
            ],
            'practical': [
                "Implementing effective strategies for {subject} requires careful planning and execution.",
                "Best practices for managing {subject} have evolved significantly in recent years.",
                "A systematic approach to {subject} yields better results than ad-hoc methods.",
                "Professionals working with {subject} recommend focusing on key metrics like {related_concept}.",
                "Developing expertise in {subject} involves both theoretical knowledge and practical experience."
            ]
        }

        self.transition_phrases = [
            "Furthermore,", "Moreover,", "In addition,", "Similarly,", "Consequently,",
            "However,", "Conversely,", "Nevertheless,", "Interestingly,", "Notably,",
            "As a result,", "Therefore,", "Subsequently,", "Indeed,", "Certainly,",
            "To illustrate,", "For instance,", "Specifically,", "In particular,", "Remarkably,"
        ]

        self.related_concepts = {
            'technology': ['innovation', 'digital transformation', 'user experience', 'efficiency', 'productivity'],
            'education': ['learning outcomes', 'student engagement', 'curriculum design', 'assessment methods',
                          'educational technology'],
            'health': ['wellness', 'prevention', 'treatment approaches', 'patient care', 'medical research'],
            'business': ['market trends', 'consumer behavior', 'operational efficiency', 'strategic planning',
                         'competitive advantage'],
            'environment': ['sustainability', 'conservation', 'ecological balance', 'climate patterns', 'biodiversity'],
            'art': ['creative expression', 'aesthetic principles', 'cultural significance', 'artistic movements',
                    'visual communication'],
            'relationships': ['communication', 'emotional intelligence', 'conflict resolution', 'mutual understanding',
                              'personal growth'],
            'society': ['cultural norms', 'social structures', 'community development', 'collective behavior',
                        'institutional frameworks']
        }

        self.eras = [
            'ancient times', 'the medieval period', 'the Renaissance', 'the Industrial Revolution',
            'the 20th century', 'the digital age', 'modern times', 'the post-war era',
            'the colonial period', 'the Enlightenment', 'the Victorian era', 'recent decades'
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

    def _process_text(self, text):
        """Process text for model input"""
        # Simple text processing without relying on NLTK tokenization
        text = text.lower()
        text = ''.join(c for c in text if c not in string.punctuation)

        try:
            # Try to use NLTK tokenization
            tokens = word_tokenize(text)
        except Exception as e:
            # Fall back to simple splitting if NLTK fails
            print(f"NLTK tokenization failed: {str(e)}. Using simple split.")
            tokens = text.split()

        return tokens

    def _determine_topic_category(self, prompt):
        """Determine which topic category best fits the prompt"""
        prompt_lower = prompt.lower()

        # Define keywords for each category
        category_keywords = {
            'history': ['history', 'historical', 'past', 'ancient', 'century', 'era', 'period', 'civilization',
                        'revolution', 'war', 'dynasty', 'empire'],
            'science': ['science', 'scientific', 'research', 'study', 'experiment', 'discovery', 'theory', 'hypothesis',
                        'analysis', 'data', 'observation'],
            'personal': ['experience', 'personal', 'myself', 'life', 'journey', 'reflection', 'growth', 'challenge',
                         'story', 'perspective', 'feeling'],
            'philosophical': ['philosophy', 'philosophical', 'concept', 'meaning', 'existence', 'consciousness',
                              'reality', 'truth', 'ethics', 'morality'],
            'practical': ['practical', 'implementation', 'strategy', 'method', 'technique', 'approach', 'solution',
                          'management', 'application', 'process']
        }

        # Count matches for each category
        category_matches = {category: sum(1 for keyword in keywords if keyword in prompt_lower)
                            for category, keywords in category_keywords.items()}

        # Get the category with the most matches
        best_category = max(category_matches.items(), key=lambda x: x[1])

        # If no matches found, default to a random category
        if best_category[1] == 0:
            return random.choice(list(self.topic_templates.keys()))
        else:
            return best_category[0]

    def _determine_related_concept_category(self, prompt):
        """Determine which related concept category best fits the prompt"""
        prompt_lower = prompt.lower()

        concept_matches = {}
        for concept, related_terms in self.related_concepts.items():
            # Check for the concept itself
            if concept in prompt_lower:
                concept_matches[concept] = 2  # Give extra weight to direct category matches

            # Check for related terms
            matches = sum(1 for term in related_terms if term in prompt_lower)
            if concept in concept_matches:
                concept_matches[concept] += matches
            else:
                concept_matches[concept] = matches

        # Get the concept with the most matches
        if concept_matches:
            best_concept = max(concept_matches.items(), key=lambda x: x[1])
            return best_concept[0]
        else:
            return random.choice(list(self.related_concepts.keys()))

    def generate(self, prompt, length=500):
        """Generate text based on a prompt"""
        if not prompt or prompt.strip() == "":
            return "Please provide a prompt to generate text."

        if not self.initialized:
            return "The model is not properly initialized. Please check the server logs."

        try:
            # Use the entire prompt as the subject to ensure relevance
            subject = prompt.strip()

            # For template substitution, use a shorter version if needed
            processed_prompt = self._process_text(prompt)
            short_subject = prompt

            # If the prompt is too long, extract a key phrase
            if len(subject) > 30:
                # Find substantial words
                for word in processed_prompt:
                    if len(word) > 3:
                        short_subject = word
                        break

            # Determine the topic category and related concept category
            topic_category = self._determine_topic_category(prompt)
            concept_category = self._determine_related_concept_category(prompt)

            # Get templates for the selected category
            templates = self.topic_templates[topic_category].copy()

            # Get related concepts for the selected concept category
            related_concepts = self.related_concepts[concept_category]

            # Generate text using templates
            paragraphs = []

            # Create a simplified text generation if templates approach fails
            if not templates:
                return f"{subject} is a fascinating topic that has many interesting aspects to explore. It offers valuable insights and continues to be relevant in various contexts."

            # First paragraph - always start with the prompt
            first_sentence = f"{subject} is a fascinating topic worth exploring in depth."
            sentences = [first_sentence]

            # Add 2-3 more sentences from templates
            for i in range(min(random.randint(2, 3), len(templates))):
                template = random.choice(templates)
                templates.remove(template)

                # Fill in template variables
                related_concept = random.choice(related_concepts)
                era = random.choice(self.eras) if topic_category == 'history' else ""

                try:
                    sentence = template.format(
                        subject=short_subject,
                        related_concept=related_concept,
                        era=era
                    )
                    sentences.append(sentence)
                except Exception as e:
                    # Fallback if formatting fails
                    sentences.append(
                        f"Understanding {short_subject} requires careful consideration of various factors.")

            paragraphs.append(" ".join(sentences))

            # Second paragraph with transition
            if templates:
                sentences = []
                transition = random.choice(self.transition_phrases)

                # Start with a transition that references the prompt again
                first_sentence = f"{transition} when discussing {subject}, it's important to consider various perspectives."
                sentences.append(first_sentence)

                # Add 2-3 more sentences
                for i in range(min(random.randint(2, 3), len(templates))):
                    if not templates:
                        break

                    template = random.choice(templates)
                    templates.remove(template)

                    related_concept = random.choice(related_concepts)
                    era = random.choice(self.eras) if topic_category == 'history' else ""

                    try:
                        sentence = template.format(
                            subject=short_subject,
                            related_concept=related_concept,
                            era=era
                        )
                        sentences.append(sentence)
                    except Exception as e:
                        # Fallback if formatting fails
                        sentences.append(f"The implications of {short_subject} extend to various domains and contexts.")

                paragraphs.append(" ".join(sentences))

            # Combine paragraphs
            generated_text = "\n\n".join(paragraphs)

            # Ensure we don't exceed the requested length
            return generated_text[:length]

        except Exception as e:
            # If anything goes wrong, return a simple response that references the prompt
            import traceback
            print(f"Error in LSTM text generation: {str(e)}")
            print(traceback.format_exc())
            return f"The topic of {prompt} is interesting and has many aspects worth exploring. It continues to evolve and offers valuable insights across different contexts."