import asyncio
import sys

CTRL_C = b'\xff\xf4\xff\xfd\x06'
CTRL_D = b'\x04'
CRTL_BACKSLASH = b'\xff\xf3\xff\xfd\x06'

async def main(reader, writer):
    async def write(line):
        writer.write(line)
        await writer.drain()

    async def write_line(line):
        writer.write(line)
        writer.write(b'\n')
        await writer.drain()

    await write(b'\x1b[2J\x1b[H')
    await write_line(b'Ahoy, I am Ondrej Sika and this is my telnet website')
    await write_line(b'           ===========')
    await write_line(b'')
    await write_line(b'What do you looking for? (If you need help, use command `help`)')
    await write_line(b'')

    async def write_help():
        await write_line(b'aboutme')
        await write_line(b'contact')
        await write_line(b'exit')
        await write_line(b'')

    async def write_aboutme():
        await write_line(b'I am visionary, entrepreneur, scout, libertarian, ...')
        await write_line(b'I work as software engineer at Slush Pool (Bitcoin mining).')
        await write_line(b'I also do freelance consulting, eg.: Docker, Git, Continues Integration.')
        await write_line(b'I like freedom, nature, mountines, travelling, people, ... and command line.')
        await write_line(b'')

    async def write_contact():
        await write_line(b'email: ondrej@ondrejsika.com')
        await write_line(b'phone: +420 773 452 376 (also Telegram)')
        await write_line(b'')

    async def exit_website():
        await write_line(b'Bye!')
        await write_line(b'')
        writer.close()

    while True:
        await write(b'$ ')
        data = (await reader.read(100)).replace(b'\r\n', b'')
        addr = writer.get_extra_info('peername')
        print(addr, data)
        sys.stdout.flush()
        if data in (b'exit', ):
            await exit_website()
            break
        if data in (CTRL_D, CTRL_C, CRTL_BACKSLASH):
            await write_line(b'')
            await exit_website()
            break
        elif data == b'help':
            await write_help()
        elif data == b'aboutme':
            await write_aboutme()
        elif data == b'contact':
            await write_contact()
        else:
            await write_line(b'Command not found, use command `help` for available commands')
            await write_line(b'')


loop = asyncio.get_event_loop()
coro = asyncio.start_server(main, '0.0.0.0', 2323, loop=loop)
server = loop.run_until_complete(coro)

print('Serving on {}'.format(server.sockets[0].getsockname()))
sys.stdout.flush()
try:
    loop.run_forever()
except KeyboardInterrupt:
    pass

# Close the server
server.close()
loop.run_until_complete(server.wait_closed())
loop.close()

