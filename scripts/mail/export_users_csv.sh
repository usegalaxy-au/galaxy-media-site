#!/usr/bin/env bash

# This script exports all Galaxy users to a users_2023.csv file to be used for bulk mail

psql -c "select u.id, u.username, u.email, u.create_time, (select max(gs.create_time) from galaxy_session gs where gs.user_id = u.id) as last_login from galaxy_user u where (u.create_time > '2023-01-01' or (select max(gs.create_time) from galaxy_session gs where gs.user_id = u.id)  > '2023-01-01') order by u.id;" --csv > users_2023.csv
