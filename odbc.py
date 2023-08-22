import asyncio
import pyodbc
import os,sys
import json
from decimal import Decimal

class ODBCServerProtocol:
    def __init__(self):
        self.cursor = None
        cnstr = os.getenv("CONNSTR")
        if not cnstr:
            print("CONNSTR not defined in env")
            exit()

        self.cnxn = pyodbc.connect(cnstr)
        self.cursor = self.cnxn.cursor()

    def __del__(self):
        if self.cursor:
            self.cursor.close()
        if self.cnxn:
            self.cnxn.close()

    def execute(self,sql):
        if self.cursor:
            self.cursor.execute(sql)
            return self.cursor.fetchall()
    
    def connection_made(self, transport):
        print("UDP connection OK")
        self.transport = transport

    def datagram_received(self, data, addr):
        message = data.decode()
        json_data = json.loads(message)
        sql = json_data["SQL"]
        print(sql)
        fetch_data = self.execute(sql)
        print(fetch_data)
        # convert reslut row to list
        result = []
        for row in fetch_data:
            list = []
            for field in row:
                # convert decimal to string
                if field and isinstance(field,Decimal):
                    list.append(str(field))
                else:
                    list.append(field)
            result.append(list)
        
        data=json.dumps(result)
        self.transport.sendto(data.encode(), addr)

async def main():
    print("Starting UDP server")
    loop = asyncio.get_running_loop()
    transport, protocol = await loop.create_datagram_endpoint(
        lambda: ODBCServerProtocol(),
        local_addr=('127.0.0.1', 9999))
        
    try:
        await asyncio.sleep(sys.maxsize)
    finally:
        transport.close()


if __name__ == '__main__':    
    asyncio.run(main())
