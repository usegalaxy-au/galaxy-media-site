-- Copy scraped data into database

-- Need to manually create supporters and tags first

\c ga_site;

BEGIN;

COPY events_event
  FROM '/home/cameron/dev/galaxy/galaxy-content-site/scrape/data/events.tab'
  WITH (
  FORMAT csv,
  HEADER true,
  DELIMITER E'\t',
  QUOTE '~',
  NULL ''
);

COPY news_news
  FROM '/home/cameron/dev/galaxy/galaxy-content-site/scrape/data/news.tab'
  WITH (
  FORMAT csv,
  HEADER true,
  DELIMITER E'\t',
  QUOTE '~',
  ESCAPE E'\\',
  NULL ''
);

COPY events_event_supporters
  FROM '/home/cameron/dev/galaxy/galaxy-content-site/scrape/data/event_supporters_oids_2.tab'
  WITH (
  FORMAT csv,
  DELIMITER E'\t',
  QUOTE '~',
  ESCAPE E'\\',
  NULL ''
);


COPY events_event_tags
  FROM '/home/cameron/dev/galaxy/galaxy-content-site/scrape/data/event_tags_oids_2.tab'
  WITH (
  FORMAT csv,
  DELIMITER E'\t',
  QUOTE '~',
  ESCAPE E'\\',
  NULL ''
);

COPY news_news_supporters
  FROM '/home/cameron/dev/galaxy/galaxy-content-site/scrape/data/news_supporters_oids_2.tab'
  WITH (
  FORMAT csv,
  DELIMITER E'\t',
  QUOTE '~',
  ESCAPE E'\\',
  NULL ''
);

COPY news_news_tags
  FROM '/home/cameron/dev/galaxy/galaxy-content-site/scrape/data/news_tags_oids_2.tab'
  WITH (
  FORMAT csv,
  DELIMITER E'\t',
  QUOTE '~',
  ESCAPE E'\\',
  NULL ''
);

COMMIT;
