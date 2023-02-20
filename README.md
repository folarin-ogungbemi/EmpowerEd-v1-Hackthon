# Education Platform for Underprivileged Children

[EmpowerEd](team4-empowered.herokuapp.com/) is an educational platform developed with the aim to provide education resources to underprivileged children. The application has a range of features to make learning interactive, accessible and engaging for students while also allowing students to connect with mentors, and providing the avenue for parents to communicate conveniently with teachers. In summary, the Website aim to achieve the goal of creating an education enabled environment for students.

## Table of contents

* [Purpose](#purpose)

* [UX Design](#ux-design)
  * [User Stories](#user-stories)
  * [UAC](#uac)
  * [Structure](#structure)

* [Wireframes](#wireframes)

* [Design](#design)

* [Development Plan](#development-plan)

* [Architecture](#architecture)

* [Data Model](#data-model)

* [Features](#features)
  * [Feature Considerations](#feature-considerations)

* [Testing](#testing)

* [Technologies](#technologies)
  * [Languages](#languages)
  * [Programs, frameworks, libraries](#programs-frameworks-libraries)

* [Deployment](#deployment)

* [Credits](#credits)


# Purpose

Django framework is utilized to build the website, which serves as the backend and handles tasks such as user authentication, data management, and routing. Moreover, the majority of the frontend is also handled by Django. A key feature of the website is the implementation of a React component that enables real-time communication and updates via WebSockets. As a result, users can enjoy a seamless and interactive experience, with parts of the website updating in real-time without the need to refresh the page. Overall, the website leverages Django's power and flexibility, as well as React and WebSockets' dynamic capabilities, to deliver a smooth and responsive user experience.
[The live website is available here](team4-empowered.herokuapp.com/)

___

# UX Design
## User stories


### As a **first time user**

### As a **returning user**

___
## UAC
___


## Structure


### Home Page

### Sign Up Page

### Sign In Page
___

___
# Development Plan

## Agile design

The development of the website has followed an Agile methodology, using GitHub's projects to prioritize and track user stories and features. The approach enabled the implementation of ideas based on their level of importance, ensuring that the website functionality and user experience were not compromised. The following categories were applied, as well as corresponding labels were created:

> - must have
> - should have
> - would have
> - could have

The project was constrained by time limitations, which resulted in some initially listed features not being implemented. However, AGILE methodology is incredibly helpful in situations like this, as it allows for the prioritization and tracking of user stories. Completed user stories are in the "Done" section and the ones that were not prioritised for the first iteration are currently in the "To Do" section to be covered in the next iteration.

See the current state of the project here. [EmpowerEd](team4-empowered.herokuapp.com/)

Using a hybrid architecture has a significant advantage of using Django's built-in tooling to handle authentication, which means that we can easily add authentication functionalities to our hybrid Django view without relying on complicated third-party authentication workflows. Another advantage of the hybrid architecture is that it allows us to send data to the frontend in two different ways, either by passing the data directly to the template using Django's templating system, or by providing the data through asynchronous APIs using JavaScript and Django REST framework. This method enables fast data loading using the native fetch API and authentication is handled seamlessly by the Django session cookie, without wrestling with CORS.

Using React for the frontend, specifically for a real-time Messenger, we can provide a smooth and responsive user experience due to React's performance benefits. React is also highly modular, enabling the easy scaling of different parts of the application independently as needed. This makes it simpler to add new features or make changes to the application without affecting other parts of the codebase, as well as simplifying the debugging and testing processes.
___
# Design

### Colour Scheme

### Typography

### Images

#### Hover effect

___
# Architecture

<img src="https://www.saaspegasus.com/static/images/web/modern-javascript/django-react-header.51a983c82dcb.png" width="300" />

A hybrid architecture - a single-page React app (Messenger) integrated into a Django project. This approach allows for multiple types of pages in the same project.

Here is a scheme of the structure:

![](https://www.saaspegasus.com/static/images/web/modern-javascript/js-pipeline-with-django.56456c10739f.png)
___
# Data Model

___
# Features

## AllAuth

AllAuth is a flexible solution for managing user authentication and registration. It uses session-based authentication instead of Django's token-based authentication to store the user's authentication information in the user's session. When a user logs in, AllAuth generates a new session for the user and saves their identifying information, such as their ID or username, in the session. The library then sends a session ID to the client as a session cookie, which is stored in the browser. Subsequent requests from the client include the session ID in the Cookie header of the HTTP request, allowing [django-allauth](https://django-allauth.readthedocs.io/en/latest/) to authenticate the user by looking up the associated session.

One of the main reasons we chose to use [django-allauth](https://django-allauth.readthedocs.io/en/latest/) is because of its flexibility and support for various authentication methods. Another reason is because of its scalability. 

### User Authentication 
The project uses a custom user model with email as a user id, instead of using Django's built-in User model, which means that users to register and log in to the website need to use their email address instead of a traditional username, it also uses a custom sign up form. 


___

# Technologies
## Languages
- HTML, CSS, JavaScript, TypeScript, Python+Django
## Programs, frameworks, libraries
- [Django](https://www.djangoproject.com/) for backend and frontend functionality.
- [Django AllAuth](https://django-allauth.readthedocs.io/en/latest/) for authentication, registration and account management.
- [Django Channels](https://channels.readthedocs.io/en/stable/) for websockets and ASGI.
- [Django Rest Framework](https://www.django-rest-framework.org/) for building API.
- [Redis](https://redis.io/) backend for handling WebSockets, to facilitate. Django Channels channel layers.
- [Redis Cloud](https://app.redislabs.com/#/) cloud database service based on Redis.
- [PostgreSQL](https://www.postgresql.org/) relational database.
- [Psycopg](https://www.psycopg.org/) PostgreSQL adapter for Python.
- [Elephant SQL](https://www.elephantsql.com/) to manage PostgreSQL databases.
- [Bootstrap](https://getbootstrap.com/) for styling.
- [Crispy Forms](https://django-crispy-forms.readthedocs.io/en/latest/) for pretty forms.
- [Crispy Bootstrap](https://pypi.org/project/crispy-bootstrap5/) for styling Crispy forms.
- [Boxicons](https://boxicons.com/) for icons.
- [FontAwesome](https://fontawesome.com/) for icons.
- [Google Fonts](https://fonts.google.com/) for typography.
- [Gitpod](https://gitpod.io/) IDE to develop the app.
- [GitHub](https://GitHub.com/) to host the source code.
- [AWS S3](https://aws.amazon.com/) Amazon web services s3 for static storage.
- [Heroku](https://www.heroku.com/) to deploy and host the live app.
- Git to provide version control (to commit and push code to the repository). 
- [Pillow](https://pypi.org/project/Pillow/) to create fake images for testing.
- [Unittest](https://docs.python.org/3/library/unittest.html) for Python unit-testing.
- [Techsini](https://tecnisih.com) to create the Mockup image in this README.
- [W3C HTML Markup Validator](https://validator.w3.org/) to validate HTML code.
- [W3C Jigsaw CSS Validator](https://jigsaw.w3.org/css-validator/) to validate CSS code.
- Code Institute's Template to generate the workspace for the project.
___

# Deployment

# Credits

## Media


## Design Template

## Code

## Acknowledgements

___
