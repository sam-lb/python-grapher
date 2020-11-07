import tkinter as tk;
import webbrowser;
from tkinter.colorchooser import askcolor;
from tkinter.messagebox import showinfo;
from Color import preset_styles;
from CAS.Parser import Parser;
from CAS.Manipulator import Manipulator;
from CAS.Errors import UserError;
from mathgraph3D.Color import Styles, ColorStyle, preset_styles;

from mathgraph3D.CartesianFunctions import Function2D, Function3D;
from mathgraph3D.ParametricFunctions import ParametricFunctionT, ParametricFunctionUV, RevolutionSurface;
from mathgraph3D.VectorFunctions import VectorField;
from mathgraph3D.StatisticalPlots import StatPlot2D, StatPlot3D;
from mathgraph3D.OtherCoordinateSystems import CylindricalFunction, SphericalFunction, PolarFunction;
from mathgraph3D.ImplicitPlots import ImplicitPlot2D;
from mathgraph3D.ComplexFunctions import ComplexFunction;
from mathgraph3D.RecurrenceRelation import RecurrenceRelation;
from mathgraph3D.Point import Point;
from mathgraph3D.Plot import Plot;
from mathgraph3D.Errors import GrapherError;

from pygame import Color;
from pprint import pprint;
from mathgraph3D.global_imports import ALLOWED_FUNCTIONS, ALLOWED_COMPLEX_FUNCTIONS;


numerical_parser = Parser(ALLOWED_FUNCTIONS);
expression_parser = Parser(ALLOWED_FUNCTIONS);


FUNCTIONS = [
    "2D function", "3D function", "3D parametric curve", "3D parametric surface",
    "Surface of revolution", "Function with cylindrical coordinates",
    "Function with spherical coordinates", "Vector field", "Polar function",
    "Recurrence relation", "Implicit 2D plot", "Complex function", "Slope field",
];

OTHER_OBJECTS = [
    "2D stat plot", "3D stat plot", "Point", "Plane", "Tangent Plane"
];

OBJECT_TYPES = FUNCTIONS + OTHER_OBJECTS;

REFERENCE_STRINGS = [
    """A map from a single real input to a single real output. Valid symbols: x""",
    """A map from 2 real inputs to a single real output. Valid symbols: x, y""",
    """A curve formed from the points generated by (x(t), y(t), z(t)). Valid symbols: t""",
    """A surface formed from the points generated by (x(u,v), y(u,v), z(u,v)). Valid symbols: u, v""",
    """The surface obtained when the given function of x is rotated about the x axis. Valid symbols: x""",
    """3D generalization of polar coordinates. The radius is a function of an angle and the z value. Valid symbols: z, t""",
    """A function in the spherical coordinate system. The radius is a function of two angles. Valid symbols: t, p""",
    """A map from a point to a vector. Valid symbols: x, y, z""",
    """A function that maps an angle to a radius. Valid symbols: t""",
    """A sequence in which the n+1th output depends on the nth output. Valid symbols: n""",
    """The set of all points in the domain such that the two given functions of x and y are equal. Valid symbols: x, y""",
    """A map from a single complex input to a single complex output. Since there are four dimensions involved, the fourth dimension is represented as color. Valid symbols: z""",
    """The slope field of the given function. Valid symbols: x, y""",
    """A curve formed by a set of numerical points rather than a continuous function""",
    """A surface formed by a mesh of numerical points rather than a continuous function""",
    """A single point in 3D space""",
    """A plane formed from 3 points""",
    """A plane tangent to a function of x and y at a point. Valid Symbols: x, y""",
];

PROMPTS = [
    ("f(x)=",), ("f(x,y)=",), ("x(t)=", "y(t)=", "z(t)="), ("x(u,v)=", "y(u,v)=", "z(u,v)="),
    ("f(x)=",), ("r(z,t)=",), ("r(t,p)=",), ("x(x,y,z)=", "y(x,y,z)=", "z(x,y,z)="), ("r(t)=",),
    ("a(n)=", "seed value: "), ("f(x,y)=", "g(x,y)="), ("f(z)=",), ("f(x,y)=",), ("Enter file name: ",), ("Enter file name: ",),
    ("Enter point in (x, y, z) format: ",), ("Point 1", "Point 2", "Point 3"), ("f(x,y)=", "x=", "y="),
];

SOLID_ONLY = [
    True, False, True, False, False, False, False, True, True, True, True, None, True, True, False, True, False, False,
];

LIGHTING_APPLICABLE = [
    False, True, False, True, True, True, True, False, False, False, False, True, False, False, True, False, False, True,
];

MESHING_APPLICABLE = [
    False, True, False, True, True, True, True, False, False, False, False, True, False, False, True, False, True, True,
];

PARSER_VALID_SYMBOLS = [
    ("x",), ("x", "y"), ("t",), ("u", "v"), ("x",), ("z", "t"), ("t", "p"), ("x", "y", "z"), ("t",),
    ("n",), ("x", "y"), ("z",), ("x", "y"), None, None, None, None, ("x", "y"),
];

PLOT_OBJECTS = [
    Function2D, Function3D, ParametricFunctionT, ParametricFunctionUV,
    RevolutionSurface, CylindricalFunction, SphericalFunction,
    VectorField, PolarFunction, RecurrenceRelation, ImplicitPlot2D,
    ComplexFunction, VectorField.slope_field_of, StatPlot2D, StatPlot3D,
    Point, Plot.plane_from_3_points, Plot.tangent_plane,
];

COLOR_TYPES = [
    "solid", "checkerboard", "gradient", "vertical striped", "horizontal striped", "color set",
];

COLOR_CC = [          # (Styles constant, number of required colors)
    (Styles.SOLID, 1), (Styles.CHECKERBOARD, 2), (Styles.GRADIENT, 2),
    (Styles.VERTICAL_STRIPED, 2), (Styles.HORIZONTAL_STRIPED, 2), (Styles.COLOR_SET, 5),
];

COLOR_DATA = dict(zip(COLOR_TYPES, COLOR_CC));

OBJECT_DATA = dict(zip(OBJECT_TYPES, zip(REFERENCE_STRINGS, PROMPTS, SOLID_ONLY, LIGHTING_APPLICABLE, MESHING_APPLICABLE, PARSER_VALID_SYMBOLS, PLOT_OBJECTS)));
##pprint(OBJECT_DATA);

SUBFRAME_COLOR = "#f0f0ff";
BUTTON_COLOR = "#ccccff";
BLINK_COLOR = "#ffcccc";
COLOR_STYLES = [];


def set_text(entry, text, clear=True):
    if clear: entry.delete(0, tk.END);
    entry.insert(0, text);
    

class Interface(tk.Frame):

    """ A tkinter GUI for the grapher. allows user to create plots within the application """

    def __init__(self, master, *args, **kwargs):
        tk.Frame.__init__(self, master, *args, **kwargs);
        self.master = master;
        self.master.title("MathGraph3D");
        self.master.grid_columnconfigure(2, weight=1);
        self.master.grid_columnconfigure(3, weight=1);
        self.objects = [];
        #self.master.iconbitmap("img/torus2.ico");

    def set_plot(self, plot):
        self.plot = plot;
        self.create_widgets();

    def show_message(self, msg, title="Notice", error=False, callback=None):
        """ show a message to the user """
        showinfo(title, "Error: " * error + msg);
        if callable(callback): callback();

    def create_widgets(self):
        """ create widgets for plot bounds, toggles for axes, angles, tracker, spin, and buttons to draw new plots """
        self.plot_to_open = tk.StringVar(self, value="Add a new object to the plot");
        menu = tk.OptionMenu(self.master, self.plot_to_open, *OBJECT_TYPES, command=self.on_new_plot);
        menu.configure(background=BUTTON_COLOR);
        menu.grid(row=0, column=3);
        self.create_function_frame();
        self.create_plot_settings();
        tk.Button(self.master, text="Website", command=lambda: webbrowser.open_new_tab("http://sambrunacini.com/")).grid(row=3, column=3, sticky=tk.N);
        tk.Label(self.master, text="Created by Sam Brunacini").grid(row=4, column=3, sticky=tk.N);

    def on_new_plot(self, event):
        """ called when the user selects a new plot to add """
        plot_type = self.plot_to_open.get();
        
        self.add_object(plot_type);
        self.plot_to_open.set("Add a new object to the plot");

    def create_function_frame(self):
        """ create the frame where the functions on the plot are displayed """
        self.function_frame = tk.Frame(self.master, borderwidth=3, relief="groove", background=SUBFRAME_COLOR);
        tk.Label(self.function_frame, text="Plots currently on the graph: ").grid(row=0, column=0);
        self.function_frame.grid(row=0, column=2, rowspan=6, sticky=tk.N+tk.S+tk.W+tk.E);
        self.function_frame.grid_columnconfigure(0, weight=1);
        self.function_frame_row = 1;

    def create_plot_settings(self):
        # bound zoom, scale zoom, background color?, axes, angles, labels, cube,
        # spin, line numbers, ticks
        self.plot_options_frame = tk.Frame(self.master, borderwidth=3, relief="groove", background=SUBFRAME_COLOR);
        tk.Label(self.plot_options_frame, text="Plot settings").grid(row=0, column=0, columnspan=4);
        tk.Button(self.plot_options_frame, text="scale up", command=lambda: self.plot.zoom(20)).grid(row=1, column=0);
        tk.Button(self.plot_options_frame, text="scale down", command=lambda: self.plot.zoom(-20)).grid(row=1, column=1);
        tk.Button(self.plot_options_frame, text="zoom in", command=lambda: self.plot.set_bounds(self.plot.x_start + 1,
                                                                                                self.plot.x_stop - 1,
                                                                                                self.plot.y_start + 1,
                                                                                                self.plot.x_stop - 1,
                                                                                                self.plot.z_start + 1,
                                                                                                self.plot.z_stop - 1,
                                                                                                anch=True)).grid(row=1, column=2);
        tk.Button(self.plot_options_frame, text="zoom out", command=lambda: self.plot.set_bounds(self.plot.x_start - 1,
                                                                                                 self.plot.x_stop + 1,
                                                                                                 self.plot.y_start - 1,
                                                                                                 self.plot.y_stop + 1,
                                                                                                 self.plot.z_start - 1,
                                                                                                 self.plot.z_stop + 1,
                                                                                                 anch=True)).grid(row=1, column=3, pady=25);
        tk.Button(self.plot_options_frame, text="toggle axes", command=self.plot.toggle_axes).grid(row=2, column=0);
        tk.Button(self.plot_options_frame, text="toggle angles", command=self.plot.toggle_angles).grid(row=2, column=1);
        tk.Button(self.plot_options_frame, text="toggle labels", command=self.plot.toggle_labels).grid(row=2, column=2);
        tk.Button(self.plot_options_frame, text="toggle cube", command=self.plot.toggle_cube).grid(row=2, column=3, pady=25);
        tk.Button(self.plot_options_frame, text="toggle spin", command=self.plot.toggle_spin).grid(row=3, column=0);
        tk.Button(self.plot_options_frame, text="toggle line numbers", command=self.plot.toggle_line_numbers).grid(row=3, column=1, columnspan=2);
        tk.Button(self.plot_options_frame, text="toggle ticks", command=self.plot.toggle_ticks).grid(row=3, column=3, pady=25);
        self.plot_options_frame.grid(row=1, column=3, sticky=tk.N);

    def add_object(self, object_type):
        """ Add an object to the plot, and create the settings widget for it in the GUI """
        obj = GraphObject(self, self.function_frame, self.function_frame_row, object_type);
        self.GOSWin = GraphObjectSettingsWindow(self, object_type, obj);
        self.function_frame_row += 1;


class GraphObjectSettingsWindow(tk.Toplevel):

    """ A window for configuring the settings of a graph object """

    def __init__(self, master, object_type, assoc_object):
        tk.Toplevel.__init__(self, master);
        self.master = master;
        self.geometry("400x400");
        self.configure(background=SUBFRAME_COLOR);
        self.deiconify();
        self.focus();
        self.enforce = True;

        self.bind("<FocusOut>", self.alarm);
        #self.grab_set();
        
        self.object_type = object_type;
        self.data = OBJECT_DATA[object_type];
        self.associated_object = assoc_object;
        self.text_inputs = {};
        
        self.create_widgets();

    def alarm(self, event):
        """ handle when the user tries to click away """
        if self.enforce:
            pass;
            #self.focus_force();
            #self.blink();

    def blink(self, blinks=3, blink_length=80):
        """ blink the window """
        self.configure(background=BLINK_COLOR);
        for i in range(blinks):
            self.after(blink_length, lambda: self.configure(background=BLINK_COLOR));
            self.after(blink_length, lambda: self.configure(background=SUBFRAME_COLOR));

    def create_input_box(self, frame, label, row, v=None):
        """ create a text input box and a label for it """
        tk.Label(frame, text=label).grid(row=row, column=0, sticky=tk.W);
        sv = tk.StringVar(frame);
        if v is not None:
            sv.set(v);
        self.text_inputs[label] = sv;
        self.add_data(label, sv);
        tk.Entry(frame, textvariable=sv).grid(row=row, column=1, sticky=tk.W);

    def create_widgets(self):
        """ generate widgets from self.data """
        edit = self.associated_object.obj_data != dict();
        
        row = 2;
        tk.Label(self, text=self.object_type).grid(row=0, column=0, sticky=tk.W);
        tk.Label(self, text=self.data[0], wraplength=300, justify=tk.LEFT).grid(row=1, column=0, sticky=tk.W);
        input_frame = tk.Frame(self, borderwidth=3, relief="groove", background=SUBFRAME_COLOR);
        for i, prompt in enumerate(self.data[1]):
            v = None if not edit else self.associated_object.obj_data[prompt].get();
            self.create_input_box(input_frame, prompt, i, v);
        input_frame.grid(row=row, sticky=tk.W);
        row += 1;
            
        self.style = tk.StringVar(self, value="select...");
        color_frame = tk.Frame(self, borderwidth=3, relief="groove", background=SUBFRAME_COLOR);
        if edit:
            self.style.set(self.associated_object.obj_data["style"].get());
            self.color_style_set(color_frame, 0, edit=True);
        self.add_data("style", self.style);

        if self.data[2]: # solid only
            self.style.set("solid"); 
            self.color_style_set(color_frame, 0);
        elif self.data[2] is None:
            pass;
        else:
            tk.OptionMenu(self, self.style, *(COLOR_TYPES + ["preset"]),
                          command=lambda event: self.color_style_set(color_frame, 0)).grid(row=row, sticky=tk.W);
            row += 1;
            
        color_frame.grid(row=row, sticky=tk.W);
        row += 1;

        if self.data[4]:
            mesh, surf = tk.IntVar(self), tk.IntVar(self);
            if edit:
                mesh.set(self.associated_object.obj_data["mesh"].get());
                surf.set(self.associated_object.obj_data["surf"].get());
            else:
                mesh.set(1); surf.set(1);
                
            self.add_data("mesh", mesh);
            self.add_data("surf", surf);
            tk.Checkbutton(self, text="Mesh", var=mesh).grid(row=row, sticky=tk.W);
            tk.Checkbutton(self, text="Surface", var=surf).grid(row=row+1, sticky=tk.W);
            row += 2;

        if edit:
            tk.Button(self, text="Save edits", command=self.on_edit).grid(row=row);
        else:
            tk.Button(self, text="Add to Plot", command=self.on_complete).grid(row=row);

    def color_box(self, frame, row, text="Color: ", data_name="fill color", edit=False):
        """ create widgets for a color picker """
        def on_color_select(cbox, canv, ask=True):
            nonlocal self, edit;
            if ask:
                color = askcolor(initialcolor="red", parent=self)[1];
            elif edit:
                color = "#";
                for color_component in self.associated_object.obj_data[data_name]:
                    subc = hex(color_component)[2:];
                    if len(subc) == 1: subc = "0" + subc;
                    color += subc;
            else:
                color="#ff0000";
            if not color: return;

            cbox.configure(text=color);
            canv.configure(background=color);
            self.add_data(data_name, Color(color)[0:3]);

        color_box = tk.Label(frame, text="#ff0000", borderwidth=3, relief="flat");
        color_box.grid(row=row, column=1);
        tk.Label(frame, text=text).grid(row=row);
        color_preview = tk.Canvas(frame, width=20, height=20);
        color_preview.grid(row=row, column=3);
        on_color_select(color_box, color_preview, ask=False);
        tk.Button(frame, text="select color", command=lambda: on_color_select(color_box, color_preview, ask=True)).grid(row=row, column=2);

    def add_data(self, name, value):
        """ Add data to the GraphObject associated with this window """
        self.associated_object.obj_data[name] = value;

    def color_style_set(self, frame, row, edit=False):
        """ Set the widgets when a ColorStyle is chosen """
        value = self.style.get();
        
        for child in frame.winfo_children():
            child.destroy();

        color_count = COLOR_DATA.get(value);
        if color_count is None:
            tk.Label(frame, text="select preset: ").grid(row=row);
            preset = tk.StringVar(frame, value="tmp");
            if edit: preset.set(self.associated_object.obj_data["preset"].get());
            self.add_data("preset", preset);
            tk.OptionMenu(frame, preset, *sorted(preset_styles.keys()), command=lambda event: None).grid(row=row, column=1);
        else:
            for i in range(1, color_count[1] + 1):
                self.color_box(frame, row, text="Color {}: ".format(i), data_name="color {}".format(i), edit=edit);
                row += 1;
            if self.data[3]:
                lighting = tk.IntVar(frame);
                if edit: lighting.set(self.associated_object.obj_data["lighting"].get());
                tk.Checkbutton(frame, text="Apply lighting", var=lighting).grid(row=row);
                self.add_data("lighting", lighting);
                row += 1;

    def on_complete(self, edit=False):
        """ handle when the user tries to add the object to the plot """
        if not all((box.get() for box in self.text_inputs.values())):
            self.enforce = False;
            self.master.show_message("All text fields must be filled.", error=True);
            self.focus_force();
            self.enforce = True;
        else:
            if edit: prev_obj = self.associated_object.obj;
            success = self.associated_object.build_object();
            if success:
                if edit: self.associated_object.parent.plot.functions.remove(prev_obj);
                self.associated_object.show(edit);
                self.destroy();

    def on_edit(self):
        """ handle when the user is done editing the object """
        self.on_complete(edit=True);
            

class GraphObject:

    """ Any object on the Plot """

    def __init__(self, parent, frame, row, object_type):
        self.parent = parent;
        self.parent_frame = frame;
        self.row = row;
        self.object_type = object_type;
        self.frame = tk.Frame(self.parent_frame, borderwidth=3, relief="groove", background=SUBFRAME_COLOR);
        self.obj = None;
        self.type_data = OBJECT_DATA[self.object_type];
        self.obj_data = {};

    def show(self, edit=False):
        """ show the graph object widget """
        if edit:
            for widget in self.frame.winfo_children(): widget.destroy();
        tk.Label(self.frame, text=self.object_type).grid(row=0, column=0);
        functions = "\n".join((" ".join(f) for f in zip(self.type_data[1], [self.obj_data[prompt].get() for prompt in self.type_data[1]])));
        tk.Label(self.frame, text=functions).grid(row=1, column=0, sticky=tk.W);
        tk.Button(self.frame, text="Edit", command=self.on_edit).grid(row=0, column=1, sticky=tk.E);
        tk.Button(self.frame, text="Delete", command=self.on_delete).grid(row=0, column=2, sticky=tk.E);
        self.frame.grid(row=self.row, column=0, sticky=tk.E+tk.W);

    def on_edit(self):
        """ Handle when the edit button is pressed """
        self.parent.GOSWin = GraphObjectSettingsWindow(self.parent, self.object_type, self);

    def on_delete(self):
        """ Handle when the delete button is pressed """
        self.parent.plot.functions.remove(self.obj);
        self.parent.GOSWin.associated_object = None;
        self.frame.destroy();
        self.parent.plot.needs_update = True;
        
    def build_ColorStyle(self):
        """ Create the ColorStyle object from the data """
        if self.obj_data["style"].get() == "preset":
            return preset_styles[self.obj_data["preset"].get()];

        if self.obj_data["style"].get() == "select...":
            self.obj_data["style"].set("solid");
            self.obj_data["lighting"] = tk.IntVar(value=0);
            self.obj_data["color 1"] = (255, 0, 0)  # set default ColorStyle to solid red
            
        color_data = COLOR_DATA[self.obj_data["style"].get()];
        if color_data[1] == 1:
            colors = {"color": self.obj_data["color 1"]};
        else:
            colors = {"color{}".format(i): self.obj_data["color {}".format(i)] for i in range(1, color_data[1]+1)};
            
        if self.type_data[3]:
            lighting = bool(self.obj_data["lighting"].get());
        else:
            lighting = False;

        return ColorStyle(color_data[0], **colors, apply_lighting=lighting, light_source=(0, 0, 6));

    def build_object(self):
        """ Create a graph object to be added to the plot """
        # Que Daniel Schiffman's "I will refactor this later"
        color_style = self.build_ColorStyle();
        plot = self.parent.plot;

        if self.object_type == "Complex function":
            expression_parser.redefine_functions(**ALLOWED_COMPLEX_FUNCTIONS);
        else:
            expression_parser.redefine_functions(**ALLOWED_FUNCTIONS);

        if self.object_type in FUNCTIONS:
            number_of_functions, params = len(self.type_data[1]), {};
            funcs = self.build_functions(self.type_data[5], number_of_functions);
            if funcs:
                if self.object_type == "Implicit 2D plot":
                    function = self.type_data[6].make_function_string([Manipulator.move_all_terms_to_left(funcs[0], funcs[1])]);
                elif self.object_type == "Slope field":
                    function = Function3D.make_function_string(funcs);
                else:
                    function = self.type_data[6].make_function_string(funcs);
                    
                params["plot"] = plot;
                params["color_style"] = color_style;
                params["function"] = function;
                if self.type_data[4]:
                    params["mesh_on"] = self.obj_data["mesh"].get();
                    params["surf_on"] = self.obj_data["surf"].get();
                if self.object_type == "Recurrence relation":
                    params["seed_value"] = numerical_parser.parse(self.obj_data["seed value: "].get()).evaluate();
                self.obj = self.type_data[6](**params);
                return True;
        else:
            params = {};
            if self.object_type in ("2D stat plot", "3D stat plot"):
                try:
                    params["plot"] = plot;
                    params["color_style"] = color_style;
                    params["file"] = self.obj_data["Enter file name: "].get();
                    if self.type_data[4]:
                        params["mesh_on"] = self.obj_data["mesh"].get();
                        params["surf_on"] = self.obj_data["surf"].get();
                    self.obj = self.type_data[6](**params);
                    return True;
                except GrapherError:
                    self.parent.show_message("File not found. Try the full path? (Note that only csv files with numerical comma separated data work)", callback=self.parent.GOSWin.lift);
                    return False;
            elif self.object_type == "Point":
                point = self.build_point(self.obj_data["Enter point in (x, y, z) format: "].get());
                if point:
                    self.type_data[6](plot, point, self.obj_data["color 1"]);
                    return True;
            elif self.object_type == "Plane":
                points = [self.build_point(self.obj_data[prompt].get()) for prompt in self.type_data[1]];
                if points:
                    try:
                        function = self.type_data[6](*points);
                    except ValueError:
                        self.parent.show_message("Points are colinear, the points are not unique, or the plane is vertical - plane could not be constructed.", callback=self.parent.GOSWin.lift);
                        return False;
                    self.obj = Function3D(plot, function, color_style=color_style, mesh_on=self.obj_data["mesh"].get(), surf_on=self.obj_data["surf"].get());
                    return True;
            elif self.object_type == "Tangent Plane":
                expression_parser.redefine_symbols(*self.type_data[5]);
                try:
                    function = Function3D.make_function_string([expression_parser.parse(self.obj_data["f(x,y)="].get())]);
                    x, y = map(lambda x: numerical_parser.parse(x).evaluate(), (self.obj_data["x="].get(), self.obj_data["y="].get()));
                except Exception:
                    self.parent.show_message("Function or (x,y) is invalid.", error=True, callback=self.parent.GOSWin.lift);
                else:
                    tangent_plane = self.type_data[6](function, x, y);
                    self.obj = Function3D(plot, tangent_plane, color_style=color_style, mesh_on=self.obj_data["mesh"].get(), surf_on=self.obj_data["surf"].get());
                    return True;
        return False;

    def build_point(self, point_string):
        """ build a point from a string """
        try:
            point = tuple(map(lambda pc: numerical_parser.parse(pc).evaluate(), point_string[1:][:-1].split(",")));
        except Exception:
            self.parent.show_message("Invalid point! must be in (x, y, z) format.", error=True, callback=self.parent.GOSWin.lift);
            return False;
        return point;

    def build_functions(self, symbols, num_functions):
        """ build the functions from GUI input """
        try:
            expression_parser.redefine_symbols(*symbols);
            raw_functions = [self.obj_data[prompt].get() for prompt in self.type_data[1]];
            parsed_functions = [expression_parser.parse(func) for func in raw_functions];
        except UserError as e:
            self.parent.show_message("Invalid function(s)!", error=True, callback=self.parent.GOSWin.lift);
            return False;
        return parsed_functions;


class DefineFunctionWindow(tk.Toplevel):

    """ Window for defining a new function """

    def __init__(self, parent):
        tk.Toplevel.__init__(self, parent);
        self.parent = parent;
        self.title("Define a function");
        #self.iconbitmap("img/torus2.ico")

        self.geometry("400x400");
        self.deiconify();
        self.radio_btn_state = tk.IntVar();
        self.radio_btn_state.initialize(1);
        self.function_entry_state = tk.StringVar();
        self.function_label_text = tk.StringVar(value="f(x)=");
        self.function_name_state = tk.StringVar();
        self.create_widgets();

    def create_widgets(self):
        """ add all widgets needed for the window """
        self.msg = tk.StringVar(self, value="Define a new function");
        tk.Label(self, textvariable=self.msg).grid(row=0, column=0);
        tk.Radiobutton(self, text="one variable", variable=self.radio_btn_state, value=1, command=lambda: self.function_label_text.set("f(x)=")).grid(row=1, column=0);
        tk.Radiobutton(self, text="two variables", variable=self.radio_btn_state, value=2, command=lambda: self.function_label_text.set("f(x,y)=")).grid(row=1, column=1);
        tk.Radiobutton(self, text="three variables", variable=self.radio_btn_state, value=3, command=lambda: self.function_label_text.set("f(x,y,z)=")).grid(row=1, column=2);
        tk.Label(self, text="Name: ").grid(row=2, column=0, sticky=tk.W);
        tk.Entry(self, textvariable=self.function_name_state).grid(row=2, column=1, sticky=tk.W);
        tk.Label(self, textvariable=self.function_label_text).grid(row=3, column=0, sticky=tk.W);
        tk.Entry(self, textvariable=self.function_entry_state).grid(row=3, column=1, sticky=tk.W);
        tk.Button(self, text="Add", command=self.on_close).grid(row=4, column=0, sticky=tk.W);

    def on_close(self):
        """ send data to the plotter and tell it a new function should be created. then destroy the window """
        function = self.function_entry_state.get();
        function_name = self.function_name_state.get();
        rbtn_state = self.radio_btn_state.get();

        if function and function_name:
            self.add_data("function", function);
            self.add_data("num vars", rbtn_state);
            self.add_data("function name", function_name);
            self.parent.broadcast_to_plotter("NEW_COMPILED_FUNCTION");
            self.destroy();
        else:
            self.show_message("function box and name box cannot be blank", True);
            return;

    def add_data(self, name, data):
        """ add data to be broadcast to the plotter """
        self.parent.extra_data[name] = data;

    def show_message(self, msg, error=False):
        """ display a message to the user """
        self.msg.set("Error: " * error + msg);
