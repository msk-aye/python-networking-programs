import signal
import subprocess
import time
import re
import random

"""
Please run this test in a linux environment and place this test file in the same directory with your code. 
This test will test the output format for each of the server and client. Please feel free to post on Ed discussions 
if you think there is any issue in the test cases. 

This test uses the newest version of the code templates, which changes the behaviour of the raw clients and servers. 
All raw clients and servers are required to run with a port number as a command-line argument. So please replace the 
raw_server_tcp.py and raw_server_udp.py with the newest version, and copy paste the read_port_number() function from 
previous clients or servers (e.g., echo_client.py) to raw_client_tcp.py and raw_client_udp.py with some minor 
modifications
"""


class Testcases:
    def __init__(self):
        # use \n to represent the action of hitting enter
        self.echo_client_inputs = ["Test 1\n", "123\n", "Hello\nWorld\n"]
        self.echo_client_expected_outputs = [
            "[Server] Test 1", "[Server] 123", "[Server] Hello", "[Server] World"]

        self.number_client_inputs = ["0\n", "1\n", "2\n", "3\n", "4\n", "5\n", "6\n", "7\n", "8\n", "9\n",
                                     "10\n", "Test\n", "123\n"]
        self.number_client_expected_outputs = ["[Server] zero", "[Server] one", "[Server] two", "[Server] three",
                                               "[Server] four", "[Server] five", "[Server] six", "[Server] seven",
                                               "[Server] eight", "[Server] nine", "[Server] Invalid message",
                                               "[Server] Invalid message", "[Server] Invalid message"]

        self.chat_client_inputs1 = ["Hello World\n"]
        self.chat_server_inputs1 = ["Hi\n"]
        self.chat_client_expected_outputs1 = [r"\[Server \((\d{2}:\d{2}:\d{2})\)\] Welcome to the channel, Alice",
                                              r"\[Server \((\d{2}:\d{2}:\d{2})\)\] Hi",
                                              "[Connection terminated by the client]"]

        self.chat_server_expected_outputs1 = [r"\[\((\d{2}:\d{2}:\d{2})\)\] Waiting for a connection",
                                              r"\[\((\d{2}:\d{2}:\d{2})\)\] Get a connection from Alice",
                                              r"\[Alice \((\d{2}:\d{2}:\d{2})\)\] Hello World",
                                              "[Connection terminated by the client]"]

        self.chat_client_inputs2 = ["Hello I am Bob.\n", "How are you?\n"]
        self.chat_server_inputs2 = ["Hi Bob, Nice to meet you!\n", "Bye\n"]
        self.chat_client_expected_outputs2 = [r"\[Server \((\d{2}:\d{2}:\d{2})\)\] Welcome to the channel, Bob",
                                              r"\[Server \((\d{2}:\d{2}:\d{2})\)\] Hi Bob, Nice to meet you!",
                                              r"\[Server \((\d{2}:\d{2}:\d{2})\)\] Bye",
                                              "[Connection terminated by the server]"]

        self.chat_server_expected_outputs2 = [r"\[\((\d{2}:\d{2}:\d{2})\)\] Waiting for a connection",
                                              r"\[\((\d{2}:\d{2}:\d{2})\)\] Get a connection from Bob",
                                              r"\[Bob \((\d{2}:\d{2}:\d{2})\)\] Hello I am Bob.",
                                              r"\[Bob \((\d{2}:\d{2}:\d{2})\)\] How are you?",
                                              "[Connection terminated by the server]"]

        self.raw_client_tcp_inputs = ["Testtest\n"]
        self.raw_server_tcp_expected_outputs = ["Waiting for connection.", "Connected by ('127.0.0.1', 12345)",
                                                "Testtest"]

        self.raw_client_udp_inputs = ["Testtest\n", "123\n", "Hello\nWorld\n"]
        self.raw_server_udp_expected_outputs = [
            "Testtest", "123", "Hello", "World"]

        # place to store client and server outputs
        self.client_outputs = None
        self.server_outputs = None

    def run_subprocess(self, server_path, client_path, port_number=None, server_inputs=None, client_inputs=None,
                       client_name=None, exit_by=None):

        # Start server
        server_process = subprocess.Popen(['python3', server_path, port_number],
                                          stdin=subprocess.PIPE,
                                          stdout=subprocess.PIPE,
                                          stderr=subprocess.PIPE)
        time.sleep(1)  # Wait for server to start

        # Start client
        if client_name:     # start chat_client.py
            client_process = subprocess.Popen(['python3', client_path, port_number, client_name],
                                              stdin=subprocess.PIPE,  # Redirect stdin
                                              stdout=subprocess.PIPE,
                                              stderr=subprocess.PIPE)
        else:
            client_process = subprocess.Popen(['python3', client_path, port_number],
                                              stdin=subprocess.PIPE,  # Redirect stdin
                                              stdout=subprocess.PIPE,
                                              stderr=subprocess.PIPE)

        time.sleep(1)   # Wait for client to start

        # Send messages to client's stdin
        for client_input in client_inputs:
            client_process.stdin.write(client_input.encode())
            client_process.stdin.flush()  # Flush stdin stream
            time.sleep(0.5)

        # Send messages to server's stdin
        if server_inputs:
            for server_input in server_inputs:
                server_process.stdin.write(server_input.encode())
                server_process.stdin.flush()  # Flush stdin stream
                time.sleep(0.5)

        # Send exit message for chat client and chat server
        if exit_by is not None:
            if exit_by == "client":
                client_process.stdin.write("exit\n".encode())
                client_process.stdin.flush()

            elif exit_by == "server":
                server_process.stdin.write("exit\n".encode())
                server_process.stdin.flush()

        time.sleep(1)
        client_process.send_signal(signal.SIGINT)
        server_process.send_signal(signal.SIGINT)
        time.sleep(1)

        # Terminate the client process
        client_process.terminate()

        # Capture and print client output
        client_outputs, client_error = client_process.communicate(timeout=200)

        # Check client output
        self.client_outputs = client_outputs.decode().strip()
        print("client_outputs:\n" + self.client_outputs)

        # Terminate the server process
        server_process.terminate()

        # Capture and print server output
        server_outputs, server_error = server_process.communicate(timeout=200)

        self.server_outputs = server_outputs.decode().strip()
        print()     # separate client_outputs and server_outputs
        print("server_outputs:\n" + self.server_outputs)
        time.sleep(1)

    def test_echo_server_client(self):
        print("-" * 40)
        try:
            random_port = str(random.randint(1023, 65535))
            # Start echo server in a subprocess
            self.run_subprocess("echo_server.py", "echo_client.py", port_number=random_port,
                                client_inputs=self.echo_client_inputs)

            assert all(output in self.client_outputs for output in self.echo_client_expected_outputs), \
                "Client outputs do not match"

            self.client_outputs = self.client_outputs.split("\n")
            assert len(
                self.client_outputs) == 4, "Incorrect number of client outputs"
            self.server_outputs = self.server_outputs.split("\n")
            print("len_server_outputs:", len(self.server_outputs))
            assert len(
                self.server_outputs) == 1 and self.server_outputs[0] == '', "Incorrect number of server outputs"

        except Exception as e:
            print("Echo test failed:", e)
        else:
            print("Echo test passed.")

    def test_number_server_client(self):
        print("-" * 40)
        try:
            random_port = str(random.randint(1023, 65535))
            self.run_subprocess("number_server.py", "number_client.py", port_number=random_port,
                                client_inputs=self.number_client_inputs)

            assert all(output in self.client_outputs for output in self.number_client_expected_outputs), \
                "Client outputs do not match"

            self.client_outputs = self.client_outputs.split("\n")
            assert len(
                self.client_outputs) == 13, "Incorrect number of client outputs"
            self.server_outputs = self.server_outputs.split("\n")
            assert len(
                self.server_outputs) == 1 and self.server_outputs[0] == '', "Incorrect number of server outputs"

        except Exception as e:
            print("Number test failed:", e)
        else:
            print("Number test passed.")

    def test_chat_server_client(self):
        print("-" * 40)
        try:
            # run chat_server.py and chat_client.py test 1
            random_port = str(random.randint(1023, 65535))
            self.run_subprocess("chat_server.py", "chat_client.py", port_number=random_port,
                                client_name="Alice", server_inputs=self.chat_server_inputs1,
                                client_inputs=self.chat_client_inputs1, exit_by="client")

            # use \r\n under windows machine
            # server_outputs = self.server_outputs.split("\r\n")

            # use \n under linux machine
            server_outputs = self.server_outputs.split("\n")

            assert re.match(
                self.chat_server_expected_outputs1[0], server_outputs[0]), "Server outputs 0 do not match"
            assert re.match(
                self.chat_server_expected_outputs1[1], server_outputs[1]), "Server outputs 1 do not match"
            assert re.match(
                self.chat_server_expected_outputs1[2], server_outputs[2]), "Server outputs 2 do not match"
            assert self.chat_server_expected_outputs1[3] == server_outputs[3], "Server outputs 3 do not match"
            assert len(
                server_outputs) == 4, "Incorrect number of server outputs"

            client_outputs = self.client_outputs.split("\n")
            assert re.match(
                self.chat_client_expected_outputs1[0], client_outputs[0]), "Client output 0 does not match"
            assert re.match(
                self.chat_client_expected_outputs1[1], client_outputs[1]), "Client output 1 does not match"
            assert self.chat_client_expected_outputs1[2] == client_outputs[2], "Client output 2 does not match"
            assert len(
                client_outputs) == 3, "Incorrect number of client outputs"

        except Exception as e:
            print("Chat test 1 failed:", e)
        else:
            print("Chat test 1 passed.")

        print("-" * 40)
        try:
            # run chat_server.py and chat_client.py test 2
            random_port = str(random.randint(1023, 65535))
            self.run_subprocess("chat_server.py", "chat_client.py", port_number=random_port,
                                client_name="Bob", server_inputs=self.chat_server_inputs2,
                                client_inputs=self.chat_client_inputs2, exit_by="server")

            # use \r\n under windows machine
            # server_outputs = self.server_outputs.split("\r\n")

            # use \n under linux machine
            server_outputs = self.server_outputs.split("\n")

            assert re.match(
                self.chat_server_expected_outputs2[0], server_outputs[0]), "Server output 0 does not match"
            assert re.match(
                self.chat_server_expected_outputs2[1], server_outputs[1]), "Server output 1 does not match"
            assert re.match(
                self.chat_server_expected_outputs2[2], server_outputs[2]), "Server output 2 does not match"
            assert re.match(
                self.chat_server_expected_outputs2[3], server_outputs[3]), "Server output 3 does not match"
            assert self.chat_server_expected_outputs2[4] == server_outputs[4], "Server output 4 does not match"
            assert len(
                server_outputs) == 5, "Incorrect number of server outputs"

            client_outputs = self.client_outputs.split("\n")
            assert re.match(
                self.chat_client_expected_outputs2[0], client_outputs[0]), "Client output 0 does not match"
            assert re.match(
                self.chat_client_expected_outputs2[1], client_outputs[1]), "Client output 1 does not match"
            assert re.match(
                self.chat_client_expected_outputs2[2], client_outputs[2]), "Client output 2 does not match"
            assert self.chat_client_expected_outputs2[3] == client_outputs[3], "Client output 3 does not match"
            assert len(
                client_outputs) == 4, "Incorrect number of client outputs"

        except Exception as e:
            print("Chat test 2 failed:", e)
        else:
            print("Chat test 2 passed.")

    def test_raw_tcp(self):
        print("-" * 40)
        random_port = str(random.randint(1023, 65535))
        try:
            self.run_subprocess("raw_server_tcp.py", "raw_client_tcp.py", port_number=random_port,
                                client_inputs=self.raw_client_tcp_inputs)

            assert all(output in self.server_outputs for output in self.raw_server_tcp_expected_outputs), \
                "Server outputs do not match"

            self.server_outputs = self.server_outputs.split("\n")
            assert len(
                self.server_outputs) == 3, "Incorrect number of server outputs"
            self.client_outputs = self.client_outputs.split("\n")
            assert len(self.client_outputs) == 1 and self.client_outputs[0] == "The chat message to send:", \
                "Incorrect number of client outputs"

        except Exception as e:
            print("raw tcp test failed:", e)
        else:
            print("raw tcp test passed.")

    def test_raw_udp(self):
        print("-" * 40)
        random_port = str(random.randint(1023, 65535))
        try:
            self.run_subprocess("raw_server_udp.py", "raw_client_udp.py", port_number=random_port,
                                client_inputs=self.raw_client_udp_inputs)

            assert all(output in self.server_outputs for output in self.raw_server_udp_expected_outputs), \
                "Server outputs do not match"

            self.server_outputs = self.server_outputs.split("\n")
            assert len(
                self.server_outputs) == 4, "Incorrect number of server outputs"
            self.client_outputs = self.client_outputs.split("\n")
            assert len(
                self.client_outputs) == 1 and self.client_outputs[0] == '', "Incorrect number of client outputs"

        except Exception as e:
            print("raw udp test failed:", e)
        else:
            print("raw udp test passed.")

    def run_all_tests(self):
        #self.test_echo_server_client()
        #self.test_number_server_client()
        self.test_chat_server_client()
        #self.test_raw_tcp()
        #self.test_raw_udp()


if __name__ == "__main__":
    testcases = Testcases()
    testcases.run_all_tests()
