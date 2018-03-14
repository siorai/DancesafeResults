# Python file for Literal SQL queries used by the backend

demoChart = r"""SELECT *
FROM sample
INNER JOIN event e on sample.eventid = e.id
INNER JOIN substances s2 on sample.finalconclusion = s2.id
WHERE e.name = 'Gem and Jam' AND e.year = 2018 AND sample.initialsuspect = sample.finalconclusion AND s2.name != 'UNKNOWN'"""

demoChart2 = r"""SELECT s2.name
FROM substances s2
INNER JOIN sample s3 on s2.id = s3.initialsuspect
INNER JOIN event e on s3.eventid = e.id
WHERE e.name = 'Gem and Jam' AND e.year = 2018 AND s3.initialsuspect = s3.finalconclusion AND s2.name != 'UNKNOWN'
ORDER BY s2.name"""
