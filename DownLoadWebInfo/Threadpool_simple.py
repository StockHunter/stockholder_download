import threadpool

class ThreadPool:
    """A thread pool, distributing work requests and collecting results.

    See the module docstring for more information.

    """

    def __init__(self, num_workers, q_size=0, resq_size=0, poll_timeout=5):
        pass

    def createWorkers(self, num_workers, poll_timeout=5):
        pass

    def dismissWorkers(self, num_workers, do_join=False):
        pass

    def joinAllDismissedWorkers(self):
        pass

    def putRequest(self, request, block=True, timeout=None):
        pass

    def poll(self, block=False):
        pass

    def wait(self):
        pass

def ThreadFun(arg1,arg2):
    pass
def main():
    device_list=[object1,object2,object3,objectn]#需要处理的设备个数
    task_pool=threadpool.ThreadPool(8)#8是线程池中线程的个数
    request_list=[]#存放任务列表
    #首先构造任务列表
    for device in device_list:
        request_list.append(threadpool.makeRequests(ThreadFun,[((device, ), {})]))
    #将每个任务放到线程池中，等待线程池中线程各自读取任务，然后进行处理，使用了map函数，不了解的可以去了解一下。
    map(task_pool.putRequest,request_list)
    #等待所有任务处理完成，则返回，如果没有处理完，则一直阻塞
    task_pool.poll()
if __name__=="__main__":
    main()