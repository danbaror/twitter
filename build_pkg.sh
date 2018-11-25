#!/bin/bash

if [ "$#" -lt 3 ]; then
   echo " ----------- "
   echo " Missing parameters. Please provide target dir, package name and tag."
   echo " Usage $0 <target dir> <package_name> <Tag>"
   echo " ----------- "
   exit 1
fi

repo="danbaror/dan-public"
target_dir=$1
package_name=$2
tag=$3

cd $target_dir
touch build_${package_name}_${tag}
docker image prune -f
docker build -t=$package_name:$tag .
container_id=$(docker ps -a| grep $package_name | cut -d" " -f1)
docker container prune -f
# docker container rm $container_id
# docker commit $container_id $package_name

# docker image ls| grep $package_name | grep $tag
# image_info=$(docker image ls| grep $package_name | grep $tag)
# image_id=$(echo $image_info| cut -d" " -f3)
# echo " Image Info: " $image_info "  Image ID" $image_id
docker tag $package_name:$tag $repo:$package_name
docker images ls
docker push $repo:$package_name
