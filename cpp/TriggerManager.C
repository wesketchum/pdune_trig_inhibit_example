#include "zmq.h"
#include "string.h"
#include <sys/time.h>
#include <unistd.h>

int main(){

  //  Prepare our context and publisher
  void *context = zmq_ctx_new ();
  void *subscriber = zmq_socket (context, ZMQ_SUB);
  int rc = zmq_connect (subscriber, "tcp://localhost:5566");
  
  char *filter = "IM-GLOBAL";
  const int hwm=1;
  rc = zmq_setsockopt (subscriber, ZMQ_SUBSCRIBE,
		       filter, strlen (filter));
  rc = zmq_setsockopt(subscriber,ZMQ_RCVHWM,&hwm,sizeof(int));

  printf("Everything is set up...\n");
  
  //  Process 100 updates
  int update_nbr;
  struct timeval timenow;
  char recv_buf[256];

  for (update_nbr = 0; update_nbr < 100; update_nbr++) {
    printf("Waiting for message...\n");
    int msg_size = zmq_recv(subscriber,recv_buf,256,ZMQ_DONTWAIT);
    gettimeofday(&timenow,NULL);

    if(msg_size<0){
      printf("Msg size was less than zero.\n");
      usleep(100000);
    }
    else
      printf("%s received at %ld seconds and %u microseconds\n",recv_buf,timenow.tv_sec,timenow.tv_usec);    
  }

  zmq_close (subscriber);
  zmq_ctx_destroy (context);
  return 0;
     
}
