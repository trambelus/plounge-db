# Divide two counts
SELECT v1.author, nsc, 100*nsc/ntl pct FROM
  (SELECT author, COUNT(*) nsc FROM comments c1
    WHERE udate > DATE('now','-3 months') 
    AND body LIKE '%scoot%' GROUP BY c1.author
    HAVING nsc >= 50) v1
  INNER JOIN
  (SELECT author, COUNT(*) ntl FROM comments c2
    WHERE udate > DATE('now','-3 months')
    GROUP BY c2.author) v2
  ON v1.author = v2.author ORDER BY pct DESC

 # Relations
 SELECT x.author a, y.author b FROM comments x INNER JOIN comments y ON x.id = y.parent_id GROUP BY a,b

 #Undirected Relations
SELECT DISTINCT
    CASE WHEN x.author > y.author THEN
        x.author ELSE y.author END AS a,
    COUNT(*)*19/3282+1 AS n,
    CASE WHEN x.author > y.author THEN
        y.author ELSE x.author END AS b
FROM comments AS x
INNER JOIN comments AS y
    ON x.id = y.parent_id
WHERE a != '[deleted]' AND b != '[deleted]'
AND y.udate > DATE('now','-6 months')
GROUP BY a, b HAVING COUNT(*) >= 100
ORDER BY COUNT(*) DESC

#Directed Relations
SELECT x.author as a, y.author as b, COUNT(*) as n
FROM comments AS x
INNER JOIN comments AS y
    ON x.id = y.parent_id
WHERE a != '[deleted]' AND b != '[deleted]'
    AND y.udate > DATE('now','-6 months')
GROUP BY a, b HAVING COUNT(*) >= 42
ORDER BY n DESC

# Hypeline
SELECT v1.ud, 100*CAST(nsp AS FLOAT)/ntl pct, nsp, ntl FROM
(SELECT DATE(udate) ud, COUNT(*) ntl FROM comments c1
  GROUP BY ud) v1
LEFT OUTER JOIN
(SELECT DATE(udate) ud, COUNT(*) nsp FROM comments c2
  WHERE body LIKE '%hype%' GROUP BY ud) v2
ON v1.ud = v2.ud ORDER BY v1.ud

# Average score
SELECT author, AVG(score) FROM comments WHERE author IN (
  SELECT author FROM comments WHERE udate > DATE('now','-100 days')
  GROUP BY author ORDER BY COUNT(*) DESC LIMIT 100)
GROUP BY author ORDER BY a DESC

# Hourly activity
SELECT STRFTIME('%H',udate) hour, COUNT(*) N FROM comments
WHERE author = '%s' GROUP BY hour ORDER BY hour

# Normalized hourly activity
SELECT hour, 100*CAST(N AS FLOAT)/T pct FROM
(SELECT STRFTIME('%H',udate) hour, COUNT(*) N FROM comments WHERE author = '{0}' GROUP BY hour) q1
LEFT JOIN (SELECT COUNT(*) T FROM comments WHERE author = '{0}') q2

# Normalized hourly activity by weekday
SELECT z.hour,
100*CAST(a.N AS FLOAT)/T sun,
100*CAST(b.N AS FLOAT)/T mon,
100*CAST(c.N AS FLOAT)/T tue,
100*CAST(d.N AS FLOAT)/T wed,
100*CAST(e.N AS FLOAT)/T thu,
100*CAST(f.N AS FLOAT)/T fri,
100*CAST(g.N AS FLOAT)/T sat
FROM (
  (SELECT STRFTIME('%H',udate) hour, COUNT(*) N FROM comments WHERE author = '{0}'
    AND udate > DATE('2014-12-01') GROUP BY hour) z
  LEFT JOIN
  (SELECT STRFTIME('%H',udate) hour, COUNT(*) N FROM comments WHERE author = '{0}'
    AND udate > DATE('2014-12-01') AND STRFTIME('%w',udate) = '0' GROUP BY hour) a
  ON (z.hour = a.hour) LEFT JOIN
  (SELECT STRFTIME('%H',udate) hour, COUNT(*) N FROM comments WHERE author = '{0}'
    AND udate > DATE('2014-12-01') AND STRFTIME('%w',udate) = '1' GROUP BY hour) b
  ON (z.hour = b.hour) LEFT JOIN
  (SELECT STRFTIME('%H',udate) hour, COUNT(*) N FROM comments WHERE author = '{0}'
    AND udate > DATE('2014-12-01') AND STRFTIME('%w',udate) = '2' GROUP BY hour) c
  ON (z.hour = c.hour) LEFT JOIN
  (SELECT STRFTIME('%H',udate) hour, COUNT(*) N FROM comments WHERE author = '{0}'
    AND udate > DATE('2014-12-01') AND STRFTIME('%w',udate) = '3' GROUP BY hour) d
  ON (z.hour = d.hour) LEFT JOIN
  (SELECT STRFTIME('%H',udate) hour, COUNT(*) N FROM comments WHERE author = '{0}'
    AND udate > DATE('2014-12-01') AND STRFTIME('%w',udate) = '4' GROUP BY hour) e
  ON (z.hour = e.hour) LEFT JOIN
  (SELECT STRFTIME('%H',udate) hour, COUNT(*) N FROM comments WHERE author = '{0}'
    AND udate > DATE('2014-12-01') AND STRFTIME('%w',udate) = '5' GROUP BY hour) f
  ON (z.hour = f.hour) LEFT JOIN
  (SELECT STRFTIME('%H',udate) hour, COUNT(*) N FROM comments WHERE author = '{0}'
    AND udate > DATE('2014-12-01') AND STRFTIME('%w',udate) = '6' GROUP BY hour) g
  ON (z.hour = g.hour) LEFT JOIN
  (SELECT COUNT(*) T FROM comments WHERE author = '{0}'
    AND udate > DATE('2014-12-01'))
)