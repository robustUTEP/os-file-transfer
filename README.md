# nets-tcp-framing

# nets-tcp-file-transfer

For this lab, you must define a file transfer protocol and implement a
client and server.  The server must be * single-threaded, * and accept
multiple concurrent client connections.

Like the demo code provided for this course, your code * should be
structured around a single loop with a single call to select(), * and
all information about protocol state should be explicitly stored in
variables

The following code should be helpful for your project

Directory `simple-echo` includes a simple tcp echo server & client

Directory `forkdemo` includes a simple tcp program with a server that forks

Directory `lib` includes the params package required for many of the programs

Directory `stammer-proxy` includes stammerProxy, which is useful for demonstrating and testing framing

