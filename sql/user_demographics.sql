SELECT
    SUM(CASE WHEN EXTRACT(YEAR FROM CURRENT_DATE()) - birth_year <= 25 AND gender = 'male' THEN 1 ELSE 0 END) AS young_male,
    SUM(CASE WHEN EXTRACT(YEAR FROM CURRENT_DATE()) - birth_year <= 25 AND gender = 'female' THEN 1 ELSE 0 END) AS young_female,
    SUM(CASE WHEN EXTRACT(YEAR FROM CURRENT_DATE()) - birth_year > 25 AND EXTRACT(YEAR FROM CURRENT_DATE()) - birth_year <= 60 AND gender = 'male' THEN 1 ELSE 0 END) AS middle_aged_male,
    SUM(CASE WHEN EXTRACT(YEAR FROM CURRENT_DATE()) - birth_year > 25 AND EXTRACT(YEAR FROM CURRENT_DATE()) - birth_year <= 60 AND gender = 'female' THEN 1 ELSE 0 END) AS middle_aged_female,
    SUM(CASE WHEN EXTRACT(YEAR FROM CURRENT_DATE()) - birth_year > 60 AND gender = 'male' THEN 1 ELSE 0 END) AS elder_male,
    SUM(CASE WHEN EXTRACT(YEAR FROM CURRENT_DATE()) - birth_year > 60 AND gender = 'female' THEN 1 ELSE 0 END) AS elder_female
FROM `{{ project }}.{{ dataset }}.trips` t