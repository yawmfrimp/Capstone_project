# Project Scope & Entities
## Overview
This Project is aimed at creating a Movie review API where registered users can create and review movies and browse reviews posted by other registered users
## In Scope Features (v1)
Core domain: movies, reviews, auth
- **CRUD for reviews** - Let users create, update, and delete their reviews 
- **Movies** - Let's admins curate movies for review 
- **User Authentication** - Signup, login, profile management
## Planned Later
- Upvotes on reviews
- Watchlists/favourites
- Comments or threaded discussions
- External API import for movies
## Out of Scope (for now)
- Streaming links, payments
## Entity list and descriptions
- **User**:
  - `user_id` → Primary Key, Auto-increment integer
  - `username` → Char(100)
  - `email` → Emailfield,  UNIQUE, case insensitive
  - `password` → Char(128), stored hashed via Django's built-in auth
  - `date joined` → Datefield, defaults to current_date
- **Movies**
  - `movie_id`→ Primary Key, Auto-increment integer
  - `title` → char(200), index for search queries
  - `director` → Textfield, optional
  - `description` → char(200), optional
  - `release_date` → Datefield, YYYY-MM-DD
  - `genre` → Char(100), optional
  - `trailer_url` → URLfield, optional
- **Reviews**
  - `review_id` → Primary Key, Auto-increment integer
  - `movie_id_fk` → Movie, on_delete=CASCADE
  - `user_id_fk` → User, on_delete=CASCADE  
  - `ratings(1-5)` → Integerfield, 1-5 range enforced at model level
  - `comment` → textfield
  - `updated_at` →DateTimefield, default timezone.now
  - `created_at` →DateTimefield
## Relationship mapping
- One user → Many Reviews
- One Movie → Many Reviews
- Unique Constraint: a User can post only one review per Movie
- On deletion of a Movie: all Reviews of said movie are also deleted
- On deletion of a User: all reviews of said user are also deleted
