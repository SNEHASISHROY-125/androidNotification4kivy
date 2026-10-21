import asyncio
import os , json
import struct , datetime ,uuid

# ROOT_DIR = "./"
CHUNK = 64 * 1024  # 64KB

async def read_exact(reader, n):
    data = b""
    while len(data) < n:
        chunk = await reader.read(n - len(data))
        if not chunk:
            raise ConnectionError("Client disconnected")
        data += chunk
    return data


async def read_message(reader):
    header = await read_exact(reader, 4)
    (length,) = struct.unpack("!I", header)
    return await read_exact(reader, length)


async def send_message(writer, data: bytes):
    writer.write(struct.pack("!I", len(data)) + data)
    await writer.drain()

def get_tree(path:str):
    '''
    'root/player/d12032026/fun.gif'\n
    (['root', 'player', 'd12032026'], 'fun.gif')
    '''
    _  = path.split('/')
    return (_[:-1] , _[-1],) if len(_) > 1 else ("." , _[-1],)

global jobs
jobs = {}

class Job:
    '''
    CROSS THREAD JOB HANDLER
    '''
    job_id = None
    job = None
    ''' job callback '''
    timeout = 100   # ~1 sec

    def __init__(self):
        pass

    def create_job(self):
        ## create job-id
        self.job_id = str(uuid.uuid4())
        ## creatte job
        self.job = self.job_handler(self.job_id)

    async def run_till_complete(self):
        ''' wait till a results are passed or timeout & return result'''
        ## loop till either times-out || value gets returned
        global jobs
        for _ in range(self.timeout):
            result = jobs.get(self.job_id)
            if result: jobs.__delitem__(self.job_id) ; break
            await asyncio.sleep(0.01)
        # print("got duration: ", duration)
        return result

    def job_handler(self, id, register=jobs, val=None): return lambda v , i=id, r=register: r.setdefault(i , v)

global _methods

async def handle_client(reader, writer):
    addr = writer.get_extra_info("peername")
    print(f"[+] Connected: {addr}")
    global _methods
    global jobs

    try:
        while True:
            msg = await read_message(reader)
            # parts = msg.split()
            p = dict(json.loads(msg))
            # debug
            print(p)

            match p["comm"]:
                # ---------------- Player Controls ----------------
                case "/show_parcel":
                    # _ , filter_id = parts
                    # print(parts,headers.encode())
                    # _methods.get('setSource')(url , json.loads(headers.encode()) , True if prepare == "true" else False)
                    _methods.get("show_parcel_notification")()
                    await send_message(writer, b"ok")

                case "/show_profile":
                    # _ , scale_w , scale_h = parts
                    # print(parts,headers.encode())
                    # _methods.get('setSource')(url , json.loads(headers.encode()) , True if prepare == "true" else False)
                    _methods.get("show_social_profile")()
                    await send_message(writer, b"ok")

                case "/show_up_down":
                    # _ , camid = parts
                    _methods.get("show_up_down_speed")()
                    await send_message(writer, b"ok")

                case "/notify":
                    # debug
                    print("json: ",p)
                    kwargs = p.get("data")
                    nid = _methods.get('notify_base')(**kwargs) if kwargs else 0
                    await send_message(writer , f"nid: {nid}".encode())
                # case "/switch_cam_t":
                #     _ , camid , c , angle = parts
                #     _methods.get("switch_cam_t")(str(camid), c , float(angle))
                #     await send_message(writer, b"ok")

                # case "/set_upload_url":
                #     _ , url = parts
                #     _methods.get("set_upload_url")(url)
                #     await send_message(writer , b'ok')

                # case "/set_rtsp_url":
                #     _ , url = parts
                #     _methods.get("set_rtsp_url")(url)
                #     await send_message(writer , b'ok')

                # case "/capture_jpeg":
                #     _methods.get("capture_jpeg")()
                #     await send_message(writer , b'ok')

                # case "/start_video":
                #     _methods.get("start_video")()
                #     await send_message(writer , b'ok')

                # case "/stop_video": 
                #     _methods.get("stop_video")()
                #     await send_message(writer , b'ok')

                case _:
                    await send_message(writer, b"error:unknown_command")

    except Exception as e:
        print(f"[!] {addr} error:", e)

    finally:
        writer.close()
        await writer.wait_closed()
        print(f"[-] Disconnected: {addr}")

from threading import Thread

TCP_PORT = 29763

def start_tcp_server(_ethods):
    '''
    Runs in a Thread.
    '''
    def run(_ethods):
        async def main(ethods):
            global _methods
            _methods = dict(ethods)
            print(_methods)
            server = await asyncio.start_server(handle_client, "0.0.0.0", TCP_PORT)
            async with server:
                print("🚀 TCP server running on : ", TCP_PORT)
                await server.serve_forever()

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(main(_ethods))
        except KeyboardInterrupt:
            pass
        finally:
            print("lOOP CLOSING...")
            loop.close()

    server_thread = Thread(target=run, args=(_ethods,),daemon=True)
    # Start server in a daemon thread
    server_thread.start()

# start_tcp_server({})

# import time
# while True: time.sleep(1.5) 