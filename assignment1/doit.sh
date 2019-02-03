#/bin/bash
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
    nice time python run_experiment.py --threads -2 --$i --verbose
    aws sns publish --region us-west-2 --phone-number $1 --message "$i done at $(date)"
done
date

