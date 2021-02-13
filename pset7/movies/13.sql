SELECT distinct(name) FROM people JOIN stars ON stars.person_id = people.id
WHERE name != "Kevin Bacon" and movie_id IN (SELECT movie_id
FROM  stars JOIN people ON people.id = stars.person_id WHERE name = "Kevin Bacon"
and birth = 1958)
