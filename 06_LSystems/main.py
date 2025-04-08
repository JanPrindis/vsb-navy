# PRI0192
import math
import tkinter as tk
from functools import partial


class LSystems:
    def __init__(self, root):
        self.root = root
        self.root.title("L-Systems")
        self.root.geometry("1000x600")

        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.canvas_frame = tk.Frame(self.main_frame, width=1000, height=1000)
        self.canvas_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.canvas = tk.Canvas(self.canvas_frame, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.control_frame = tk.Frame(self.main_frame, width=200, padx=10, pady=10)
        self.control_frame.pack(side=tk.RIGHT, fill=tk.Y)

        self.startingPosX_entry = self.add_labeled_entry(self.control_frame, "Starting Pos X", 200)
        self.startingPosY_entry = self.add_labeled_entry(self.control_frame, "Starting Pos Y", 200)
        self.startingAngle_entry = self.add_labeled_entry(self.control_frame, "Starting Angle (deg)")
        self.maxNesting_entry = self.add_labeled_entry(self.control_frame, "Max Nesting", 3)
        self.axiom_entry = self.add_labeled_entry(self.control_frame, "Axiom (F, +, -, [, ])")
        self.rule_entry = self.add_labeled_entry(self.control_frame, "Rule (F, +, -, [, ])")
        self.angle_entry = self.add_labeled_entry(self.control_frame, "Angle (deg)", 0)
        self.line_length = self.add_labeled_entry(self.control_frame, "Line length", 10)

        self.draw_button = tk.Button(self.control_frame, text="Draw", command=self.draw)
        self.draw_button.pack(pady=5)

        self.clear_button = tk.Button(self.control_frame, text="Clear", command=self.clear)
        self.clear_button.pack(pady=5)

        for i in range(1, 5):
            btn = tk.Button(self.control_frame, text=f"Example {i}", command=partial(self.draw_demo, i))
            btn.pack(pady=2)

    @staticmethod
    def add_labeled_entry(parent, label_text, initial_value=None):
        label = tk.Label(parent, text=label_text)
        label.pack()
        entry = tk.Entry(parent)

        if initial_value:
            entry.insert(0, initial_value)

        entry.pack()
        return entry

    @staticmethod
    def apply_rule(axiom: str, rule: str):
        return axiom.replace('F', rule)

    @staticmethod
    def set_default_int(var):
        if var == '':
            return 0
        else:
            return int(var)

    @staticmethod
    def set_default_float(var):
        if var == '':
            return 0.0
        else:
            return float(var)

    def draw_internal(self, axiom, rule,  max_nesting, pos_x, pos_y, angle, angle_step, length):
        # Clear the canvas
        self.clear()

        # Apply rule to axiom
        if rule != '':
            for i in range(max_nesting):
                axiom = self.apply_rule(axiom, rule)

        checkpoint_stack = []

        for c in axiom:
            if c == 'F':
                angle_radians = math.radians(angle)
                x_end = pos_x + length * math.cos(angle_radians)
                y_end = pos_y + length * math.sin(angle_radians)

                self.canvas.create_line(pos_x, pos_y, x_end, y_end)
                pos_x = x_end
                pos_y = y_end

            elif c == '+':
                angle += angle_step

            elif c == '-':
                angle -= angle_step

            elif c == '[':
                checkpoint_stack.append((pos_x, pos_y, angle))

            elif c == ']':
                if checkpoint_stack:
                    pos_x, pos_y, angle = checkpoint_stack.pop()
                else:
                    print("Stack is empty, something broke")

    def draw(self):
        pos_x = self.set_default_int(self.startingPosX_entry.get())
        pos_y = self.set_default_int(self.startingPosY_entry.get())
        angle = self.set_default_float(self.startingAngle_entry.get())
        max_nesting = self.set_default_int(self.maxNesting_entry.get())
        axiom = self.axiom_entry.get()
        rule = self.rule_entry.get()
        angle_step = self.set_default_int(self.angle_entry.get())
        length = self.set_default_int(self.line_length.get())

        if axiom == '':
            print("Pls input the axiom :)")
            return

        self.draw_internal(axiom, rule, max_nesting, pos_x, pos_y, angle, angle_step, length)


    def clear(self):
        self.canvas.delete("all")

    def draw_demo(self, idx):

        if idx == 1:
            self.draw_internal(
                axiom=' F+F+F+F',
                rule='F+F-F-FF+F+F-F',
                max_nesting=3,
                pos_x = 200,
                pos_y = 150,
                angle=0,
                angle_step=90,
                length=5
            )
        elif idx == 2:
            self.draw_internal(
                axiom='F++F++F',
                rule=' F+F--F+F',
                max_nesting=3,
                pos_x = 100,
                pos_y = 100,
                angle=0,
                angle_step=60,
                length=18
            )
        elif idx == 3:
            self.draw_internal(
                axiom='F',
                rule=' F[+F]F[-F]F',
                max_nesting=3,
                pos_x = 100,
                pos_y = 200,
                angle=0,
                angle_step=math.degrees(3.141592653589793232 / 7.0),
                length=18
            )
        elif idx == 4:
            self.draw_internal(
                axiom='F',
                rule=' FF+[+F-F-F]-[-F+F+F]',
                max_nesting=3,
                pos_x = 100,
                pos_y = 150,
                angle=0,
                angle_step=math.degrees(3.141592653589793232 / 8.0),
                length=18
            )


if __name__ == "__main__":
    root = tk.Tk()
    app = LSystems(root)
    root.mainloop()