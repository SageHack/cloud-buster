#!/bin/sh
#
# Save working and protected hosts from Crimeflare DB.
# Take about 6 hours to complete.
# 
# Using CTRL+C kills CURLs command and not the bash script
# use `killall ipout-filter.sh`


# check hosts in a file and keeps the one behind Cloudflare
parse() {
    for host in $(cat $1)
    do
        cfray=$(curl -m 2 -Is $host | grep -i cf-ray | sed "s/CF-RAY: //")
        echo "$host $cfray"

        if [ ! -z "$cfray" ]
        then
            echo "$host $cfray" >> ipout-protected
        fi

        # delete host entry once scanned
        #sed -i "/$host/d" $1
    done
}


# empty filtered output file
true > ipout-protected

# fetch all hosts from Crimeflare DB
cat ipout | cut -d' ' -f1 | sort | uniq > ipout-hosts

# split the list into multiple files to allow multiple processes
split -l 25000 ipout-hosts 

# start parsing in multiple processes
for split_file in $(ls x*)
do
    parse $split_file &
done

# wait for parsing to complete
wait

rm -f x*
rm -f ipout-hosts

cat ipout-protected | cut -d' ' -f1 | sort | uniq > ipout-protected.sorted
mv ipout-protected.sorted ipout-protected
