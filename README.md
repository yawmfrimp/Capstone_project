# MOVIE REVIEW API - A secure scalable Django + MySQL backend for managing movies, reviews, and user interactions

# OVERVIEW
- The Project is an API created for reviewing movies and aggregating the reviews for everyone.
- This Project is for every movie lover who wants an opinion on movies to watch 
- The Project creates a place where movies are shared and reviewed for all to see
- This project is a Django‑based Movie Review API where registered users can browse movies, post one review per movie, and read reviews from others. Admins manage the movie catalog, while members can create, update, and delete their own reviews. Core features include CRUD for reviews, movie management, and secure user authentication, with future plans for upvotes, watchlists, comments, and external movie imports. The data model enforces relationships between users, movies, and reviews, ensuring referential integrity and unique user‑movie reviews.

# SCOPE
- The Movie Review API is a Django‑based backend designed to let registered users browse a curated catalog of movies, post one review per title, and read feedback from other members. Core functionality in the current scope includes secure user authentication (signup, login, profile management), full CRUD operations for user‑authored reviews, and administrative tools for managing the movie list. The system enforces clear relationships between users, movies, and reviews, ensuring each user can only review a movie once, and that deleting a movie or user cascades to remove their associated reviews.

- Planned future enhancements extend beyond the initial release, with features such as upvoting reviews, creating watchlists or favourites, adding threaded comments, and importing movie data from external APIs. Out‑of‑scope items for now include streaming links and payment integrations, keeping the focus on building a secure, scalable foundation for community‑driven movie discussions.

- For more details, check the scope and entities file (https://github.com/yawmfrimp/Capstone_project/blob/main/docs/scope_and_entities.md#in-scope-features-v1)

- # ENTITIES AND RELATIONSHIPS
- ![ERD](https://github.com/user-attachments/assets/24513ee9-f423-415b-9e6d-431827c5bea6)
- ## Entity list and descriptions
- **User**: Authenticated users on the platform who can post reviews, edit and delete their own reviews

- **Movies**: Movies that will be curated by admins for the site

- **Reviews**: Reviews on movies by authenticated users on the site featurring a rating system from 1-5
- For attribute level details click this link https://github.com/yawmfrimp/Capstone_project/blob/main/docs/scope_and_entities.md#entity-list-and-descriptions

# TECH STACK
- Django
- Django REST Framework
- MySQL
- Python

# INSTALLATION AND SETUP
- Clone repo
- Create virtual environment
- Install dependencies
- Set up .env file
- Run migrations
- Start server

