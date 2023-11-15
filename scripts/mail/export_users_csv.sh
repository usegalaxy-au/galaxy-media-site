#!/usr/bin/env bash

# This script exports all Galaxy users to a users_YYYY.csv file to be used for bulk mail

YEAR=2023

psql -c "select u.id, u.username, u.email, u.create_time, (select max(gs.create_time) from galaxy_session gs where gs.user_id = u.id) as last_login from galaxy_user u where (u.create_time > '${YEAR}-01-01' or (select max(gs.create_time) from galaxy_session gs where gs.user_id = u.id)  > '${YEAR}-01-01') order by u.id;" --csv > users_${YEAR}.csv
