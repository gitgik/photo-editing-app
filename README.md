# photo-editing-app [![Build Status](https://travis-ci.org/gitgik/photo-editing-app.svg?branch=master)](https://travis-ci.org/gitgik/photo-editing-app) [![Coverage Status](https://coveralls.io/repos/github/gitgik/photo-editing-app/badge.svg?branch=feature-socialmedia)](https://coveralls.io/github/gitgik/photo-editing-app?branch=feature-socialmedia) [![Code Health](https://landscape.io/github/gitgik/photo-editing-app/develop/landscape.svg?style=flat)](https://landscape.io/github/gitgik/photo-editing-app/develop) [![License](http://img.shields.io/:license-mit-blue.svg)](http://doge.mit-license.org)
A django-powered app that allows you to edit your photos and share them on facebook.
Live version available [here](https://picto.herokuapp.com/)


## Technologies used
* [Django](https://www.djangoproject.com/): The web framework for perfectionists with deadlines (Django builds better web apps with less code).
* [Pillow](http://pillow.readthedocs.org/en/3.1.x/): The friendly Python Imaging Library (PIL) fork.
* [Django Rest Framwork](http://www.django-rest-framework.org/): A powerful and flexible toolkit for building web APIs.
* [AngularJS](https://angularjs.org/): The go-to framework for building HTML enhanced web apps.
* [Angular Material](https://material.angularjs.org/latest/): AngularJS implementation for Google's material design specification.
* [Google Web Fonts](https://www.google.com/fonts): Beautiful fonts from Google to complement your web app.
* Minor dependencies can be found in the requirements.txt file on the root folder.


## Installation
* If you wish to run your own build, first ensure you have python globally installed in your computer. If not, you can get python [here](https://www.python.org").
* After this, ensure you have installed virtualenv globally as well. If not, run this:
    ```
        $ pip install virtualenv
    ```
* Git clone this repo to your PC
    ```
        $ git clone https://github.com/andela-ggikera/photo-editing-app.git
    ```


* #### Dependencies
    1. Cd into your the cloned repo as such:
        ```
            $ cd photo-editing-app
        ```

    2. Create and fire up your virtual environment:
        ```
            $ virtualenv env
            $ source env/bin/activate
        ```
    3. Install the dependencies needed to run the app:
        ```
            $ pip install -r requirements.txt
        ```

        ```
            $ npm install -g bower
        ```

        ```
            $ bower install
        ```


* #### Run It
    Fire the engines using this one simple command:
    ```
        $ python manage.py collectstatic --noinput
    ```

    ```
        $ python manage.py runserver
    ```

    You can now access the service on your browser by using
    ```
        http://localhost:8000/
    ```
