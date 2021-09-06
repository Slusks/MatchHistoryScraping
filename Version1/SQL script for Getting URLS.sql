

select * from complete_leaguestats where url ='http://lpl.qq.com/es/stats.shtml?bmid=2281';

select distinct url from complete_leaguestats where url NOT LIKE 'http://lpl%' and url NOT LIKE 'https://lpl%';

# As of the dataset that I pulled in August there are 283982 rows of data
#every non-lpl url should occur 12 times
select * from complete_leaguestats;

#There are 16757 matches with urls, and then 1212 without.
SELECT 
    url, COUNT(url) AS 'count'
FROM
    complete_leaguestats
WHERE
    url NOT LIKE 'http://lpl%'
	AND url NOT LIKE 'https://lpl%'
GROUP BY url
ORDER BY url;