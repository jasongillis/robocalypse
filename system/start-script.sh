#!/bin/bash

# Determine what card ID the USB sound card has
card_number=`arecord -l | sed -n 's/^card \([[:digit:]]\)\: Device.*$/\1/p'`
asoundrc_file="/home/jgillis/robocalypse/system/asoundrc-card${card_number}"

echo "Considering $asoundrc_file"
if [ ! -f "${asoundrc_file}" ]; then
    echo "The asoundrc file doesn't exist"
    exit 1
fi

# Copy the correct ALSA sound rc file in place
cp "$asoundrc_file" "/home/jgillis/.asoundrc"

count=0
wled_is_down=1
while [ $wled_is_down -eq 1 ]
do
    if ping -c 1 192.168.199.2 &> /dev/null
    then
        wled_is_down=0
    else
        echo "Waiting for WLED... $((120 - count)) seconds remaining"
        count=$((count + 1))
        sleep 1
    fi

    if [ $count -ge 120 ]; then
        echo "WLED is not coming up"
        exit 1
    fi
done

python /home/jgillis/robocalypse/button_reader.py
