-- Copy scraped data into database

-- Need to manually create supporters and tags first

\c ga_site;

COPY events_event
  FROM 'data/events.tab'
  OIDS true
  DELIMITER '\t'
  QUOTE '"'
  ESCAPE '\\'
  NULL ''
;

COPY events_event_supporters
  FROM 'data/events_supporters.tab'
  OIDS false
  DELIMITER '\t'
  QUOTE '"'
  ESCAPE '\\'
  NULL ''
;

COPY events_event_tags
  FROM 'data/events_tags.tab'
  OIDS false
  DELIMITER '\t'
  QUOTE '"'
  ESCAPE '\\'
  NULL ''
;

COPY news_news
  FROM 'data/news.tab'
  OIDS true
  DELIMITER '\t'
  QUOTE '"'
  ESCAPE '\\'
  NULL ''
;

COPY news_news_supporters
  FROM 'data/news_supporters.tab'
  OIDS false
  DELIMITER '\t'
  QUOTE '"'
  ESCAPE '\\'
  NULL ''
;

COPY news_news_tags
  FROM 'data/news_tags.tab'
  OIDS false
  DELIMITER '\t'
  QUOTE '"'
  ESCAPE '\\'
  NULL ''
;
