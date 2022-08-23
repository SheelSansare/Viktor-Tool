from pathlib import Path

from viktor import File, Color, ViktorController, UserException
from viktor.external.word import WordFileTag, WordFileImage, render_word_file
from viktor.external.spreadsheet import SpreadsheetCalculation, SpreadsheetCalculationInput
from viktor.geometry import CircularExtrusion, SquareBeam, Extrusion, Material, Line, Point, Group
from viktor.result import DownloadResult
from viktor.parametrization import ViktorParametrization, Step, GeoPointField, NumberField, DownloadButton, DateField, \
    IntegerField, OptionField, Table, TextField, TextAreaField, FileField, DynamicArray, OptionListElement, Text, \
    Section, BooleanField, Lookup, Tab
from viktor.utils import convert_word_to_pdf
from viktor.views import MapView, MapPoint, MapLegend, MapLabel, MapResult, PDFView, PDFResult, GeometryView, \
    GeometryResult, DataGroup, DataItem, DataStatus, PNGView, PNGResult, PlotlyAndDataView, PlotlyAndDataResult, Label, GeometryAndDataResult, GeometryAndDataView

barnumbers = [3, 4, 5, 6, 7, 8, 9, 10, 11, 14, 18]
bardiameters = [.375, .5, .625, .75, .875, 1, 1.128, 1.27, 1.41, 1.693, 2.257]
def get_diameter(bar):
    return bardiameters[barnumbers.index(bar)]

def calculate(a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w):
    
    inputs = [
        SpreadsheetCalculationInput('PDL', a),  
        SpreadsheetCalculationInput('PLL', b), 
        SpreadsheetCalculationInput('woverburden', c),  
        SpreadsheetCalculationInput('qallow', d), 
        SpreadsheetCalculationInput('Include Ftg SW', e),  
        SpreadsheetCalculationInput('Xftg', f), 
        SpreadsheetCalculationInput('Yftg', g),  
        SpreadsheetCalculationInput('Xcol', h), 
        SpreadsheetCalculationInput('Ycol', i),  
        SpreadsheetCalculationInput('fc', j), 
        SpreadsheetCalculationInput('Cover', k),  
        SpreadsheetCalculationInput('h', l), 
        SpreadsheetCalculationInput('Bar Size x', m),  
        SpreadsheetCalculationInput('# Bars x', n), 
        SpreadsheetCalculationInput('fy x', o),  
        SpreadsheetCalculationInput('Bar Size y', p), 
        SpreadsheetCalculationInput('# Bars y', q),  
        SpreadsheetCalculationInput('fy y', r), 
        SpreadsheetCalculationInput('fyt', s),  
        SpreadsheetCalculationInput('Bar Size shear', t), 
        SpreadsheetCalculationInput('Spacing - x', u),  
        SpreadsheetCalculationInput('Spacing - y', v), 
        SpreadsheetCalculationInput('Include', w)  
    ]

    sheet_path = Path(__file__).parent / 'sft.xlsx'
    sheet = SpreadsheetCalculation.from_path(sheet_path, inputs=inputs)
    spreadsheet_result = sheet.evaluate(include_filled_file=False)
    return spreadsheet_result.values  

def check_dcr(dcr):
    if (float(dcr) >= 1.00):
        status = DataStatus.ERROR
        status_msg = 'Failed'
    if (float(dcr) < 0.95):
        status = DataStatus.SUCCESS
        status_msg = 'Pass'
    if (float(dcr) < 1.00 and float(dcr) >= 0.95):
        status = DataStatus.WARNING
        status_msg = "Ok"
    return status, status_msg

class Parametrization(ViktorParametrization):

    spt = Step("Spread Footing Tool", views=['geometry_data_view'])
    spt.text1 = Text(
        "Loading Input"
    )
    spt.p_dl = NumberField(
        "Pdl", suffix='k', default=438,
        description="Pdl"
    )
    spt.p_ll = NumberField(
        "Pll", suffix='k', default=260,
        description="Pll"
    )
    spt.w_overburden = NumberField(
        "w_overburden", suffix='ksf', default=0,
        description="Used in bearing check"
    )
    spt.text2 = Text(
        "Footing Parameter Input"
    )
    spt.q_allow = NumberField(
        "q_allow", suffix='ksf', default=19,
        description="Allowable bearing pressure"
    )
    spt.ftg_sw = BooleanField("Include Footing SW?", default=True, flex=30)
    spt.text3 = Text(
        "Concrete"
    )
    spt.x_ftg = NumberField(
        "X_ftg", suffix='in', min=0, default=216, step=12,
        description="Footing width"
    )
    spt.y_ftg = NumberField(
        "Y_ftg", suffix='in', min=0, default=216, step=12,
        description="Footing length"
    )
    spt.x_col = NumberField(
        "X_col", suffix='in', min=0, default=20, step=6,
        description="Column x"
    )
    spt.y_col = NumberField(
        "Y_col", suffix='in', min=0, default=14, step=6,
        description="Column y"
    )
    spt.fc = NumberField(
        "F'c", suffix='ksi', min=0, default=6,
        description="Column y"
    )
    spt.cover = NumberField(
        "Cover", suffix='in', min=0, default=3,
        description="Column y"
    )
    spt.h = NumberField(
        "h", suffix='in', min=0, default=60,
        description="Footing thickness"
    )
    spt.text4 = Text(
        "Flexure Reinforcement (X-direction)"
    )
    spt.barsize_x = NumberField(
        "Bar Size", min=0, max=18, step=1, default=9,
        description="Bar size"
    )
    spt.numbars_x = NumberField(
        "Number of Bars", min=0, step=1, default=53,
        description="Number of bars"
    )
    spt.fy_x = NumberField(
        "Fy", suffix='ksi', min=0, default=60,
        description="Reinforcing steel strength"
    )
    spt.text5 = Text(
        "Flexure Reinforcement (Y-direction)"
    )
    spt.barsize_y = NumberField(
        "Bar Size", min=0, max=18, step=1, default=11,
        description="Bar size"
    )
    spt.numbars_y = NumberField(
        "Number of Bars", min=0, step=1, default=53,
        description="Number of bars"
    )
    spt.fy_y = NumberField(
        "Fy", suffix='ksi', min=0, default=60,
        description="Reinforcing steel strength"
    )
    spt.text6 = Text(
        "Shear Reinforcement (optional)"
    )
    spt.f_yt = NumberField(
        "F_yt", suffix='ksi', min=0, default=60,
        description="Reinforcing steel strength"
    )
    spt.barsize_shear = NumberField(
        "Bar Size", min=0, max=18, step=1, default=6,
        description="Bar size"
    )
    spt.spacing_x = NumberField(
        "Spacing - X", suffix='in', min=0, default=6,
        description="X spacing"
    )
    spt.spacing_y = NumberField(
        "Spacing - Y", suffix='in', min=0, default=6,
        description="Y spacing"
    )
    spt.text7 = Text(
        "Size Effect Factor"
    )
    spt.size_effect= BooleanField("Include Size Effect Factor?", default=True, flex=30)
    
  
   

class Controller(ViktorController):
   
    label = 'My Entity Type'  # label of the entity type as seen by the user in the app's interface
    parametrization = Parametrization  # parametrization associated with the editor of the MyEntityType entity type

    @GeometryAndDataView("Model and Results", duration_guess=2)
    def geometry_data_view(self, params, **kwargs):

        inputs = params.spt
        print(inputs.ftg_sw)
        if (inputs.ftg_sw == True):
            ftg_sw = "YES"
        else:
            ftg_sw = "NO"
        if (inputs.size_effect == True):
            size_effect = "YES"
        else:
            size_effect = "NO"
    
        outputs = calculate(inputs.p_dl, inputs.p_ll, inputs.w_overburden, inputs.q_allow, ftg_sw, inputs.x_ftg, inputs.y_ftg, 
            inputs.x_col, inputs.y_col, inputs.fc, inputs.cover, inputs.h, inputs.barsize_x, inputs.numbars_x, inputs.fy_x, inputs.barsize_y, 
            inputs.numbars_y, inputs.fy_y, inputs.f_yt, inputs.barsize_shear, inputs.spacing_x, inputs.spacing_y, size_effect)
        dcr_bearing = outputs['Bearing_DCR']
        dcr_flexure_x = outputs['Flexure_X_DCR']
        dcr_flexure_y = outputs['Flexure_Y_DCR']
        dcr_onewayshear = outputs['OneWayShear_DCR']
        dcr_twowayshear = outputs['TwoWayShear_DCR']
        final_check = outputs['CodeCheck']

        max_flexure = max(float(dcr_flexure_x), float(dcr_flexure_y))
        max_shear = max(float(dcr_onewayshear), float(dcr_twowayshear))
        #get status of checks (ei. pass/fail)
        bearing_status, bearing_message = check_dcr(dcr_bearing)
        flexure_x_status, flexure_x_message = check_dcr(dcr_flexure_x)
        flexure_y_status, flexure_y_message = check_dcr(dcr_flexure_y)
        flexure_status, flexure_message = check_dcr(max_flexure)
        onewayshear_status, onewayshear_message = check_dcr(dcr_onewayshear)
        twowayshear_status, twowayshear_message = check_dcr(dcr_twowayshear)
        shear_status, shear_message = check_dcr(max_shear)
        #creates data
        data = DataGroup(
            bearing = DataItem('Bearing', 'DCR = ' + str(round(dcr_bearing, 2)), status=bearing_status, status_message=bearing_message),
            flexure = DataItem('Flexure', 'Max DCR = ' + str(round(max_flexure, 2)), status=flexure_status, status_message=flexure_message, subgroup=DataGroup(
                x_dir = DataItem('X-Direction', 'DCR = ' + str(round(dcr_flexure_x, 2)), status=flexure_x_status, status_message=flexure_x_message),
                y_dir = DataItem('Y-Direction', 'DCR = ' + str(round(dcr_flexure_y, 2)), status=flexure_y_status, status_message=flexure_y_message)
            )),
            shear = DataItem('Shear', 'Max DCR = ' + str(round(max_shear, 2)), status=shear_status, status_message=shear_message, subgroup=DataGroup(
                oneway = DataItem('One Way Shear', 'DCR = ' + str(round(dcr_onewayshear, 2)), status=onewayshear_status, status_message=onewayshear_message),
                twoway = DataItem('Two Way Shear', 'DCR = ' + str(round(dcr_twowayshear, 2)), status=twowayshear_status, status_message=twowayshear_message)
            ))
        )
       
        concrete_material = Material("concrete", threejs_roughness=.8, threejs_metalness=.2, threejs_opacity=.8)
        steel_material = Material("steel", threejs_roughness=0, threejs_metalness=1, threejs_opacity=1)
        profile_ftg = [
            Point(0, 0),
            Point(0, inputs.y_ftg),
            Point(inputs.x_ftg, inputs.y_ftg),
            Point(inputs.x_ftg, 0),
            Point(0, 0)
        ]
        ftg = Extrusion(profile_ftg, Line((Point(1,1,0)), Point(1,1,inputs.h)), material=concrete_material)
        profile_col = [
            Point(inputs.x_ftg/2 - inputs.x_col/2, inputs.y_ftg/2 - inputs.y_col/2),
            Point(inputs.x_ftg/2 - inputs.x_col/2, inputs.y_ftg/2 + inputs.y_col/2),
            Point(inputs.x_ftg/2 + inputs.x_col/2, inputs.y_ftg/2 + inputs.y_col/2),
            Point(inputs.x_ftg/2 + inputs.x_col/2, inputs.y_ftg/2 - inputs.y_col/2),
            Point(inputs.x_ftg/2 - inputs.x_col/2, inputs.y_ftg/2 - inputs.y_col/2)
        ]
        col = Extrusion(profile_col, Line((Point(1,1,inputs.h)), Point(1,1,inputs.h + min(inputs.x_ftg, inputs.y_ftg)/2)), material=concrete_material)
        
        x_dia = get_diameter(inputs.barsize_x)
        x_spacing = (inputs.y_ftg - (2*inputs.cover) - x_dia) / inputs.numbars_x
        barlocation_x = inputs.cover + x_dia/2
        x_bars = Group([])
        for i in range(inputs.numbars_x):
            #bar
            point1 = Point(inputs.cover, barlocation_x, inputs.cover + x_dia/2)
            point2 = Point(inputs.x_ftg - inputs.cover, barlocation_x, inputs.cover + x_dia/2)
            x_bars.add(CircularExtrusion(x_dia, Line(point1, point2), material=steel_material))
            #hook
            point3 = Point(inputs.x_ftg - inputs.cover, barlocation_x, inputs.cover + x_dia/2 + 3*x_dia + 12*x_dia)
            point4 = Point(inputs.cover, barlocation_x, inputs.cover + x_dia/2 + 3*x_dia + 12*x_dia)
            x_bars.add(CircularExtrusion(x_dia, Line(point2, point3), material=steel_material))
            x_bars.add(CircularExtrusion(x_dia, Line(point1, point4), material=steel_material))
            barlocation_x += x_spacing
        
        y_dia = get_diameter(inputs.barsize_y)
        y_spacing = (inputs.x_ftg - (2*inputs.cover) - get_diameter(inputs.barsize_y)) / inputs.numbars_y
        barlocation_y = inputs.cover + y_dia/2
        y_bars = Group([])
        for i in range(inputs.numbars_y):
            #bar
            point1 = Point(barlocation_y, inputs.cover, inputs.cover + y_dia + x_dia/2 + 1)
            point2 = Point(barlocation_y, inputs.y_ftg - inputs.cover, inputs.cover + y_dia + x_dia/2 + 1)
            y_bars.add(CircularExtrusion(y_dia, Line(point1, point2), material=steel_material))
            #hook
            point3 = Point(barlocation_y, inputs.y_ftg - inputs.cover, inputs.cover + y_dia + x_dia/2 + 1 + 3*y_dia + 12*y_dia)
            point4 = Point(barlocation_y, inputs.cover, inputs.cover + y_dia + x_dia/2 + 1 + 3*y_dia + 12*y_dia)
            y_bars.add(CircularExtrusion(y_dia, Line(point2, point3), material=steel_material))
            y_bars.add(CircularExtrusion(y_dia, Line(point1, point4), material=steel_material))
            barlocation_y += y_spacing
        

        #CircularExtrusion(dia, Line(), material=steel_material)
        
        geometry = [ftg, col, x_bars, y_bars]
        return GeometryAndDataResult(geometry, data)

#visually show load directions and magnitudes on retaining walls
#Visually show the variations in dcr's or any other values along horiz. and vert. of shear walls for a whole building (concrete shear wall PMM3 - Tool)
#batching for mass producing dcr values
#punching shear tool
#plotting vibration analysis

#present to tst on:
#whats possible with this software, how data links work, batching cases, 