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
static int dump_info(void){
        int fd;
        ssize_t ret;
        struct person p;
        fd = open("person_info", O_RDONLY);
        if(fd == -1){
                printf("open error\n");
                return -1;
        }

        do{
                ret = read(fd, &p, sizeof(struct person));
                if(ret == -1){
                        printf("read() fail\n");
                        close(fd);
                        return -1;
                }else if(ret == 0){
                        FILE *fp;
                        fp = fopen("person_info", "r");
                        if(fp == NULL){
                                printf("fopen() fail\n");
                                close(fd);
                                return -1;
                        }
                        printf("file position = %ld\n", ftell(fp));
                        fclose(fp);
                        break;
                }
                else if(ret != sizeof(struct person)){
                        printf("read fail\n");
                        close(fd);
                        return -1;
                }
                                printf("%zd",ret);
                printf("name: %s, age: %d\n", p.name, p.age);
        }while(1);

        close(fd);
        return 0;
}


int main(int argc, char **argv){
        struct person persons[] = {
                {"kim",40},
                {"kang",28}
        };
        write_info(&persons[0]);
        write_info(&persons[1]);
        dump_info();
        return 0;
}
