./run.sh HobroNet -n -tp 0 -c 1.8 -u 0 -o ../../TestResults/tp0c1_8
./run.sh HobroNet -u 10 -o ../../TestResults/tp0c1_8
./run.sh HobroNet -u 50 -o ../../TestResults/tp0c1_8
./run.sh HobroNet -u 100 -o ../../TestResults/tp0c1_8

./run.sh HobroNet -n -tp 0 -c 2.0 -u 0 -o ../../TestResults/tp0c2_0
./run.sh HobroNet -u 10 -o ../../TestResults/tp0c2_0
./run.sh HobroNet -u 50 -o ../../TestResults/tp0c2_0
./run.sh HobroNet -u 100 -o ../../TestResults/tp0c2_0

./run.sh HobroNet -n -tp 0 -c 2.2 -u 0 -o ../../TestResults/tp0c2_2
./run.sh HobroNet -u 10 -o ../../TestResults/tp0c2_2
./run.sh HobroNet -u 50 -o ../../TestResults/tp0c2_2
./run.sh HobroNet -u 100 -o ../../TestResults/tp0c2_2

./run.sh HobroNet -n -tp 0 -c 2.4 -u 0 -o ../../TestResults/tp0c2_4
./run.sh HobroNet -u 10 -o ../../TestResults/tp0c2_4
./run.sh HobroNet -u 50 -o ../../TestResults/tp0c2_4
./run.sh HobroNet -u 100 -o ../../TestResults/tp0c2_4

./run.sh HobroNet -n -tp 0 -c 2.6 -u 0 -o ../../TestResults/tp0c2_6
./run.sh HobroNet -u 10 -o ../../TestResults/tp0c2_6
./run.sh HobroNet -u 50 -o ../../TestResults/tp0c2_6
./run.sh HobroNet -u 100 -o ../../TestResults/tp0c2_6

python FinalData.py ../TestResults/
