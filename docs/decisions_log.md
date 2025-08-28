# Decisions Log

| Date	        | Category                              | Decision	                                     | Status             |     Reasoning                                                          |
| --------------|---------------------------------------|------------------------------------------------|--------------------|------------------------------------------------------------------------|
| 2025‑08‑14	  |  Database                             | MySQL for DB	                                 | Final              | Familiarity, solid tooling in Django, available in hosting environment |
| 2025‑08‑14	  |  Permissions                          | Admin‑only movie creation in v1	               | Amendable          | Ensures data integrity & avoids spam |
| 2025-08-14    |  Data Integrity                       | User email uniqueness                          | Amendable          | Prevents a single email from creating multiple accounts |
| 2025-08-14    |  Data Integrity                       | Enforce rating between 1-5 inclusive           | Final              | Keeps review scores within a defined range |
| 2025-08-14    |  Schema Design                        | fk relationships for review with on_delete=CASCADE | Final          | When the parent is deleted, all reviews are deleted as well |
| 2025-08-26    |  Security                             | created a .env file to secure database configurations | Final       | Ensures security of the database |
| 2025-08-28    |  Schema Design                        | created ordering by title for the movie list view     | Final       | To show a readily ordered list of movies |
| 2025‑08‑28	  |  Data Integrity                       | Review uniqueness by (user, movie)	           | Final              | Prevent duplicate reviews clutter |
| 2025-08-28      |  Schema Design                        | Modified the def strings to account for a null release date | Final | Prevent None value in def strings |
| 2025-08-28      |  Permission                         | Created access based roles for the user          | Final              | To prevent ordinary users from having admin level permission |