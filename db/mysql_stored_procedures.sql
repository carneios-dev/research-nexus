DROP PROCEDURE IF EXISTS `get_faculty`;

DELIMITER $$
USE `academicworld`$$
CREATE PROCEDURE `get_faculty` ()
BEGIN
    SELECT faculty_name
    FROM valid_faculty_view;
END$$

DELIMITER ;

DROP PROCEDURE IF EXISTS `get_faculty_pubs_cites`;

DELIMITER $$
USE `academicworld`$$
CREATE PROCEDURE `get_faculty_pubs_cites` (IN faculty_name VARCHAR(512))
BEGIN
	SELECT f.`name` AS faculty_name,
		COUNT(p.id) AS publication_count,
		SUM(p.num_citations) AS total_citations
	FROM faculty f
	INNER JOIN faculty_publication fp ON f.id = fp.faculty_id
	INNER JOIN publication p ON fp.publication_id = p.id
	WHERE f.`name` = faculty_name
	GROUP BY f.`name`;
END$$

DELIMITER ;

DROP PROCEDURE IF EXISTS `get_universities`;

DELIMITER $$
USE `academicworld`$$
CREATE PROCEDURE `get_universities` ()
BEGIN
	SELECT university_name
	FROM valid_university_view;
END$$

DELIMITER ;

DROP PROCEDURE IF EXISTS `get_university_pubs_per_year`;

DELIMITER $$
USE `academicworld`$$
CREATE PROCEDURE `get_university_pubs_per_year` (IN university_name VARCHAR(512))
BEGIN
	SELECT p.`year`, COUNT(p.id) AS publication_count
	FROM publication p
	INNER JOIN faculty_publication fp ON p.id = fp.publication_id
	INNER JOIN faculty f ON fp.faculty_id = f.id
	INNER JOIN university u ON f.university_id = u.id
	WHERE u.`name` = university_name
	GROUP BY p.`year`
	ORDER BY p.`year`;
END$$

DELIMITER ;
