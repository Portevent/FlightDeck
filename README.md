![Version](https://img.shields.io/badge/dynamic/toml?url=https%3A%2F%2Fraw.githubusercontent.com%2FPortevent%2FFlightDeck%2Fmain%2Fpyproject.toml&query=%24.project.version&label=version
)
![Lint](https://github.com/Portevent/FlightDeck/actions/workflows/pylint.yml/badge.svg)
![GitHub License](https://img.shields.io/github/license/Portevent/FlightDeck)

# 🛰 Flight Deck 

FlightDeck let you define pages to be displayed over serial port (Minitel) or with curses.
User can interact with it, and have your frontend react accordingly.
It uses Component, that can display characters within an area and have their own logics.
Component can nest other component, and gives them reference to variable so children automaticly update when their input changes.
You can mark certain component as pages, so you can navigate trought your application

## How to use it
Install FlightDeck with pip
```shell
pip install flight-deck
```

## Basic app
To start using FlightDeck, you must create a client and a display. Currently the only display available is `curses`, but
I plan to add minitel support.

```python
# Define the display
client = FlightDeck().set_display(FlightDeckCursesDisplay())

# Client must be entered to start and exit the display
with client:
    # Do stuff
    ...
```
or
```python
# Client must be entered to start and exit the display
with FlightDeck().set_display(FlightDeckCursesDisplay()) as client:
    # Do stuff
    ...
```

## Basic custom component
We will create a new component that will act as our page.
Its template contains various native components (see full list below)
This component is a basic "Hello world" text, that will be displayed to the user
```python
@Template("""
<page>
    <text text="Hello world"/>
    <br/>
</page>
""")
class SimplePage(Component):
    pass

```


This component is a form component, which mean it can search trought its children for field using `getFormValues`.
It uses Output to dynamicly update the text when user changes (I think so)
```python
@Template("""
<page>
    <text text="My App "/>
    <br/>
    <horizontal>
        <text text="Hello "/>
        <text text="#user"/>
    </horizontal>
    <br/>
    <field name="name" label="My name is" value="World"/>
    <button text="Show" onClick="@showName"/>
</page>
""")
@Output("user")
class HelloPage(FormComponent):

    user: str

    def start(self):
        self.user = "_____"

    def showName(self):
        self.user = self.getFormValues()["name"]

```

To display a page, we can register a route :
```python
with FlightDeck().set_display(FlightDeckCursesDisplay()) as client:

    client.add_route("home", HelloPage)
    
    # Start client
    client.start("home")
```

And we can navigate within our app using navigate_to (as long as the route has been added)

```python
@Template("""
<page>
    <text text="Home"/>
    <br/>
    
    <horizontal>
    
    <br/>
    <button text="Login" onClick="@login"/>
    <button text="Incident Report" onClick="@incidentReportForm"/>
    <button text="Mission" onClick="@mission"/>
</page>
""")
class HomePage(Component):

    def login(self):
        self.client.navigate_to("login")

    def incidentReportForm(self):
        self.client.navigate_to("incidentReportForm")

    def mission(self):
        self.client.navigate_to("mission")
```

We can also register new component to be used by other page :
```python

@ComponentName("logo")
class Logo(Component):
    """
    Logo
    """

    def __init__(self, **kwargs):
        super().__init__(height=3, width=6, **kwargs)

    def display_after_content(self):
        self._displayText(["//==\\\\",
                           "||  ||",
                           "\\\\==//"])

```