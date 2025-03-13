from manim import *
import numpy as np
import trimesh

config.renderer = "opengl"

def simplify_obj(input_path, output_path, target_faces_ratio = 0.1):
    mesh = trimesh.load(input_path)
    if isinstance(mesh,trimesh.Scene):
        if len(mesh.geometry) == 0:
            raise ValueError("The provided .obj file contains no geometry.")
        mesh = list(mesh.geometry.values())[0]
    
    target_reduction = 1 - target_faces_ratio
    simplified = mesh.simplify_quadric_decimation(int(len(mesh.faces)*target_faces_ratio))
    simplified.export(output_path)
    return output_path


# def parse_obj_fast(file_path):
#     vertices = []
#     faces = []
#     with open(file_path, 'r') as f:
#         for line in f:
#             if line.startswith('v '):
#                 parts = list(map(float,line.strip().split()[1:4]))
#                 vertices.append(parts)
#             elif line.startswith('f '):
#                 face = [int(part.split('/')[0]) - 1 for part in line.strip().split()[1:]]
#                 faces.append(face)
#     return np.array(vertices, dtype = np.float32), np.array(faces, dtype = np.int32)
class introduction(ThreeDScene):
    def construct(self):
        original_path = r"E:\\UNM\\Car-Model\\Car.obj"
        simplified_path = r"E:\\UNM\\Car-Model\\simplified_Car.obj"
        simplify_obj(original_path,simplified_path,target_faces_ratio=0.1)
        
        # vertices, faces = parse_obj_fast(simplified_path)
        
        mesh = OpenGLPMobject.from_obj(simplified_path)
        mesh.set_color(GRAY).set_opacity(0.8)
        
        axes = ThreeDAxes()
        self.add(axes,mesh)
        self.set_camera_orientation(phi=75*DEGREES,theta=30*DEGREES)






class proof(Scene):
    def construct(self):
        scaling = Text("Scaling",font_size=144)
        self.play(Write(scaling))
        self.wait(2)
        self.play(FadeOut(scaling))

        scaling_graph = Axes(x_range=[-2,5,1],y_range=[-2,5,1],x_length=7,y_length=7,axis_config={"include_tip":True},).shift(LEFT*3)
        square = Square(side_length=1,color=BLUE, fill_opacity=0.5).move_to(scaling_graph.c2p(0.5,0.5))

        def get_vertex_dots():
            return VGroup(*[Dot(point=vertex,color = WHITE) for vertex in square.get_vertices()])
        
        vertex_dots = always_redraw(get_vertex_dots)

        label_xy = always_redraw(lambda:MathTex("(x, y)").next_to(square,UR,buff=0.2))
        sx_arrow = DoubleArrow(start=scaling_graph.c2p(-0.25,-0.5),end=scaling_graph.c2p(3.25,-0.5), color=YELLOW,)
        sx_label = MathTex("s_x=3").next_to(sx_arrow,DOWN,buff=0.2)
        sy_arrow = DoubleArrow(start=scaling_graph.c2p(3.5,-0.25), end=scaling_graph.c2p(3.5,2.25), color=YELLOW,width = 0.1)
        sy_label = MathTex("s_y=2").next_to(sy_arrow,RIGHT,buff=0.2)
        
        self.play(Create(scaling_graph) ,Create(square),Create(vertex_dots))
        self.wait(1)
        self.play(Write(label_xy))
        self.wait(1)

        self.play(square.animate.scale([3,1,1]).move_to(scaling_graph.c2p(0,0),DL))
        self.play(Create(sx_arrow),Write(sx_label))
        self.play(square.animate.scale([1,2,1]).move_to(scaling_graph.c2p(0,0),DL))
        self.play(Create(sy_arrow),Write(sy_label))
        self.wait(2)

        scaling_text = MathTex(r"x'= s_x \cdot x \\"
                               r"y'= s_y \cdot y").shift(RIGHT*4).shift(UP*2)
        self.play(Write(scaling_text))
        self.wait(2)
        scaling_matrix = MathTex(
            r"\begin{bmatrix} x' \\ y' \end{bmatrix} ="
            r"\begin{bmatrix} s_x & 0 \\ 0 & s_y \end{bmatrix}"
            r"\begin{bmatrix} x \\ y \end{bmatrix}"
        ).next_to(scaling_text, DOWN, buff = 1)

        self.play(Transform(scaling_text.copy(), scaling_matrix))
        self.wait(3)
        self.play(square.animate.scale([1/3,1/2,1]).move_to(scaling_graph.c2p(0.0),DL),FadeOut(sx_arrow,sx_label,sy_arrow,sy_label,scaling_text))
        self.wait(1)

        Rotation = Text("Rotation",font_size=144)
        self.play(*[FadeOut(mob)for mob in self.mobjects])
        self.play(Write(Rotation))
        self.wait(2)
        self.play(FadeOut(Rotation))

        self.play(Create(scaling_graph))
        theta = 90 *DEGREES
        r = 4
        alpha = 30 *DEGREES
        start_point = scaling_graph.c2p(0, 0)
        end_point = scaling_graph.c2p(r *np.cos(alpha), r * np.sin(alpha))
        
        lable_xy1 = MathTex(r"(x, y)").next_to(end_point,UR,buff=0.2)
        vector = Arrow(start=start_point,end=end_point,buff=0,color=WHITE)
        
        rotated_end =scaling_graph.c2p(r * np.cos(alpha + theta), r * np.sin(alpha + theta))
        rotated_vector = Arrow(start=start_point, end=rotated_end,buff=0, color=YELLOW)
        
        label_alpha = Angle(
            line1=Line(start_point,scaling_graph.c2p(1,0)),
            line2=vector,
            radius=0.8,
            other_angle=False,
            color=WHITE
            )
        alpha_lable = MathTex(r"\alpha").next_to(label_alpha,RIGHT*0.5,buff=0.1)
        label_theta = Angle (
            line1=  vector,
            line2=rotated_vector,
            radius=0.8,
            other_angle=False,
            color=WHITE
        )
        
        theta_lable = MathTex(r"\theta").next_to(label_theta,UP,buff=0.1)
        label_xy_prime = MathTex(r"(x', y')").next_to(rotated_end,UR,buff=0.2)
        
        self.play(Create(vector),Write(lable_xy1))
        self.play(Create(label_alpha),Write(alpha_lable))
        self.wait(2)

        
        self.play(Rotate(vector.copy(),angle=theta,about_point=scaling_graph.c2p(0,0)), Create(label_theta),Write(theta_lable))
        self.play(Create(rotated_vector), Write(label_xy_prime))
        self.wait(2)

        rotation_equation1 = MathTex(
            r"x = r \cos \alpha \\"
            r"y = r \sin \alpha",
            font_size = 36
        ).shift(RIGHT*3).shift(UP*3)

        rotation_equation2 = MathTex(
            r"x' = r \cos(\alpha + \theta) \\"
            r"y' = r \sin(\alpha + \theta)",
            font_size = 36
        ).next_to(rotation_equation1,DOWN,buff=0.5)

        rotation_equation3 = MathTex(
            r"x' = r \cos(\alpha + \theta) = r \cos\alpha \cos\theta - r \sin\alpha \sin\theta \\"
            r"y' = r \sin(\alpha + \theta) = r \sin\alpha \cos\theta + r \cos\alpha \sin\theta",
            font_size = 36
        ).next_to(rotation_equation1,DOWN,buff=0.5)

        rotation_equation4 = MathTex(
            r"x' = x \cos\theta - y \sin\theta \\"
            r"y' = x \sin\theta + y \cos\theta",
            font_size = 36
        ).next_to(rotation_equation3,DOWN,buff=0.5)

        self.play(Write(rotation_equation1))
        self.wait(1)
        self.play(Write(rotation_equation2))
        self.wait(1)
        self.play(FadeOut(rotation_equation2), Write(rotation_equation3))
        self.wait(1)
        self.play(Transform(Group(rotation_equation3.copy(), rotation_equation1.copy()),rotation_equation4))
        self.wait(2)

        rotation_matrix = MathTex(
            r"\begin{bmatrix} x' \\ y' \end{bmatrix} ="
            r"\begin{bmatrix} \cos\theta & -\sin\theta \\ \sin\theta &\cos\theta \end{bmatrix}"
            r"\begin{bmatrix} x \\ y \end{bmatrix}",
            font_size = 36
        ).next_to(rotation_equation4,DOWN,buff = 0.5)

        self.play(Transform(rotation_equation4.copy(),rotation_matrix))
        self.wait(3)
        
        


        


        


