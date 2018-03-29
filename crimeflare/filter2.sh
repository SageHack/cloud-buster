#!/bin/sh
#
# Turn out using this was a bit overkill as some origin did
# not answer the CURL request in time but are still valid.
#
# I'm keeping this here but it's not really useful for now.
#
# Save dead origins from the Crimeflare DB.
# Take about 3 hours to complete.
# 
# Using CTRL+C kills CURLs command and not the bash script
# use `killall filter2.sh`


# check hosts in a file and keeps the one behind Cloudflare
parse() {
    for ip in $(cat $1)
    do
        hdr1=$(curl -m 4 -Iks $ip -H 'Host: www.example.com' -H "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.89 Safari/537.36" | head -n1)
        echo "$ip $hdr1"

        if [ -z "$hdr1" ]
        then
            echo "$ip" >> ipout-invalid-origin
        fi

        # delete host entry once scanned
        #sed -i "/$host/d" $1
    done
}


# empty filtered output file
true > ipout-invalid-origin

# fetch all ips
# cat ipout | cut -d' ' -f2 | sort | uniq > ipout-ips

# split the list into multiple files to allow multiple processes
split -l 5000 ipout-ips

# start parsing in multiple processes
for split_file in $(ls x*)
do
    parse $split_file &
done

# wait for parsing to complete
wait

# rm -f x*
# rm -f ipout-ips

# cat ipout-invalid-ips | sort | uniq > tmp
# mv tmp ipout-invalid-ips
# rm ipout-invalid-origin
