# OfficeMCP

OfficeMCP server is designed for AI to Automate Microsoft Excel Application in Windows OS. Not working on Linux/MacOS.

## Installation
There are two ways or two modes to install OfficeMCP (They also can be used in the same time):

### 1. User OfficeMCP as stdio server: 
- One OfficeMCP server for One MCP Client mode
- Put following setting to MCP.json file for vscode or some proper place for other AI IDE:

```json
{
    "mcpServers": {
        "OfficeMCP": {
            "type": "stdio",
            "command": "uvx",
            "args": [
                "OfficeMCP"
            ]
        }
    }
}
```

### 2. User OfficeMCP as sse server: 
- One OfficeMCP server for multi MCP Client mode
- You can change port and host as you like
#### step 1:  
**Run one command in shell or power shell:**
>uvx OfficeMCP sse

With "url": "http//127.0.0.1:8000/sse"

or
>uvx OfficeMCP sse --port 8009

or
>uvx OfficeMCP sse 8009

or
>uvx OfficeMCP sse --port 8009 --host 127.0.0.1

With "url": "http//127.0.0.1:8009/sse"
#### setp 2: 
**Put following setting to MCP.json file for vscode or some proper place for other AI IDE:**

```json
{
    "servers": {
        "OfficeMCP": {
            "url": "http//127.0.0.1:8009/sse"
        }
    }
}
```
## Usage
OfficeMCP enables AI-driven Excel automation through natural language commands. Example chat-based workflow:

1. **Check Excel Availability**  
   `@OfficeMCP IsAppAvailable {"app_name": "Excel"}`

2. **Launch Excel**  
   `@OfficeMCP Launch {"app_name": "Excel"}`

3. **Make Excel Visible**  
   `@OfficeMCP Visible {"app_name": "Excel", "visible": true}`

4. **Create Workbook**  
   `@OfficeMCP RunPython {"PythonCode": "this.Excel.Workbooks.Add()"}`

5. **Add Sample Data**  
   ```json
   @OfficeMCP RunPython {
     "PythonCode": "this.Excel.ActiveSheet.Range('A1').Value = 'AI Generated Report'"
   }```

## Tools Reference
Core Tools:
- `AvailableApps()`: Checks which Microsoft Office applications are installed
- `IsAppAvailable(app_name: str,visible: bool=true)`: Verifies if a specific Office application is installed
- `Launch(app_name: str)`: Starts an Office application instance
- `Visible(app_name: str, visible: bool)`: Controls application visibility
- `Quit(app_name: str)`: Terminates an Office application
- `RunPython(PythonCode: str)`: Executes Python scripts within Office applications
  - Access application via `this.Excel`, `this.Word`, etc.
- `Demonstrate()`: Shows interactive demo of capabilities

Special Features:
- Supports Excel, Word, PowerPoint, Outlook, Visio, Access, and Project
- Registry-based Office application detection
- COM object management for Office interoperability
- Installed(): chedk if Excel Application is installed on your computer.
- Launch(...): launch a new Excel Application and set it's visibility.
- Visible(): set the current Excel Application's visibility to True or False.
- Quit(): quit the current Excel Application.
- WorkBook(BookPath:=None): create a new Excel WorkBook if BootPath is None or empty and open or save an Excel WorkBook as the BookPath refer to.
- There're some other tools not mentioned here.

- RunPython(...): run python code in the current Excel Application.
    - This is most powerful tool in OfficeMCP server. AI can use this tool to do whatever you want to do in the current Excel Application.
    - There's an Global variable named class instance "The" in the python code, "The.Excel" hold the current Excel Application, 
    - The openpyxl library' workbook is imported in the python code, so you can use openpyxl to manipulate excel files.

- More other tools will be added in the future.


## Development
```bash
git clone https://github.com/officemcp/OfficeMCP
```