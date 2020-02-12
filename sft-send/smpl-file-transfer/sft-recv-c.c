/* $Id:$ */

/* 
 *	Simple File Transfer protocol receiver 
 *
 *	Header:
 *		SIMPLE-FILE-TRANSFER|filename|size\n
 */

#define _GNU_SOURCE
#include <errno.h>
#include <fcntl.h>
#include <stdio.h>
#include <string.h>
#include <sys/select.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <unistd.h>
#include <string.h>
#include <stdlib.h> /* strtol */

const char header_start[] = "SIMPLE-FILE-TRANSFER|";
const int  header_start_len = sizeof(header_start) - 1;

#define BUF_SIZE 0xff
int len = 0;
char buf[0xfff];

char tmp[0xfff];	/* for strtol() */

#define FILENAME_MAX_LEN 80
char filename[FILENAME_MAX_LEN];

int fsize;
int fd = -1;

#define HEADER_MAX 	  (header_start_len + FILENAME_MAX_LEN + 25) /* 25 == цифры, два '|' и \n */

int main()
{
	char *p;
	int llen;

	for (;;)
	{

		char c;
		llen = read(STDIN_FILENO, &c, 1);	/* переделать на получение строки? */

		if (llen == 0)
			return 0;

		buf[len++] = c;

		/* printf(">len: %d, fsize: %d, %c\n", len, fsize, c); */
		/* заполняем буфер строкой или до конца буфера или до конца принимаемого файла */
		if (len < BUF_SIZE && c != '\n' )
		{
			if (fsize == 0)
				continue;
			else if (len < fsize)
					continue;
		}
				

		/* printf("len: %d, fsize: %d, %c\n", len, fsize, c); */

		/* пытаемся в буфере найти новый заголовок.
		 * заголовок может прийти и в середине файла, и начнется прием нового файла.
		 * это борьба с "зависшими" передачами.
		 */
		if ((p = memmem(buf, len, header_start, header_start_len)) != NULL)
		{
			int i;

			p += header_start_len;
			for (i = 0;*p != '|' && i < FILENAME_MAX_LEN;p++, i++)
				filename[i] = *p;

			if (i != FILENAME_MAX_LEN)
			{
				int tmp_fsize;
				char *end;

				filename[i] = 0;

				p++;
				llen = len - (p - buf); /* длина строки с цифрой */
				memcpy (tmp, p, llen);
				tmp[llen - 1] = '\0';	/* for strtof() */

				tmp_fsize = strtol(tmp, &end, 0);

				if((errno == ERANGE || ((fsize == 0) && (tmp == end))) || *end == '\0')
				{
					/* тут распознался новый заголовок */
					if (fd != -1)
					{
						fprintf (stderr, "can't reveive %d bytes for file\n", fsize);
						close(fd);
					}

					printf ("start receive filename: %s, size %d \n", filename, tmp_fsize);

					if ((fd = open (filename, O_CREAT|O_WRONLY|O_TRUNC, 0666)) != -1)
						fsize = tmp_fsize;
					else
						fprintf (stderr, "error open file: %s, \"%s\"\n", filename, strerror(errno));
					len = 0;	/* TODO: вставить contunue ??? */
				}
			}
		}

		/* если мы в процессе принятия файла и в буфере что то есть - начинаем писать */
		if (len != 0 && fsize != 0 && fd != -1)
		{
			llen = len;
			if (len == BUF_SIZE)
			{
				/*
				 * если у нас полный буфер, то отдаем не весь буфер, а оставляем часть
				 * в которой может начинатся заголовок
				 */
				llen = len - HEADER_MAX + 1;
			}

			/* printf ("llen = %d, len = %d, HEADER_MAX = %d, header_start_len: %d\n" */
					/* , llen, len , HEADER_MAX, header_start_len, FILENAME_MAX_LEN); */

			llen = write (fd, buf, fsize < llen ? fsize : llen);
			if (llen == -1)
			{
				fprintf (stderr, "error write to file: \"%s\"\n", strerror(errno));
				fsize = 0;
				len   = 0;
			}
			else
			{
				fsize -= llen;
				len   -= llen;
			}

			if (fsize == 0)
			{
				printf ("file done\n");
				close(fd);
				fd = -1;
			}
		}
		else if (len != 0)	/* TODO: улучшить вывод дропнутых байтов, что бы не выводилось для каждого набранного буфера */
			printf ("drop %d bytes\n", len);

	}

	return 0;
}
