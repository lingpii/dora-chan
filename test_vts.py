import pyvts 
import asyncio

async def main(): 
    vts = pyvts.vts(plugin_info={
        "plugin_name": "Dora-chan",
        "developer": "Chi",
        "authentication_token_path": "./token.txt"
    })

    await vts.connect()
    await vts.request_authenticate_token()
    await vts.request_authenticate()

    response = await vts.request(vts.vts_request.requestHotKeyList())
    print(response)
    await vts.close()

asyncio.run(main())

