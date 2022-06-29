#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>
#include <unistd.h>
#include <sys/stat.h>
#include <fcntl.h>

struct person{
        char name[32];
        int age;
};

static int write_info(struct person *p){
        int fd;
        ssize_t ret;
        fd = open("person_info", O_CREAT|O_WRONLY|O_APPEND, 0644);
        if(fd == -1){
                printf("open error\n");
                return -1;
        }

        ret = write(fd, p, sizeof(struct person));
        if(ret == -1){
                printf("write error\n");
                close(fd);
                return -1;
        }
        else if(ret != sizeof(struct person)){
                printf("write() fail(partial write)\n");
                close(fd);
                return -1;
        };
        close(fd);
        return 0;
}
