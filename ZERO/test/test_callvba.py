import win32com.client as client

filename = r"C:\Users\qhj01\Desktop\美化.xlsm"

xlapp = client.Dispatch('Excel.Application')
xlapp.visible = 1
try:
    book1 = xlapp.Workbooks.Open(filename)

    xlapp.Application.Run("美化.xlsm!beautify")
    print('执行完毕')
except:
    pass
finally:
    xlapp.DisplayAlerts = 0
    book1.Close()
    xlapp.DisplayAlerts = 1
    xlapp.Application.Quit()