select url, count(url) as 'count' from complete_leaguestats group by url order by url;

select * from complete_leaguestats where url ='http://lpl.qq.com/es/stats.shtml?bmid=2281';

select distinct url from complete_leaguestats where url NOT LIKE 'http://lpl%' and url NOT LIKE 'https://lpl%';