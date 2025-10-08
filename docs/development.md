# Development

#### | [Overview](../README.md) | Development |

## Structure

This project requires an understanding of Django. A brief summary of Django will be given, followed by the project's structure.

### Django

`manage.py`

This is the starting point of the application. It handles commands, such as "python manage.py runserver".

`settings.py`

These are the project settings. They are pretty important.

`apps`

Projects are made up of apps. They are used to encapsulate different parts of the project. Examples include browse, post, staff, and user. Each app has its own URLs, views, models, etc.

`urls.py`

This handles URL routing. Each app can define its own paths and subpaths. URLs usually lead to views.

`views.py`

This is where the bulk of the application logic goes. Views can run code, interact with models, create forms, and more. Views trigger when a URL is visited. After handling logic, they return the correct HTML and data to the user.

`templates`

This is where the HTML is written. This HTML can also include server-processed logic.

`models`

A model represents a table in the database. Views can access data through them. Django can automatically modify the database to match models through migrations.

`forms.py`

Custom forms can be defined, usually corresponding to a model. This simplifies how user input is handled.

## e-Dog

This project is structured as a series of apps. A brief summary of each will be provided.

`browse`
 
The browse app handles most of the post showcasing. It includes the home page and search results.

`post`

The post app handles everything related to posts. This includes creating/editing posts and viewing them after.

`user`

The user app handles all things related to accounts. Login, sign up, profile pages, and pinned posts are here.