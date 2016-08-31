#!/bin/bash

# Script to setup some extra disks in an emulated manner 
#  folks like the ceph project need native disks to test against

# 2016-01-30 Patrick Laimbock and K Singh

if [ ! $1 ]; then
  echo 'Call this script with $1 = size in GB'
  exit 1
fi
size=$1
fname=/var/$(mktemp -u)
if [ ! -e /usr/bin/qemu-img ]; then
  yum -y -d0 install qemu-img
fi
qemu-img create -f raw $fname ${size}G
if [ $? -ne 0 ]; then 
  echo 'failed to create host file'
  exit 1
fi
parted ${fname} mklabel gpt
parted -a optimal ${fname} mkpart p ext2 1024 100%
#kpartx -l ${fname} | grep -v 'deleted' | cut -f1 -d\ 
kpartx -avs ${fname} | grep 'add map' | cut -f8 -d\ 
