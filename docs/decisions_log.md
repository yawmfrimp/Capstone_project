# Decisions Log

| Date	        | Category                              | Decision	                                     | Status             |     Reasoning                                                          |
| --------------|---------------------------------------|------------------------------------------------|--------------------|------------------------------------------------------------------------|
| 2025‑08‑14	  |  Database                             | MySQL for DB	                                 | Final              | Familiarity, solid tooling in Django, available in hosting environment |
| 2025‑08‑14	  |  Permissions                          | Admin‑only movie creation in v1	               | Amendable          | Ensures data integrity & avoids spam |
| 2025‑08‑14	  |  Data Integrity                       | Review uniqueness by (user, movie)	           | Final              | Prevent duplicate reviews clutter |
| 2025-08-14    |  Data Integrity                       | User email uniqueness                          | Amendable          | Prevents a single email from creating multiple accounts |
