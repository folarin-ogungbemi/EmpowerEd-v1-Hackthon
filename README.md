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


___
# Data Model

___
# Features
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
