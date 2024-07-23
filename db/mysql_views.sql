CREATE VIEW `valid_faculty_view` AS
SELECT f.`name` AS faculty_name
FROM faculty f
WHERE f.`name` IS NOT NULL
    AND TRIM(f.`name`) <> ''
ORDER BY f.`name`;

CREATE VIEW `valid_university_view` AS
SELECT `name` AS university_name
FROM university
WHERE `name` IS NOT NULL
	AND TRIM(`name`) <> ''
ORDER BY `name`;
