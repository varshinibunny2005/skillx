"""
Management command to seed the database with initial skills, tests, and demo data.
Run: python manage.py seed_data
"""
from django.core.management.base import BaseCommand
from skills.models import Skill, SkillTest, Question, Answer


SKILLS_DATA = [
    # Technology
    ('Python Programming', 'tech', 'fas fa-code', '#3b82f6'),
    ('JavaScript', 'tech', 'fas fa-js', '#f59e0b'),
    ('Web Development', 'tech', 'fas fa-globe', '#6366f1'),
    ('Data Science', 'tech', 'fas fa-chart-bar', '#8b5cf6'),
    ('Machine Learning', 'tech', 'fas fa-brain', '#a78bfa'),
    ('Mobile Development', 'tech', 'fas fa-mobile', '#34d399'),
    ('SQL & Databases', 'tech', 'fas fa-database', '#60a5fa'),
    ('DevOps & Cloud', 'tech', 'fas fa-cloud', '#93c5fd'),
    ('Cybersecurity', 'tech', 'fas fa-shield', '#f87171'),
    ('UI/UX Design', 'tech', 'fas fa-pen-nib', '#c084fc'),
    # Music
    ('Guitar', 'music', 'fas fa-guitar', '#f59e0b'),
    ('Piano', 'music', 'fas fa-music', '#ec4899'),
    ('Singing', 'music', 'fas fa-microphone', '#a78bfa'),
    ('Music Production', 'music', 'fas fa-headphones', '#22d3ee'),
    ('Violin', 'music', 'fas fa-music', '#fb923c'),
    # Languages
    ('English', 'language', 'fas fa-language', '#22c55e'),
    ('Hindi', 'language', 'fas fa-language', '#f97316'),
    ('Spanish', 'language', 'fas fa-language', '#ef4444'),
    ('French', 'language', 'fas fa-language', '#3b82f6'),
    ('Mandarin', 'language', 'fas fa-language', '#eab308'),
    ('Japanese', 'language', 'fas fa-language', '#e879f9'),
    # Art
    ('Drawing & Illustration', 'art', 'fas fa-paintbrush', '#f472b6'),
    ('Photography', 'photography', 'fas fa-camera', '#94a3b8'),
    ('Video Editing', 'art', 'fas fa-film', '#818cf8'),
    ('Graphic Design', 'art', 'fas fa-palette', '#fb923c'),
    # Fitness & Cooking
    ('Yoga', 'fitness', 'fas fa-person-walking', '#34d399'),
    ('Cooking', 'cooking', 'fas fa-utensils', '#f59e0b'),
    ('Baking', 'cooking', 'fas fa-bread-slice', '#fb923c'),
    ('Dance', 'dance', 'fas fa-person-dancing', '#c084fc'),
    # Business
    ('Digital Marketing', 'business', 'fas fa-bullhorn', '#22d3ee'),
    ('Content Writing', 'writing', 'fas fa-pen', '#a3e635'),
    ('Public Speaking', 'business', 'fas fa-microphone-alt', '#f472b6'),
    ('Chess', 'other', 'fas fa-chess', '#94a3b8'),
    ('Mathematics', 'math', 'fas fa-square-root-variable', '#60a5fa'),
]

PYTHON_QUESTIONS = {
    'beginner': [
        {
            'text': 'What is the output of print(type(42))?',
            'answers': [("<class 'int'>", True), ("<class 'str'>", False), ("int", False), ("42", False)],
            'explanation': 'type() returns the type of the object. 42 is an integer.'
        },
        {
            'text': 'Which keyword is used to define a function in Python?',
            'answers': [('def', True), ('function', False), ('func', False), ('define', False)],
        },
        {
            'text': 'What is the result of 10 // 3 in Python?',
            'answers': [('3', True), ('3.33', False), ('3.0', False), ('4', False)],
        },
        {
            'text': 'Which of the following is a valid Python comment?',
            'answers': [('# This is a comment', True), ('// This is a comment', False), ('/* comment */', False), ('<!-- comment -->', False)],
        },
        {
            'text': 'What data type is the result of 5 / 2 in Python 3?',
            'answers': [('float', True), ('int', False), ('str', False), ('double', False)],
        },
    ],
    'intermediate': [
        {
            'text': 'What is the purpose of *args in a Python function?',
            'answers': [('To accept a variable number of positional arguments', True), ('To accept keyword arguments', False), ('To define default parameters', False), ('To unpack a list', False)],
        },
        {
            'text': 'Which built-in function returns an iterator of tuples from multiple iterables?',
            'answers': [('zip()', True), ('map()', False), ('enumerate()', False), ('filter()', False)],
        },
        {
            'text': 'What does list comprehension [x*2 for x in range(5)] return?',
            'answers': [('[0, 2, 4, 6, 8]', True), ('[1, 2, 3, 4, 5]', False), ('[0, 1, 2, 3, 4]', False), ('[2, 4, 6, 8, 10]', False)],
        },
        {
            'text': 'What is a lambda function?',
            'answers': [('An anonymous function defined with the lambda keyword', True), ('A class method', False), ('A recursive function', False), ('A function with default arguments', False)],
        },
        {
            'text': 'What does the @property decorator do?',
            'answers': [('Makes a method accessible as an attribute', True), ('Makes a method static', False), ('Makes a method class-level', False), ('Makes a method private', False)],
        },
    ],
    'expert': [
        {
            'text': 'What is the Global Interpreter Lock (GIL) in Python?',
            'answers': [('A mutex that protects access to Python objects', True), ('A tool for debugging', False), ('A garbage collector', False), ('A compiler optimization', False)],
        },
        {
            'text': 'Which metaclass is the base metaclass for all classes in Python?',
            'answers': [('type', True), ('object', False), ('class', False), ('base', False)],
        },
        {
            'text': 'What is the purpose of __slots__ in a Python class?',
            'answers': [('To restrict the attributes a class can have and save memory', True), ('To define class methods', False), ('To override default behavior', False), ('To enable inheritance', False)],
        },
        {
            'text': 'What does asyncio.gather() do?',
            'answers': [('Runs multiple coroutines concurrently', True), ('Collects results from a single coroutine', False), ('Cancels all pending tasks', False), ('Creates a new event loop', False)],
        },
        {
            'text': 'What is a descriptor in Python?',
            'answers': [('An object that defines __get__, __set__, or __delete__', True), ('A documentation string', False), ('A type hint', False), ('A debugging tool', False)],
        },
    ],
}


class Command(BaseCommand):
    help = 'Seed the database with initial skills and test questions'

    def handle(self, *args, **kwargs):
        self.stdout.write('🌱 Seeding skills...')

        # Create skills
        created_skills = {}
        for name, category, icon, color in SKILLS_DATA:
            skill, created = Skill.objects.get_or_create(
                name=name,
                defaults={'category': category, 'icon': icon, 'color': color}
            )
            created_skills[name] = skill
            if created:
                self.stdout.write(f'  + {name}')

        # Create Python tests
        python = created_skills.get('Python Programming')
        if python:
            self.stdout.write('📝 Creating Python skill tests...')
            for level, questions_data in PYTHON_QUESTIONS.items():
                titles = {'beginner': 'Python Basics', 'intermediate': 'Python Intermediate', 'expert': 'Python Expert'}
                test, created = SkillTest.objects.get_or_create(
                    skill=python, level=level,
                    defaults={
                        'title': titles[level],
                        'passing_score': 60,
                        'time_limit_minutes': 10,
                    }
                )
                if created:
                    for i, q_data in enumerate(questions_data):
                        question = Question.objects.create(
                            test=test, question_text=q_data['text'],
                            explanation=q_data.get('explanation', ''), order=i
                        )
                        for ans_text, is_correct in q_data['answers']:
                            Answer.objects.create(question=question, answer_text=ans_text, is_correct=is_correct)
                    self.stdout.write(f'  + Python {level} test created')

        self.stdout.write(self.style.SUCCESS(f'\n✅ Seeded {Skill.objects.count()} skills and {SkillTest.objects.count()} tests!\n'))
        self.stdout.write('🚀 Next steps:')
        self.stdout.write('   1. python manage.py createsuperuser')
        self.stdout.write('   2. python manage.py runserver')
        self.stdout.write('   3. Visit http://127.0.0.1:8000/')
