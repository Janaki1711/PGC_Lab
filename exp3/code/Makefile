CC      = gcc
CFLAGS  = -fopenmp -O2 -Wall

TARGETS = race critical atomic barrier semaphore compare_sync

all: $(TARGETS)

race:         race.c
	$(CC) $(CFLAGS) -o $@ $<

critical:     critical.c
	$(CC) $(CFLAGS) -o $@ $<

atomic:       atomic.c
	$(CC) $(CFLAGS) -o $@ $<

barrier:      barrier.c
	$(CC) $(CFLAGS) -o $@ $<

semaphore:    semaphore.c
	$(CC) $(CFLAGS) -o $@ $<

compare_sync: compare_sync.c
	$(CC) $(CFLAGS) -o $@ $<

clean:
	rm -f $(TARGETS)

.PHONY: all clean
