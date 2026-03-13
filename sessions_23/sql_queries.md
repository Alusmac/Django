
## 1. Select all books

```sql
SELECT *
FROM sessions_23_book;
```

## 2. Retrieve books with their authors

```sql
SELECT b.id, b.title, b.publication_year, a.name
FROM sessions_23_book b
         JOIN sessions_23_author a ON b.author_id = a.id;
```

## 3. Retrieve all reviews

```sql
SELECT r.id, r.text, r.rating, r.book_id
FROM sessions_23_review r;
```

## 4. Calculate average rating per author

```sql
SELECT a.id, a.name, AVG(r.rating) AS avg_rating
FROM sessions_23_author a
         JOIN sessions_23_book b ON b.author_id = a.id
         JOIN sessions_23_review r ON r.book_id = b.id
GROUP BY a.id, a.name;
```

## 5. Count reviews and calculate average rating per book

```sql
SELECT b.id,
       b.title,
       COUNT(r.id)   AS review_count,
       AVG(r.rating) AS avg_rating
FROM sessions_23_book b
         LEFT JOIN sessions_23_review r ON r.book_id = b.id
GROUP BY b.id, b.title
ORDER BY review_count DESC, avg_rating DESC;
```

## 6. Find authors with more than 10 reviews

```sql
SELECT a.id, a.name, COUNT(r.id) AS total_reviews
FROM sessions_23_author a
         JOIN sessions_23_book b ON b.author_id = a.id
         JOIN sessions_23_review r ON r.book_id = b.id
GROUP BY a.id, a.name
HAVING COUNT(r.id) > 10;
```

## 7. Count total number of books

```sql
SELECT COUNT(*)
FROM sessions_23_book;
```

## 8. Create indexes for performance optimization

```sql
CREATE INDEX idx_book_title ON sessions_23_book (title);
CREATE INDEX idx_book_publication_year ON sessions_23_book (publication_year);
CREATE INDEX idx_review_rating ON sessions_23_review (rating);
```

## 9. Insert a new book

```sql
INSERT INTO sessions_23_book (title, publication_year, author_id)
VALUES ('Example Book', 2023, 1);
```

## 10. Insert a review for a book

```sql
INSERT INTO sessions_23_review (text, rating, book_id)
VALUES ('Great book!', 5, 1);
```

