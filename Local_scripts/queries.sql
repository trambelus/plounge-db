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