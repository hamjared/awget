# Anonymous wget

Anonymous wget downloads webpages much like the normal wget, but conceals the end downloaders IP address by sending the 
download request through multiple hosts before downloading the file. Once the file is downloaded the chain
of hosts is then unraveled by sending the file contents to the previous stepping stone until it reaches the end user. All connections and 
data related to the file being downloaded is removed from each stepping stone. 

My version of wget is functioning properly in python3 as long as the stepping stone servers are running on linux machines with wget installed and callable from the command line from any directory. The stepping stone server will not run on a windows machine 
due to a system call to wget which windows does not have

## To run the Stepping Stone Servers
- It is compatible with Python3 only. When run, it will print the ip addresses returned by the python function gethostbyname
- If no port number is passed to the program the default port is 6324

```
$ python3 ss.py [-p PORT]

$ python3 ss.py -p 8000
['127.0.1.1', '192.168.1.101']
Socket listening on  ['127.0.1.1', '192.168.1.101'] port:  8000

```

## To Run awget
- awget can be run using python3 only from linux or windows. 
- You must pass the url of the file you would like to download
- You can optionally pass a chain file formatted as shown in chain file section of this document. If not chain file is passed it, the program will use its default chain file
- Before running awget, run stepping stone servers on each host defined in your chain file

```
$ python3 awget.py <URL> [-c chainfile] 
```

## Chain files

The format of a chainfile should be as follows:

```
<SSnum>
<SSaddr, SSport>
<SSaddr, SSport>
<SSaddr, SSport>
...
```

An example chain file is listed below:
```
4
129.82.45.59 20000
129.82.47.209 25000
129.82.47.223 30000
129.82.47.243 35000
```
