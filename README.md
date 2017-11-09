TravisCI Badge: [![Build Status](https://travis-ci.org/HarithJ/Yummy-Recipes.svg?branch=restructuring-ch2)](https://travis-ci.org/HarithJ/Yummy-Recipes)

coveralls badge: [![Coverage Status](https://coveralls.io/repos/github/HarithJ/Yummy-Recipes/badge.svg)](https://coveralls.io/github/HarithJ/Yummy-Recipes)

# Yummy-Recipes


To view the webiste please visit (PLEASE NOTE: The link is not working perfectly as it should): https://yummy-recipes-harith.herokuapp.com/

You can also clone the development branch and take the following steps to view the website (this shud happen inside command-line prompt:

1. Move in the Yummy-Recipes directory: 

        cd Yummy-Recipes
        
2. Activate the virtualenv: 

        source bin/activate

3. From here you can use two ways:
        
        Set the variable for flask: export FLASK_APP=webapp/app.py
        Run flask: flask run
    
    OR JUST TYPE
            
        gunicorn -w 4 webapp.app:app
