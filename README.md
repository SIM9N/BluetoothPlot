# SerialPlotTool

## Getting Started

1. Install Python3

3. go to the file directory

4. create a virtual environment<br />
    You can use `anaconda`, but here I am using `virtualenv`<br />
    install `virtualenv`<br />
    mac:`python3 -m pip install --user virtualenv`<br />
    win:`py -m pip install --user virtualenv`<br />
5. Creating a virtual environment
    mac: `python3 -m venv serialPlot`<br />
    win: `py -m venv serialPlot`<br />
    venv will create a virtual Python installation in the `serialPlot` folder.<br />
    if you don't like the name `serialPlot`, change it and also change the `.gitignore` venv file<br />
6. Activating a virtual environment
    mac: `source env/bin/activate`<br />
    win: `.\env\Scripts\activate`<br />
    note: you might want to leave the virtual environment for running other python application, run `deactivate` to leave the current virtual environment<br />
7. Install the required libraries <br />
   mac: `python3 -m pip install pyserial openpyxl matplotlib`<br />
   win: `py -m pip install pyserial openpyxl matplotlib`<br />
   note: run `python3 -m pip freeze` or `py -m pip freeze` to check the list of all installed packages<br />

8. start the app by `python3 ./SerialPlotTool.py` or `py .\SerialPlotTool.py`

## How to use

### connect to a serial port
- connect your device with bluetooth or TTL
- run the app, choose the Port and set the corresponding baudrate
- once successful, the `SerialDataFrame` will show all the data sending from your device 
- note: for new device, you must plugin the device before running the app
### initialize the data to store the data
- the data shown on the `SerialDataFrame` is only for showcast 
- you have to send a cmd to initialize the data identifier in order to store the data and futher use other functions 
- the cmd is "dataName", follow by a "-" and then your first data identifier, end with a new line char "\n" <br />`dataName-[yourDataName1]-[yourDataName2]-...\n`
- once you initialized the data identifier, you can find it in the `GraphContolPanel` ddrop down input box

### save a segment of data to a excel file
- the `export` btn in the `LoggingPanel` will export all the saved data to a excel file under excel folder
- However you can use a `save` and `end` cmd to select a segment of data to export
- all the store data within the `save` and `end` cmd will be exported to a separate sheet named `once `
- you can use the OPEN button to selcet the output excel file
- if you don't select a file manually, a new excel file will be generated
- you can add NOTE to specify the purpose of the record, the note will export together with the data

```=
//pseudo code
while(true){
    if (button1 pressed) then send("dataName-time-x-y\n")

    if (button2 pressed) then send("save\n")

    if (button3 pressed) then send("end\n")

    send(time)
    send(',')
    send(x)
    send(',')
    send(y)
    send("\n")
}
```
