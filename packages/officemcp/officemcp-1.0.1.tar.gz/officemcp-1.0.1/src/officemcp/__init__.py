import winreg
import asyncio
import pywintypes
from fastmcp import FastMCP
import os,sys
import win32com.client

mcp = FastMCP("OfficeMCP")

class MyClass:
    def __init__(self):
        self.helloworld = "Hello World"
class Utils:
    def __init__(self):
        self._printable = False
        self._my = MyClass()
    def print(self, obj):
        if self._printable:
            try:              
                print(obj)
            except Exception as e:
                print(e)
    def close_app_by_force(app):
        import win32process
        import win32api
        import win32con
        # Get the window's process id's
        hwnd = app.Hwnd
        t, p = win32process.GetWindowThreadProcessId(hwnd)
        # Ask window nicely to close  
        try:
            handle = win32api.OpenProcess(win32con.PROCESS_TERMINATE, 0, p)
            if handle:
                win32api.TerminateProcess(handle, 0)
                win32api.CloseHandle(handle)
        except:
            pass
class ThisClass:
    def __init__(self):
        self._excel = None
        self._word = None
        self._outlook = None
        self._visio =None
        self._access = None
        self._project = None
        self._publisher = None
        self._onenote = None
        self._powerpoint = None

        self._printable = False
        self._my = MyClass()
        self.MicrosoftApplications=[
        'Word', 'Excel', 'PowerPoint',
        'Visio', 'Access', 'MSProject',
        'Outlook', 'Publisher',"OneNote"
        ]
    def print(self, obj):
        if self._printable:
            try:              
                print(obj)
            except Exception as e:
                print(e)
    @property
    def Excel(self) -> object:
        """Get the Excel application object."""
        try:
            name = self._excel.Name
            return self._excel
        except Exception as e:
            self._excel = self.Application("Excel",False)
        return self._excel

    @property
    def Word(self) -> object:
        """Get the Word application object."""
        try:
            name = self._word.Name
            return self._word
        except Exception as e:
            self._word = self.Application("Word",False)
        return self._word
    
    @property
    def PowerPoint(self) -> object:
        """Get the PowerPoint application object."""
        try:
            name = self._powerpoint.Name
            return self._powerpoint
        except Exception as e:
            self._powerpoint = self.Application("PowerPoint", False)
        return self._powerpoint

    @property
    def Visio(self) -> object:
        """Get the Visio application object."""
        try:
            name = self._visio.Name
            return self._visio
        except Exception as e:
            self._visio = self.Application("Visio", False)
        return self._visio

    @property
    def Access(self) -> object:
        """Get the Access application object."""
        try:
            name = self._access.Name
            return self._access
        except Exception as e:
            self._access = self.Application("Access", False)
        return self._access

    @property
    def Project(self) -> object:
        """Get the Project application object."""
        try:
            name = self._project.Name
            return self._project
        except Exception as e:
            self._project = self.Application("MSProject", False)
        return self._project

    @property
    def Outlook(self) -> object:
        """Get the Outlook application object."""
        try:
            name = self._outlook.Name
            return self._outlook
        except Exception as e:
            self._outlook = self.Application("Outlook", False)
        return self._outlook

    @property
    def Publisher(self) -> object:
        """Get the Publisher application object."""
        try:
            name = self._publisher.Name
            return self._publisher
        except Exception as e:
            self._publisher = self.Application("Publisher", False)
        return self._publisher

    @property
    def OneNote(self) -> object:
        """Get the OneNote application object."""
        try:
            name = self._onenote.Name
            return self._onenote
        except Exception as e:
            self._onenote = self.Application("OneNote", False)
        return self._onenote

    def Visible(self, app_name: str, visible = None) -> bool:
        """Check if the specified application is visible."""
        try:
            app = self.Application(app_name)
            if app is None:
                return False
            else:
                if not visible is None:
                    app.Visible = visible
                return app.Visible
        except Exception as e:
            print(e)
            return False

    def Quit(self,app_name: str)->bool:
        """Quit the microsoft excel application."""
        this.print('Tool.Quit:')
        app_name_attr="_"+app_name.lower()
        if hasattr(self, app_name_attr):
            app = getattr(self, app_name_attr)
            try:
                app.Quit()
                return True
            except Exception as e:
                this.print(e)
        return False

    def Application(self, app_name: str, asNewInstance: bool = False) -> object:  # noqa: E741
        """Get the specified Microsoft Office application object."""
        app_name_attr="_"+app_name.lower()
        if hasattr(self, app_name_attr):
            app = getattr(self, app_name_attr)
            try:
                name = app.Name
                return app
            except Exception as e:
                print(e)
        if not app_name in self.MicrosoftApplications:
            return None
        if not self.IsAppAvailable(app_name):
            return None
        app_full_name = app_name + ".Application"#
        if asNewInstance:
            app = win32com.client.Dispatch(app_full_name)
            self.__dict__[app_name_attr] = app
            return app
        else:
            try:
                app = win32com.client.GetActiveObject(app_full_name)
            except pywintypes.com_error:
                app = win32com.client.Dispatch(app_full_name)
            self.__dict__[app_name_attr] = app
            return app

    def AvailableApps(self) -> list:        
        apps = []
        for prog_id in self.MicrosoftApplications:
            try:
                # Registry verification
                with winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, prog_id+".Application"):
                    pass
                apps.append(prog_id)            
            except (FileNotFoundError, pywintypes.com_error):
                continue
            except Exception as e:
                print(f"[DEBUG] Error verifying {prog_id}: {str(e)}")            
        return apps
    def IsAppAvailable(self,app_name: str) -> bool:
        """Check if the specified application is installed."""
        try:
            if not app_name.endswith(".Application"):
                app_name=app_name+".Application"
            with winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, app_name):
                pass
            return True
        except Exception as e:
            print("e")
            return False

    def Demonstrate(self):
        self.DemonstrateExcel()
        self.DemonstratePowerPoint()
    def DemonstrateExcel(self):
        excel=this.Excel
        if excel is None:
            return []
        book = excel.Workbooks.Add()
        sheet = excel.ActiveSheet
        excel.Visible = True
        sheet.Cells(1, 1).Value = "Hello, World From OfficeMCP Server!"
        sheet.Cells(1, 1).Font.Size = 20
        sheet.Cells(1, 1).Font.Bold = True
        sheet.Cells(2, 1).Value = "This is a demonstration of the OfficeMCP server."
        sheet.Cells(3, 1).Value = "You can use this server's tool to control all Microsoft Office Applications."
        sheet.Cells(4, 1).Value = "RunPython tool to run Python codes to edit Office Application's documents."
        sheet.Cells(4, 1).Font.Color = 0xFF0000  # Red color
        sheet.Cells(5, 1).Value = "AvailableApplications tool to check the Microsoft Office applications installed."
        sheet.Cells(6, 1).Value = "IsAppAvailable tool to check if an specific Microsoft Office application is installed."
        sheet.Cells(7, 1).Value = "Launch tool to Launch an specific Microsoft Office application."
        sheet.Cells(8, 1).Value = "Visible tool to check if an specific Microsoft Office application is visible."
        sheet.Cells(9, 1).Value = "Quit tool to quit an specific Microsoft Office application."        
    def DemonstratePowerPoint(self):
        ppt=this.Application("PowerPoint")
        if ppt is None:
            return []
        ppt.Visible = True
        presentation = ppt.Presentations.Add()
        slide = presentation.Slides.Add(1, 12)
        top = 20
        shape = slide.Shapes.AddTextbox(1, 100, top, 800, 100)
        shape.TextFrame.TextRange.Text = "Hello, World From OfficeMCP Server!"
        #make shape bold
        shape.TextFrame.TextRange.Font.Bold = True
        top += 40
        shape = slide.Shapes.AddTextbox(1, 100, top, 800, 100)
        shape.TextFrame.TextRange.Text = "This is a demonstration of the OfficeMCP server."
        top += 40
        shape = slide.Shapes.AddTextbox(1, 100, top, 800, 100)
        shape.TextFrame.TextRange.Text = "You can use this server's tools to control all Microsoft Office Applications."
        top += 40
        shape = slide.Shapes.AddTextbox(1, 100, top, 800, 100)
        shape.TextFrame.TextRange.Text = "RunPython tool to run Python codes to edit Office Application's documents."
        #make shape red
        shape.TextFrame.TextRange.Font.Color = 0xFF0000
        top += 40
        shape = slide.Shapes.AddTextbox(1, 100, top, 800, 100)
        shape.TextFrame.TextRange.Text = "AvailableApplications tool to check the Microsoft Office applications installed."
        top += 40
        shape = slide.Shapes.AddTextbox(1, 100, top, 800, 100)
        shape.TextFrame.TextRange.Text = "IsAppAvailable tool to check if an specific Microsoft Office application is installed."
        top += 40
        shape = slide.Shapes.AddTextbox(1, 100, top, 800, 100)
        shape.TextFrame.TextRange.Text = "Launch tool to Launch an specific Microsoft Office application."
        top += 40
        shape = slide.Shapes.AddTextbox(1, 100, top, 800, 100)
        shape.TextFrame.TextRange.Text = "Visible tool to check if an specific Microsoft Office application is visible."    
        top += 40
        shape = slide.Shapes.AddTextbox(1, 100, top, 800, 100)
        shape.TextFrame.TextRange.Text = "Quit tool to quit an specific Microsoft Office application."
        top += 40
        shape = slide.Shapes.AddTextbox(1, 100, top, 800, 100)
        shape.TextFrame.TextRange.Text = "Demonstrate tool to see this demonstration."
        top += 40
        shape = slide.Shapes.AddTextbox(1, 100, top, 800, 100)
        shape.TextFrame.TextRange.Text = "Instructions tool to see the instructions of this server."

global this,my
my = MyClass()
this = ThisClass() 
this.my = my

@mcp.tool()
def AvailableApps() -> list:
    """Get Microsoft Office applications availability.      
    """
    print('Tool.Applications:')
    return this.AvailableApps()

@mcp.tool()
def IsAppAvailable(app_name: str) -> bool:
    """Check if the specified application is installed."""
    return this.IsAppAvailable(app_name)

@mcp.tool()
def Visible(app_name: str, visible: bool) -> bool:
    """Check if the microsoft excel application is visible."""
    this.print('Tool.Visible:')
    return this.Visible(app_name,visible)

@mcp.tool()
def Launch(app_name: str, visilbe: bool = True)->bool:
    """Launch an new microsoft excel application or use the existed one."""
    this.print('Tool.Launch:')
    try:
        app = this.Application(app_name)
        app.Visible = visilbe
        return True
    except Exception as e:
        this.print(e)
        return False

@mcp.tool()
def RunPython(PythonCode: str) -> dict:
    """Run Python codes to control office applications.
    Description:
        The MCP tools can also can be used in the Python code.
    Example:
        RunPython('this.Excel.ActiveWorkbook.SaveAs("C:\\Users\\YourName\\Desktop\\test.xlsx")')
        RunPython('this.Excel.ActiveWorkbook.Close()')
      Args:
        PythonCode (str): The Python code to be executed.
    """
    print('Tool.RunPython:')
    try:
        exec(PythonCode, globals())
        return {'success': True, 'output': 'Execution completed'}
    except Exception as e:
        return {'success': False, 'error': str(e)}

@mcp.tool()
def Quit(app_name: str)->bool:
    """Quit the microsoft excel application."""
    print('Tool.Quit:')
    return this.Quit(app_name)

@mcp.tool()
def Demonstrate()->dict:
    """Demonstrate for you to see some functions in this OfficeMCP server."""
    print('Tool.Demonstrate:')
    try:
        this.Demonstrate()    
        return {"success": True, "output": "Demonstration completed"}
    except Exception as e:
        print(e)
        return {"failed": False, "error": str(e)}

@mcp.resource("resource://Instructions")
def Instructions() -> str:
    return """
    There're some base tools for you to control Microsoft applications.
    Specially you can use tool RunPython to run python codes to control Microsoft applications.
    There're an object called "this" as global, it have properties (this.Excel, this.Word, this.Outlook etc.) representing the Microsoft applications.
    """

def main() -> None:
    """OfficeMCP server entry point with command line arguments support.
    
    Usage examples:
    1. OfficeMCP (stdio mode by default)
    2. OfficeMCP sse 8080 127.0.0.1 (SSE mode with port and host)
    3. OfficeMCP sse --port 8080 --host 127.0.0.1 (alternative syntax)
    """
    args = sys.argv[1:]
    transport = "stdio"
    thePort = 8000
    theHost = "127.0.0.1"

    try:
        if args:
            transport = args[0].lower()
            
            # Handle port and host arguments
            if len(args) > 1:
                # Try to parse port from arguments
                for arg in args[1:]:
                    if arg.isdigit():
                        thePort = int(arg)
                        break
                    
                # Try to find host in arguments (first non-port argument)
                for arg in args[1:]:
                    if '--host' in arg:
                        theHost = arg.split('=')[-1]
                    elif not arg.isdigit() and '--port' not in arg:
                        theHost = arg

            # Handle explicit flags (--port/--host)
            if '--port' in args:
                thePort = int(args[args.index('--port') + 1])
            if '--host' in args:
                theHost = args[args.index('--host') + 1]

        if transport == "stdio":
            print("OfficeMCP running in stdio mode")
            mcp.run("stdio")
        else:
            print(f"Starting SSE server on {theHost}:{thePort}")
            mcp.run(transport="sse", host=theHost, port=thePort)

    except ValueError as e:
        print(f"OfficeMCP Error parsing arguments: {e}")
    except Exception as e:
        print(f"OfficeMCP Server startup failed: {e}")
    if transport == "stdio":
        print("OfficeMCP runed on stdio mode")
        mcp.run("stdio")
    else:
        mcp.run(transport="sse", host=theHost, port=thePort)