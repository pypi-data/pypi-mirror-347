# hobby-by-category-py 🎨⚡🏕️

A comprehensive Python package providing categorized hobby data. Perfect for forms, recommendation systems, and hobby discovery apps.

## Features

- **300+ hobbies** across 10 categories
- **Easy-to-use API** for accessing hobby data
- **Python 3.6+** compatible
- **Zero dependencies**
- **Active maintenance**

## Installation

```bash
pip install hobby-by-category
Basic Usage
python
from hobby_by_category import get_hobbies_by_category, get_random_hobby

# Get all creative hobbies
creative_hobbies = get_hobbies_by_category("creative_and_artistic")
print(creative_hobbies)

# Get a random outdoor activity
random_outdoor = get_random_hobby("outdoor_and_adventure")
print(random_outdoor)
Available Categories
creative_and_artistic - Painting, Drawing, Photography, etc.

outdoor_and_adventure - Hiking, Camping, Rock Climbing, etc.

sports_and_fitness - Running, Yoga, Swimming, etc.

intellectual_and_learning - Reading, Chess, Astronomy, etc.

tech_and_gaming - Coding, Gaming, VR, etc.

music_and_performance - Instruments, Singing, DJing, etc.

collecting - Coins, Vinyl, Comics, etc.

food_and_drink - Cooking, Brewing, Mixology, etc.

social_and_community - Volunteering, Board Games, etc.

relaxation_and_mindfulness - Meditation, Journaling, etc.

API Reference
Data Structure
Access the raw hobby data dictionary:

python
from hobby_by_category import HOBBY_DATA
Utility Functions
Function	Description	Example
get_all_categories()	Returns all category names	['creative_and_artistic', ...]
get_hobbies_by_category(category)	Returns hobbies for specific category	get_hobbies_by_category('tech_and_gaming')
get_random_hobby(category=None)	Returns random hobby (optional category filter)	get_random_hobby('food_and_drink')
Example Implementations
Flask Form Processing
python
from flask import Flask, request
from hobby_by_category import get_hobbies_by_category

app = Flask(__name__)

@app.route('/submit-hobby', methods=['POST'])
def submit_hobby():
    category = request.form['category']
    hobby = request.form['hobby']
    
    if hobby not in get_hobbies_by_category(category):
        return "Invalid hobby selection", 400
        
    # Process valid hobby
    return "Hobby saved successfully", 200
Django Form
python
from django import forms
from hobby_by_category import get_all_categories, get_hobbies_by_category

class HobbyForm(forms.Form):
    category = forms.ChoiceField(choices=[(c, c.replace('_', ' ').title()) for c in get_all_categories()])
    hobby = forms.ChoiceField(choices=[])
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'category' in self.data:
            category = self.data['category']
            self.fields['hobby'].choices = [(h, h) for h in get_hobbies_by_category(category)]
Development
Building from Source
bash
git clone https://github.com/therealMAO247/hobby-by-category-py.git
cd hobby-by-category-py
pip install -e .
Testing
bash
python -m unittest discover
Contributing
Contributions are welcome! Please:

Fork the repository

Create a new branch for your feature

Submit a pull request

License
MIT © 2025, Michael Anan Onimisi <@therealMAO247>.
MIT © 2025, Ahoiza Technologies <www.ahoizatechnologies.com>.