CC = python3
CFLAGS = -t -Wall

default: maze.py
	$(CC) maze.py $(CFLAGS)
