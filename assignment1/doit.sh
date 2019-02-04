#/bin/bash

source ~/miniconda3/bin/activate ml

set -x

if [ "$1" == "" ]; then
    echo "Missing phone number"
    exit
fi

aws sns publish --region us-west-2 --phone-number $1 --message "Start of run at $(date)"

date
#for i in dt boosting knn ann svm; do
for i in svm ann; do
    aws sns publish --region us-west-2 --phone-number $1 --message "starting $i"
    time nice python run_experiment.py --threads -2 --$i --verbose --seed 12345
    aws sns publish --region us-west-2 --phone-number $1 --message "$i done at $(date)"
done
date

#tar zcf ~/dt-output-72core.tgz output*
#aws s3 cp ~/dt-output-72core.tgz s3://bnisly-results/dt-output-72core.tgz
#sudo shutdown now
