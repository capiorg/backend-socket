# from misc import sio
#
#
# @sio.on('broadcast_message')
# async def test_broadcast_message(sid, data):
#     async with sio.session(sid) as session:
#         print(session['username'])
#
#     sio.enter_room(sid, "foo")
#     await sio.emit("broadcast_message_response", {"foo": "bar"}, room="foo")
#     await sio.disconnect()
#
#
# @sio.on("connect")
# async def connect(sid, environ, auth):
#     await sio.save_session(sid, {'username': auth})
#     await sio.emit("connected", {"result": True})
#
#
# @sio.on("disconnect")
# async def disconnect(sid):
#     print('disconnect ', sid)
#
#
