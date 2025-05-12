# coding=utf-8
import asyncio
import sys
import io
import json
from fastmcp import Client
from fastmcp.client.transports import SSETransport

# Set output encoding to UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Service configuration
sse_url = "http://localhost:8000/sse"
client = Client(SSETransport(url=sse_url))

async def test_tools():
    async with client:
        print("=== OfficeMCP SSE Comprehensive Testing ===")
        tools = await client.list_tools()
        print("\nAvailable Tools:")
        for tool in tools:
            print(f"- {tool}")
        try:
            # Test application lifecycle tools
            print("[3/5] Testing AvailableApps...")
            apps = await client.call_tool("AvailableApps")
            print(f"Installed applications: {', '.join(app.text for app in apps)}")

            print("[4/6] Testing IsAppAvailable...")
            assert await client.call_tool("IsAppAvailable", {"app_name": "Excel"}), "Excel should be available"
            if not client.call_tool("IsAppAvailable", {"app_name": "FakeApp"}):
                print("FakeApp should not be available")

            print("\n[1/5] Testing Launch...")
            assert await client.call_tool("Launch", {"app_name": "Excel"}), "Failed to launch Excel"
            
            print("[2/5] Testing Visible...")
            assert await client.call_tool("Visible", {"app_name": "Excel", "visible": True}), "Failed to make Excel visible"

            print("[6/6] Testing Quit...")
            assert await client.call_tool("Quit", {"app_name": "Excel"}), "Failed to quit Excel"

            print("[5/5] Testing RunPython...")
            python_code = '''
this.Excel.Visible = True
this.Excel.Workbooks.Add()
this.Excel.ActiveSheet.Cells(1,1).Value = "Test RunPython Tool Successful"
'''
            result = await client.call_tool("RunPython", {"PythonCode": python_code})
            result = json.loads(result[0].text)
            if result.get('success'):  # Check if success field exists
                print("Python execution successful")
            else:
                print(f"Python execution failed: {result.get('error', 'Unknown error')}")

            print("[7/7] Testing Demonstrate...")
            await client.call_tool("Demonstrate")

            print("\nAll non-demonstration tests completed successfully!")

        except Exception as e:
            print(f"\nTest failed: {str(e)}")

if __name__ == "__main__":
    asyncio.run(test_tools())