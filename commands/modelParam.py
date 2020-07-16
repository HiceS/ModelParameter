import adsk.core
handlers = []

class modelParamCreated(adsk.core.CommandCreatedEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args):
        eventArgs = adsk.core.CommandCreatedEventArgs.cast(args)
        app = adsk.core.Application.get()
        cmd = eventArgs.command

        inputs = cmd.commandInputs

        # If there are default units use them - otherwise use cm.
        units = "cm"
        if (app.activeDocument.design.fusionUnitsManager):
            units = app.activeDocument.design.fusionUnitsManager.defaultLengthUnits

        selectionInput = inputs.addSelectionInput("model_sel", "Model Select", "Component Selected")
        selectionInput.tooltip = "Component to attach the model parameter."
        selectionInput.setSelectionLimits(1)
        selectionInput.addSelectionFilter("Occurrences")

        inputs.addStringValueInput('name', 'Name', 'Name of the parameter to be added.')

        inputs.addValueInput('param', 'Value', units, adsk.core.ValueInput.createByReal(0.0))

        # Connect to the execute event.
        onExecute = modelParamExecuted()
        cmd.execute.add(onExecute)
        handlers.append(onExecute)


class modelParamInputChanged(adsk.core.InputChangedEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args):
        eventArgs = adsk.core.InputChangedEventArgs.cast(args)
        inputs = eventArgs.inputs

        # This is possible but I have alot to do at the moment. ----

        # selectionInput = inputs.itemById("model_sel")

        # if selectionInput is not None:
        #     if selectionInput.component.modelParameters is not None:
        #        selectionInput.component.modelParameters.itemByName(inputs.itemById("name"))

        #valueInput = inputs.itemById("param")

class modelParamExecuted(adsk.core.CommandEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args):
        eventArgs = adsk.core.CommandEventArgs.cast(args)

        # Code to react to the event.
        app = adsk.core.Application.get()
        ui  = app.userInterface

        inputs = eventArgs.command.commandInputs

        selectionInput = inputs.itemById("model_sel")
        nameInput = inputs.itemById("name")
        valueInput = inputs.itemById("param")

        if selectionInput is not None:
            params = selectionInput.component.modelParameters
            if params is not None:
                pass
                # Turns out you can't - you technically can but it's not worth it.
            else:
                ui.messageBox(f"Cannot get Model Parameters for {selectionInput.name}")

        ui.messageBox(f"Add or change {selectionInput.name},\n\t - {nameInput}: {valueInput}")