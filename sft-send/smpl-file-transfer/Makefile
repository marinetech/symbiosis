#CROSS=arm-linux-gnueabi-
#CC=$(CROSS)gcc-9

#CROSS=arm-angstrom-linux-uclibceabi-
#CROSS=arm-linux-
CC=$(CROSS)gcc

STRIP=$(CROSS)strip
#CFLAGS=-static -W -Wall -mfloat-abi=soft -march=armv5te  -mthumb-interwork
#CFLAGS=-static -W -Wall -I /opt/arcom/arm-elf/include/ -L /opt/arcom/arm-elf/lib -I /opt/arcom/arm-linux/lib/dietlibc/include/
#CFLAGS=-static -W -Wall -L /opt/arcom/arm-elf/lib -I /opt/arcom/arm-linux/lib/dietlibc/include/ -march=armv5te
CFLAGS=-static -W -Wall -I /opt/arcom/arm-linux/lib/dietlibc/include/ -L /opt/arcom/arm-linux/lib/dietlibc/lib-arm -L /opt/arcom/lib/gcc/arm-elf/3.4.4/
all:
	$(CC) $(CFLAGS) -o sft-recv-c sft-recv-c.c
	$(STRIP) sft-recv-c
strace:
	strace -f $(CC) $(CFLAGS) -o sft-recv-c sft-recv-c.c 2>&1
	$(STRIP) sft-recv-c
