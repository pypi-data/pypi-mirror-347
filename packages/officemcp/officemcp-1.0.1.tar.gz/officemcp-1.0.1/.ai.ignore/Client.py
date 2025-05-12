# Test all OfficeMCP tools
import src.officemcp as OfficeMCP

print("=== OfficeMCP Comprehensive Testing ===")

try:
    # Test application lifecycle tools
    print("[3/5] Testing AvailableApplications...")
    apps = OfficeMCP.AvailableApps()
    print(f"Installed apps: {', '.join(apps)}")

    print("[4/6] Testing IsAppAvailable...")
    assert OfficeMCP.IsAppAvailable("Excel"), "Excel should be available"
    assert not OfficeMCP.IsAppAvailable("FakeApp"), "FakeApp should not be available"

    print("\n[1/5] Testing Launch...")
    assert OfficeMCP.Launch("Excel"), "Failed to launch Excel"
    
    print("[2/5] Testing Visible...")
    assert OfficeMCP.Visible("Excel", True), "Failed to make Excel visible"   

    print("[4/5] Testing Quit...")
    assert OfficeMCP.Quit("Excel"), "Failed to quit Excel"   
    
    print("[5/5] Testing RunPython...")
    python_code = '''
this.Excel.Visible = True
this.Excel.Workbooks.Add()
this.Excel.ActiveSheet.Cells(1,1).Value = "Test RunPython Tool Successful"
'''
    result = OfficeMCP.RunPython(python_code)
    assert result['success'], f"Python execution failed: {result.get('error', '')}"

    print("[7/7] Testing Demonstrate...")
    OfficeMCP.Demonstrate()

    print("\nAll non-demonstration tests completed successfully!")

except Exception as e:
    print(f"\nTest failed: {str(e)}")

