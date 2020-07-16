
import os
import sys
import adsk.core
import traceback

app_path = os.path.dirname(__file__)

sys.path.insert(0, app_path)
sys.path.insert(0, os.path.join(app_path, 'apper'))

# Set to True to display various useful messages when debugging your app
debug = False

try:
    import config
    import apper

    # Import the command
    from .commands.MPCommand import mpCommand
    from .commands.modelParam import *

    
    app = adsk.core.Application.cast(adsk.core.Application.get())
    ui = app.userInterface

    my_addin = apper.FusionApp(config.app_name, config.company_name, False)

    mpCommand_buttons = ui.commandDefinitions.addButtonDefinition('mp_cmd_og', 'Model Parameters', 'Add or Overwrite Model Parameter', './/commands//resources//command_icons')

    # Connect to the command created event.
    created = modelParamCreated()
    mpCommand_buttons.commandCreated.add(created)

    global handlers
    handlers.append(created)

    # curr = ui.activeWorkspace

    # mess = "Panels ------ \n"
    # for item in curr.toolbarPanels:
    #    mess += f"\t- {item.id} \n"
    # ui.messageBox(mess)

    # Get the ADD-INS panel in the model workspace. 
    solidmodpanel = ui.allToolbarPanels.itemById('SolidModifyPanel')
    sketchmodpanel = ui.allToolbarPanels.itemById('SketchModifyPanel')

    # Add the button to the bottom.
    if solidmodpanel:
        buttonControl1 = solidmodpanel.controls.addCommand(mpCommand_buttons)
    
    if sketchmodpanel:
        buttonControl2 = sketchmodpanel.controls.addCommand(mpCommand_buttons)

except:
    if ui:
        ui.messageBox('Initialization: {}'.format(traceback.format_exc()))

def run(context):
    my_addin.run_app()

def stop(context):
    # Get the UserInterface object and the CommandDefinitions collection.
    ui = app.userInterface

    # Delete the button definition.
    button = ui.commandDefinitions.itemById('mp_cmd_og')
    if button:
        button.deleteMe()
        
    # Get panel the control is in.
    solidmodpanel = ui.allToolbarPanels.itemById('SolidModifyPanel')
    sketchmodpanel = ui.allToolbarPanels.itemById('SketchModifyPanel')

    # Get and delete the button control.
    buttonControl = solidmodpanel.controls.itemById('mp_cmd_og')
    if buttonControl:
	    buttonControl.deleteMe()

    buttonControl = sketchmodpanel.controls.itemById('mp_cmd_og')
    if buttonControl:
	    buttonControl.deleteMe()

    my_addin.stop_app()
    sys.path.pop(0)
    sys.path.pop(0)
