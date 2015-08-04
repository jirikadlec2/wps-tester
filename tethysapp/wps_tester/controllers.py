from django.shortcuts import render
from owslib.wps import monitorExecution
from tethys_gizmos.gizmo_options import TextInput
from tethys_apps.sdk import list_wps_service_engines

def home(request):
    """
    Controller for the app home page.
    """

    if request.POST and 'inputURL' in request.POST:
        display_url = request.POST['inputURL']

        my_url = display_url.replace('=', '!')
        my_url = my_url.replace('&', '~')

        wps_outputs = run_wps(str(my_url))
        context = {'final_output': wps_outputs }

    else:
        display_url = "http://hydrodata.info/chmi-h/cuahsi_1_1.asmx/GetValuesObject?location=CHMI-H:140&variable=CHMI-H:TEPLOTA&startDate=2015-06-01&endDate=2015-08-03&authToken="
        my_url = display_url.replace("=", "!")
        my_url = my_url.replace("&", "~")
        context = {'final_output': ''}

    text_input_options = TextInput(display_text='Time Series URL',
                       name='inputURL',
                                   initial=display_url)


    context['text_input_options'] = text_input_options
    return render(request, 'wps_tester/home.html', context)


#test the controller approaching the WPS
def run_wps(timeseries_url):

    wps_engines = list_wps_service_engines()
    my_engine = wps_engines[0]

    #choose the r.time-series-converter
    process_id = 'org.n52.wps.server.r.time-series-converter'
    my_process = my_engine.describeprocess(process_id)
    my_inputs = my_process.dataInputs

    input_names = []
    for input in my_inputs:
        input_names.append(input)


    input_url = timeseries_url
    inputs = [ ("url", input_url), ("interval", "daily"), ("stat", "median")]

    #executing the process..
    output = "output"
    execution = my_engine.execute(process_id, inputs, output)

    #checking the status...
    #monitorExecution will run until the process is completed...
    monitorExecution(execution)

    output_data = execution.processOutputs
    final_output_url = output_data[0].reference
    return final_output_url

