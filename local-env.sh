#!/bin/bash
container_id=''

function get_container_id () {
    container_id=`docker ps | grep homework-django-project | awk '{ print $1 }'`
    echo 'Container ID: '$container_id
}

alias homework-admin=`get_container_id && docker exec -it $container_id bash`