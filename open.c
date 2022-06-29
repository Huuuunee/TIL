#include <stdio.h>
#include <string.h>
   
   int static write_file(void){
       FILE*fp;
       fp = fopen("text.txt","w");
       if(fp==NULL){
           printf("error!");
          return -1;
      }
      fputs("Hello!",fp);
      fclose(fp);
  
      return 0;
  }
  
  int static read_file(void){
      FILE*fp;
      fp = fopen("text.txt","r");
      char buf[1024];
     if(fp==NULL){
         printf("error!");
          return -1;
      }
      memset(buf,0,sizeof(buf));
      fgets(buf,sizeof(buf),fp);
      fclose(fp);
      printf("buf's content is %s",buf);
      return 0;
  }
  
  
  int main(){
      write_file();
      read_file();
  }
