WITH foo AS (
    SELECT
            a, b, c
    FROM
            mytable
)

INSERT INTO other_table ( one, two, three )
SELECT a, b, c
FROM foo
