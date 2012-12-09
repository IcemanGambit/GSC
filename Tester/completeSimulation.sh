./run.sh HobroNet -n -tp 0 -c 0.4 -u 0 -o ../../TestResults/tp0c0_4
./run.sh HobroNet -u 10 -o ../../TestResults/tp0c0_4
./run.sh HobroNet -u 50 -o ../../TestResults/tp0c0_4
./run.sh HobroNet -u 100 -o ../../TestResults/tp0c0_4

./run.sh HobroNet -n -tp 0 -c 0.6 -u 0 -o ../../TestResults/tp0c0_6
./run.sh HobroNet -u 10 -o ../../TestResults/tp0c0_6
./run.sh HobroNet -u 50 -o ../../TestResults/tp0c0_6
./run.sh HobroNet -u 100 -o ../../TestResults/tp0c0_6

./run.sh HobroNet -n -tp 0 -c 0.8 -u 0 -o ../../TestResults/tp0c0_8
./run.sh HobroNet -u 10 -o ../../TestResults/tp0c0_8
./run.sh HobroNet -u 50 -o ../../TestResults/tp0c0_8
./run.sh HobroNet -u 100 -o ../../TestResults/tp0c0_8

./run.sh HobroNet -n -tp 0 -c 1.0 -u 0 -o ../../TestResults/tp0c1_0
./run.sh HobroNet -u 10 -o ../../TestResults/tp0c1_0
./run.sh HobroNet -u 50 -o ../../TestResults/tp0c1_0
./run.sh HobroNet -u 100 -o ../../TestResults/tp0c1_0

./run.sh HobroNet -n -tp 0 -c 1.2 -u 0 -o ../../TestResults/tp0c1_2
./run.sh HobroNet -u 10 -o ../../TestResults/tp0c1_2
./run.sh HobroNet -u 50 -o ../../TestResults/tp0c1_2
./run.sh HobroNet -u 100 -o ../../TestResults/tp0c1_2


./run.sh HobroNet -n -tp 0 -c 1.4 -u 0 -o ../../TestResults/tp0c1_4
./run.sh HobroNet -u 10 -o ../../TestResults/tp0c1_4
./run.sh HobroNet -u 50 -o ../../TestResults/tp0c1_4
./run.sh HobroNet -u 100 -o ../../TestResults/tp0c1_4

./run.sh HobroNet -n -tp 0 -c 1.6 -u 0 -o ../../TestResults/tp0c1_6
./run.sh HobroNet -u 10 -o ../../TestResults/tp0c1_6
./run.sh HobroNet -u 50 -o ../../TestResults/tp0c1_6
./run.sh HobroNet -u 100 -o ../../TestResults/tp0c1_6

./run.sh HobroNet -n -tp 0 -c 1.8 -u 0 -o ../../TestResults/tp0c1_8
./run.sh HobroNet -u 10 -o ../../TestResults/tp0c1_8
./run.sh HobroNet -u 50 -o ../../TestResults/tp0c1_8
./run.sh HobroNet -u 100 -o ../../TestResults/tp0c1_8

python FinalData.py ../TestResults/
