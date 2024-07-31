#!/usr/bin/env python

# name    :  socketserver_simple.py
# version :  0.0.1
# date    :  20240712
# author  :  
# desc    :  

import json
import socketserver
import sqlite3

class Cadet():
    def __init__(self, data):
        self.last_name = data[1]
        self.first_name = data[2]

    def name(self):
        return "{} {}".format(self.first_name, self.last_name)

class RequestHandler(socketserver.BaseRequestHandler):

    def setup(self):
        con = sqlite3.connect("cadets.db")
        self.cur = con.cursor()
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        print("Recieved from {}:".format(self.client_address[0]))
        print(self.data)
        self.request.sendall(self.get_response(self.data))

    def build_data(self, data, result):
        """ Take a dict for data and add the result to it with the index
            as the dict key.
            Sample result:
              (123, 'Domici', 'Alba', None, 'f', 1416146, 22, 9, 'Trail Rat')
        """
        new_data = {
            "idx":          result[0],
            "last_name":    result[1],
            "first_name":   result[2],
            "middle_name":  result[3],
            "gender":       result[4],
            "birthdate":    result[5],
            "plot":         result[6],
            "temperament":  result[7],
            "notes":        result[8],
            }
        data[new_data["idx"]] = new_data
        return data

    def search_values(self, terms = [], data = ()):
        """ Return True if string of all search terms are in data values, else False.
            'data' is a tuple from a Sqlite3 fetchall().

        >>> search_values(["Lefron"], (1429, "Lefron"))
        True

        >>> search_values(["lefron"], (1429, "Lefron"))
        True

        >>> search_values(["lef"], (1429, "Lefron"))
        True

        >>> search_values(["left"], (1429, "Lefron"))
        False

        >>> search_values(["lef", "al"], (1429, "Lefron"))
        False

        >>> search_values([1], (1429, "Lefron"))
        True

        >>> search_values([], (1429, "Lefron"))
        True

        >>> search_values(["lef", "al"], ())
        False
        """
        if len(terms) == 0:
            return True
        if len(data) == 0:
            return False

        for term in terms:
            term_result = False
            for dat in data:
                if str(term).lower() in str(dat).lower():
                    term_result = True
            if term_result == False:
                return False

        return True

    def get_response(self, key):
        return_data = dict()
        search_key = key.decode()
        # res = self.cur.execute("Select * from people where first_name = ?", (search_key,))
        res = self.cur.execute("Select * from people")
        results = res.fetchall()

        # result = res.fetchone()
        print("results are: ", results)
        for result in results:
            if self.search_values([search_key], result):
                return_data = self.build_data(return_data, result)

        # cadet = Cadet(result)
        # print("cadet is: ", cadet.name())
        #return str.encode(cadet.name())
        #return str.encode(search_key)
        #return str.encode(search_key)
        return_data_str = json.dumps(return_data)
        return str.encode(return_data_str)


if __name__ == "__main__":
    HOST, PORT = "localhost", 8080
    
    with socketserver.TCPServer((HOST, PORT), RequestHandler) as server:
        server.serve_forever()


