# Obtain Performance Profile
python -m cProfile -o temp.dat <PROGRAM>.py
snakeviz temp.dat
