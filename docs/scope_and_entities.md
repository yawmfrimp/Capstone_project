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
  - `user_id`, `username`, `email`,  `password`, `date joined` 
- **Movies**
  - `movie_id`, `title`, `director`, `description`, `release_date`, `genre`, `trailer_url`
- **Reviews**
  - `review_id`, `movie_id_fk`, `user_id_fkk`, `ratings(1-5)`, `comment`, `updated_at`, `created_at`
## Relationship mapping
- One user → Many Reviews
- One Movie → Many Reviews
- Unique Constraint: a User can post only one review per Movie
- On deletion of a Movie: all Reviews of said movie are also deleted
- On deletion of a User: all reviews of said user are also deleted
