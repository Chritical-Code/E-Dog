# e-Dog

#### | Overview | [Development](docs/development.md) |

## Overview

### A web app for buying and selling dogs. Made in Django (Python).

![Home page](/docs/images/overview.png)

## Features

### Accounts

Users can sign up to create an account, log in, view account details, and log out.

![Account page](/docs/images/account.png)

### Creating Posts

Users can create and edit posts for dogs they wish to sell.

![Edit post page](/docs/images/edit.png)

### Viewing Posts

Users can click on posts to view more details about the dog. Each post will also link to the seller's profile.

![Post page](/docs/images/post.png)

### Pins

Users can pin posts they find, making them easy to locate later.

![Pins page](/docs/images/pin.png)

### Search

Users can search for specific breeds of dog, making it easy to find what they are looking for.

![Search page](/docs/images/search.png)

## Technical Details

This is a web application built using the Django framework. The backend is written in Python. A SQL database is used to store data. The frontend uses Django's Templates, incorporating HTML, CSS, and JavaScript. The demo site is being hosted on a VPS, configured with Nginx as the proxy server and Gunicorn as the application server. 