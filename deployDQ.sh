if [ "$#" -ne 1 ]
  then
    echo "Please pass in DQ folder name under lib/local"
    exit 1
fi
scp -r /home/hermes/v2/lib/local/$1/. jlu@resnow-dev.decipherinc.com:/home/hermes/v2/lib/local/$1
scp -r /home/hermes/v2/lib/local/$1/. jlu@rnuk.decipherinc.com:/home/hermes/v2/lib/local/$1
scp -r /home/hermes/v2/lib/local/$1/. jlu@rnca.decipherinc.com:/home/hermes/v2/lib/local/$1
scp -r /home/hermes/v2/lib/local/$1/. jlu@rnau.decipherinc.com:/home/hermes/v2/lib/local/$1
