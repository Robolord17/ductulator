import tkinter as tk
import math
from fractions import Fraction

class DuctulatorApp:
    def __init__(self, root):
        self.root = root
        root.title('Ductulator')

        # create and set initial variable values
        self.cfm = tk.DoubleVar(value=0)
        self.velocity = tk.DoubleVar(value=0)
        self.friction_loss = tk.DoubleVar(value=0.00)
        self.rectangular_width = tk.DoubleVar(value=0)
        self.rectangular_height = tk.DoubleVar(value=0)
        self.round_diameter = tk.DoubleVar(value=0)
        self.aspect_ratio = tk.StringVar()
        
        # Trace variables
        self.cfm.trace_add("write", self.update_sizes)
        self.velocity.trace_add("write", self.update_sizes)
        self.friction_loss.trace_add("write", self.update_sizes)
        self.rectangular_width.trace_add("write", self.update_sizes)
        self.rectangular_height.trace_add("write", self.update_sizes)
        self.round_diameter.trace_add("write", self.update_sizes)

        # Create widgets
        self.create_widgets()
    
    def create_widgets(self):
        # create and place labels, entry widgets, and button
        tk.Label(self.root, text="Friction Loss (inWG/100 ft.):").grid(row=0, column=0, sticky='w')
        tk.Spinbox(self.root, from_=0, to=10, increment=0.01, textvariable=self.friction_loss, command=self.delayed_update_sizes).grid(row=0, column=1)  # Adjusted row number
        # tk.Entry(self.root, textvariable=self.friction_loss).grid(row=0, column=1, sticky='e')

        tk.Label(self.root, text="CFM:").grid(row=1, column=0, sticky='w')
        tk.Spinbox(self.root, from_=0, to=300000, increment=5.0, textvariable=self.cfm, command=self.delayed_update_sizes).grid(row=1, column=1)
        # tk.Entry(self.root, textvariable=self.cfm).grid(row=1, column=1, sticky='e')

        tk.Label(self.root, text="Velocity (FPM):").grid(row=2, column=0, sticky='w')
        tk.Spinbox(self.root, from_=0, to=10000, increment=10.0, textvariable=self.velocity, command=self.delayed_update_sizes).grid(row=2, column=1)  # Added velocity spinbox
        # tk.Entry(self.root, textvariable=self.velocity).grid(row=2, column=1, sticky='e')

        tk.Label(self.root, text="Round Duct Diameter (inches):").grid(row=4, column=0, sticky='w')
        # tk.Spinbox(self.root, from_=0, to=100, increment=1, textvariable=self.round_diameter, command=self.delayed_update_sizes).grid(row=4, column=1)
        tk.Entry(self.root, textvariable=self.round_diameter, state='readonly').grid(row=4, column=1, sticky='e')

        tk.Label(self.root, text="Rectangular Duct Height (inches):").grid(row=5, column=0, sticky='w')
        tk.Spinbox(self.root, from_=0, to=100, increment=1, textvariable=self.rectangular_height, command=self.delayed_update_sizes).grid(row=5, column=1)
        # tk.Entry(self.root, textvariable=self.rectangular_height).grid(row=5, column=1, sticky='e')

        tk.Label(self.root, text="Rectangular Duct Width (inches):").grid(row=6, column=0, sticky='w')
        tk.Spinbox(self.root, from_=0, to=100, increment=1, textvariable=self.rectangular_width, command=self.delayed_update_sizes).grid(row=6, column=1)
        # tk.Entry(self.root, textvariable=self.rectangular_width).grid(row=6, column=1, sticky='e')

        tk.Label(self.root, text="Aspect Ratio:").grid(row=7, column=0, sticky='w')
        tk.Entry(self.root, textvariable=self.aspect_ratio, state='readonly').grid(row=7, column=1, sticky='e')

    
    def delayed_update_sizes(self):
        self.root.after_idle(self.update_sizes)
     
    # define calculation function
    def update_sizes(self, *args):
        # get the input values
        cfm = self.cfm.get()
        friction_loss = self.friction_loss.get()  # convert from in/100ft to in/ft
        velocity_fpm = self.velocity.get()

        # Convert velocity from FPM to ft/s
        velocity = velocity_fpm / 60.0

        # Calculate round duct diameter based on user-entered CFM & Velocity
        # round_duct_diameter_value = math.sqrt((4 * cfm_value) / (math.pi * velocity_value_fps))

        #empirical fit to the Darcy-Weisbach equation...
        round_duct_diameter = ((0.109136 * (cfm ** 1.9)) / friction_loss) ** 0.2
        self.round_diameter.set(int(round(round_duct_diameter)))  # convert to integer and round to nearest whole number

        round_duct_area = math.pi * (round_duct_diameter ** 2) / 4

        # get the current rectangular duct height and width
        rectangular_duct_height = self.rectangular_height.get()
        rectangular_duct_width = self.rectangular_width.get()
        
        # if the product of the current height and width is significantly different from
        # the round duct area, it means the user has changed the height
        
        if rectangular_duct_height == 0:
            # assume initial aspect ratio of 1
            rectangular_duct_height = math.sqrt(round_duct_area)
            rectangular_duct_width = rectangular_duct_height
        elif abs(rectangular_duct_height * rectangular_duct_width - round_duct_area) > 0.1:
            # recalculate the width based on the current height and round duct area
            rectangular_duct_width = round_duct_area / rectangular_duct_height
        else:
            # calculate the height and width based on the round duct area (aspect ratio of 1:1)
            rectangular_duct_height = math.sqrt(round_duct_area)
            rectangular_duct_width = round_duct_area / rectangular_duct_height

        # check if the user has manually updated rectangular duct height
        # if float(self.rectangular_height.get()) == 0:
        #     aspect_ratio_value = 1
        #     rectangular_duct_height = math.sqrt(round_duct_area)
        #     rectangular_duct_width = rectangular_duct_height
        # else:
        #     rectangular_duct_height = float(rectangular_height.get())
        #     # calculate rectangular duct width
        #     rectangular_duct_width = round_duct_area / rectangular_duct_height
    
        # set the rectangular duct height and width
        self.rectangular_height.set(round(rectangular_duct_height))
        self.rectangular_width.set(round(rectangular_duct_width))

        # calculate and display aspect ratio
        aspect_ratio_val = Fraction(round(rectangular_duct_height) / round(rectangular_duct_width)).limit_denominator()
        self.aspect_ratio.set(f"{aspect_ratio_val.numerator}:{aspect_ratio_val.denominator}")



# run the main loop
root = tk.Tk()
app = DuctulatorApp(root)
root.mainloop()