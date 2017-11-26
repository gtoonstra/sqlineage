WITH foo AS (
    SELECT
            bar.a, bar.b, bar.c
    FROM
    ( 
        SELECT a, b, c 
        FROM mytable
    ) bar
)

INSERT INTO other_table ( one, two, three )
SELECT a, b, c
FROM foo
